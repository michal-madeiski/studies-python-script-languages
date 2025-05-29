#zad4
def triangle_square():
    print ("Program obliczający pole trójkąta: \n")
    a = int(input("wartość a: "))
    h = int(input("wartość h: "))
    s = (a * h) / 2
    print(s)
triangle_square()
#zad4

#zad5
import pyfiglet

def create_ascii_art():
    print("Program zwracający ascii art tekstu: \n")
    t = input("tekst: ")
    print(pyfiglet.figlet_format(t))
create_ascii_art()
#zad5
