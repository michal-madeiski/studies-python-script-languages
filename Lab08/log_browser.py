import os
import sys
from PySide6.QtWidgets import (QApplication, QPushButton, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QWidget,
                               QDateEdit, QFormLayout, QFileDialog, QListWidget)
from PySide6.QtCore import QDate
from PySide6.QtGui import QIcon
from Lab03.zad2a import read_log, filter_logs
from Lab03 import utils
from style import style

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(sys.prefix, "Lib", "site-packages", "PySide6", "plugins", "platforms")

class LogBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setWindowIcon(QIcon("log_icon.png"))
        self.setWindowTitle("Log Browser")

        self.logs = []
        self.filtered_logs = []
        self.curr_log_idx = 0

        self.path_to_logs = QLineEdit()
        self.date_from = QDateEdit()
        self.date_to = QDateEdit()
        self.log_list = QListWidget()

        self.next_button = QPushButton("Next")
        self.prev_button = QPushButton("Previous")

        self.remote_host = QLineEdit(""); self.remote_host.setReadOnly(True); self.remote_host.setProperty("class", "log_info")
        self.date = QLineEdit(""); self.date.setReadOnly(True); self.date.setProperty("class", "log_info")
        self.time = QLineEdit(""); self.time.setReadOnly(True); self.time.setProperty("class", "log_info")
        self.method = QLineEdit(""); self.method.setReadOnly(True); self.method.setProperty("class", "log_info")
        self.status_code = QLineEdit(""); self.status_code.setReadOnly(True); self.status_code.setProperty("class", "log_info")
        self.uri = QLineEdit(""); self.uri.setReadOnly(True); self.uri.setMaximumWidth(680); self.uri.setProperty("class", "log_info")

        self.setStyleSheet(style)
        self.create_gui()

    def create_gui(self):
        main_layout = QVBoxLayout()
        up_layout = QVBoxLayout()
        down_layout = QFormLayout()

        # file_layout
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("File: "), 1)

        search_button = QPushButton("Search file with logs")
        search_button.clicked.connect(self.open_file)

        self.path_to_logs.setReadOnly(True)
        file_layout.addWidget(self.path_to_logs, 7)
        # file_layout

        # date_layout
        date_layout = QHBoxLayout()

        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(QDate(2000, 1, 1))
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(QDate.currentDate())
        self.date_from.dateChanged.connect(self.update_filtered)
        self.date_to.dateChanged.connect(self.update_filtered)

        date_layout.addWidget(QLabel("Date from: "))
        date_layout.addWidget(self.date_from)
        date_layout.addWidget(QLabel("Date to: "))
        date_layout.addWidget(self.date_to)
        # date_layout

        # log_list
        self.log_list.currentRowChanged.connect(self.show_details)
        # log_list

        # nav_layout
        nav_layout = QHBoxLayout()

        self.prev_button.clicked.connect(self.show_prev)
        self.next_button.clicked.connect(self.show_next)

        nav_layout.addWidget(self.prev_button)
        nav_layout.addWidget(self.next_button)
        # nav_layout

        # up_layout
        up_layout.addWidget(search_button)
        up_layout.addLayout(file_layout)
        up_layout.addLayout(date_layout)
        up_layout.addWidget(self.log_list)
        up_layout.addLayout(nav_layout)
        # up_layout

        # down_layout
        down_layout.addRow("Remote host:", self.remote_host)
        down_layout.addRow("Date:", self.date)
        down_layout.addRow("Time:", self.time)
        down_layout.addRow("Method:", self.method)
        down_layout.addRow("Status code:", self.status_code)
        down_layout.addRow("Resource:", self.uri)
        # down_layout

        # main_layout
        main_layout.addLayout(up_layout, 4)
        main_layout.addLayout(down_layout, 2)
        # main_layout

        self.setLayout(main_layout)

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file with logs", "", "Log files (*.log *.txt);;All files (*)")
        if path:
            self.path_to_logs.setText("")
            self.path_to_logs.setText(path)
            with open(path, "r", encoding="utf-8") as f:
                self.logs = read_log(f)
                self.update_filtered()

    def update_filtered(self):
        date_f = self.date_from.date().toPython()
        date_t = self.date_to.date().toPython()

        self.filtered_logs = filter_logs(self.logs, date_f, date_t)
        self.log_list.clear()
        for i, log in enumerate(self.filtered_logs):
            text = f"{i+1}. {log[utils.entry_idx['orig_h']]} - [{log[utils.entry_idx['ts']].strftime('%d/%b/%Y:%H:%M:%S')}] \"{log[utils.entry_idx['method']]} {log[utils.entry_idx['uri']]}\""
            self.log_list.addItem(text[:50] + ("..." if len(text) > 50 else ""))

        self.curr_log_idx = 0
        self.log_list.setCurrentRow(self.curr_log_idx)
        self.show_details(self.curr_log_idx)

    def show_details(self, index):
        self.curr_log_idx = index
        self.remote_host.setText("")
        self.date.setText("")
        self.time.setText("")
        self.method.setText("")
        self.status_code.setText("")
        self.uri.setText("")

        if not self.filtered_logs or index < 0 or index >= len(self.filtered_logs):
            return

        log = self.filtered_logs[index]

        self.remote_host.setText(log[utils.entry_idx["orig_h"]])
        self.date.setText(str(log[utils.entry_idx["ts"]].date()))
        self.time.setText(log[utils.entry_idx["ts"]].strftime("%H:%M:%S"))
        self.method.setText(log[utils.entry_idx["method"]])
        self.status_code.setText(str(log[utils.entry_idx["status_code"]]))
        self.uri.setText(log[utils.entry_idx["uri"]])

        self.prev_button.setEnabled(index > 0)
        self.next_button.setEnabled(index < len(self.filtered_logs) - 1)

    def show_next(self):
        if self.curr_log_idx < len(self.filtered_logs) - 1:
            self.curr_log_idx += 1
            self.log_list.setCurrentRow(self.curr_log_idx)
            self.show_details(self.curr_log_idx)

    def show_prev(self):
        if self.curr_log_idx > 0:
            self.curr_log_idx -= 1
            self.log_list.setCurrentRow(self.curr_log_idx)
            self.show_details(self.curr_log_idx)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = LogBrowser()
    browser.show()
    sys.exit(app.exec())