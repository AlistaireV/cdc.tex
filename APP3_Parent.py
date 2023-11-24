#Code pour le BEtag des parents
from microbit import *
import radio
import music
import time

radio.config(group=22)
radio.on()

    
def start():
    for x in range(2):
        music.play(["C4:4", "D4", "E4", "C4"])
    for x in range(2):
        music.play(["E4:4", "F4", "G4:8"])
        sleep(5)

def command():
    if button_a.was_pressed():
        setting()


def menu():
    while True :
        display.show(Image.DUCK)
        command()
        if command():
            break

count = 0
def setting():
    global count

    display.scroll("Launch of the milk counter")
    display.show(0)
    while True:
        if button_b.is_pressed():
            count += 1
            display.show(count)
            sleep(500)
        if button_a.is_pressed():
            count -= 1
            display.show(count)
            sleep(500)
        if accelerometer.was_gesture('shake'):
            count = 0
            display.show(count)
            sleep(500)
        if pin_logo.is_touched():
            menu()


def main():
    start()
    menu()

if __name__ == "__main__":
    main()

