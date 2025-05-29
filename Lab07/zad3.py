import random as rd
import string

class PasswordGenerator:
    def __init__(self, length, count, charset=string.ascii_letters + string.digits):
        self.length = length
        self.count = count
        self.charset = charset

    def __iter__(self):
        return self

    def __next__(self):
        if self.count == 0:
            raise StopIteration
        password = ""
        for i in range(self.length):
            password += rd.choice(self.charset)
        self.count -= 1
        return password


if __name__ == "__main__":
    count = 9
    length = 8
    password_generator = PasswordGenerator(length, count)
    for i in range(count + 1):
        print(f"{i + 1}) {password_generator.__next__()}")