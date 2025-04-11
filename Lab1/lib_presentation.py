import numpy as np #rozkład punktów
import matplotlib.pyplot as plt #wykresy
from mplsoccer import Pitch #heatmapa piłkarza

#Heatmapa zawodnika za pomocą mplsoccer

num_of_pos = 10000 #liczba punktów, w których pojawiał się zawodnik

#generowanie pozycji - rozkład Gaussa - koncentracja wokół środka (bardziej realne)
center_x, center_y = 60, 40 #boisko 120x80
sigma_x, sigma_y = 30, 20 #odchylenia

np.random.seed(42)
x_positions = np.clip(np.random.normal(center_x, sigma_x, num_of_pos), 0, 120)
y_positions = np.clip(np.random.normal(center_y, sigma_y, num_of_pos), 0, 80)

statistic = np.zeros((24, 25)) #pusta siatka boiska: 25x24 według strony pasuje do 120x80
for i in range(num_of_pos):
    #normalizacja x i y na współrzędne siatki z komórkami 5x3.5
    x_pos = int(x_positions[i] // 5) #bo 120 / 24 = 5
    y_pos = int(y_positions[i] // 3.47) #bo 80 / 23 = 3.47
    statistic[y_pos, x_pos] += 1 #zwiększenie liczby pojawień się zawodnika na danym polu

y, x = statistic.shape #tworzenie boiska z siatki
x_grid = np.linspace(0, 120, x + 1) #wspołrzędne x boiska - 24 komórki równomierne rożłożóne na dł 120
y_grid = np.linspace(0, 80, y + 1) #wspołrzędne y boiska - 23 komórki równomierne rożłożóne na dł 80
stats = dict(statistic=statistic, x_grid=x_grid, y_grid=y_grid) #słownik przekazywany do heatmapy

#zmiany wizualne (typ boiska, kolor, czcionka, przezroczystość, motyw, wyświetlane informacje)
pitch = Pitch(pitch_type='statsbomb', line_zorder=2, pitch_color='green', line_color='white') #(line_zorder=2 tzn linie będą widoczne)
fig, ax = pitch.draw(figsize=(13.2, 8.25)) #wymiary w calach; fig-figura(boisko), ax-osie
heatmap = pitch.heatmap(stats, ax=ax, cmap='plasma')
color_bar = fig.colorbar(heatmap, ax=ax, shrink=0.6) #pasek kolorów
color_bar.ax.tick_params(labelsize=15) #czcionka paska kolorów
color_bar.outline.set_edgecolor('black') #obramowanie paska kolorów
color_bar.ax.yaxis.set_tick_params(color='black') #oś y paska kolorów
plt.title("PlayerX's heatmap", fontsize=20, color='black') #tytuł

#wyświetlanie
plt.show()