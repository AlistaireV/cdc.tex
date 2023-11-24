from microbit import *
import music
import time


MILK_COUNT = 0


def start():
    for x in range(2):
        music.play(["C4:4", "D4", "E4", "C4"])
    for x in range(2):
        music.play(["E4:4", "F4", "G4:8"])

def command():
    if button_a.was_pressed():
        setting()
    

def menu():
    while True:
        display.show(Image.DUCK)
        if button_a.was_pressed() : 
            setting()


def setting():
    global MILK_COUNT
    display.scroll(" milk")
    display.show(MILK_COUNT)
    while True:
        if button_b.is_pressed():
            MILK_COUNT += 1
            display.show(MILK_COUNT)
            sleep(500)
        if button_a.is_pressed():
            MILK_COUNT -= 1
            display.show(MILK_COUNT)
            sleep(500)
        if accelerometer.was_gesture('shake'):
            MILK_COUNT = 0
            display.show(MILK_COUNT)
            sleep(500)
        if pin_logo.is_touched():
            # Sauvegarde la valeur das  la mémoire flash
            menu()

def main():
    start()
    menu()

if __name__ == "__main__":
    main()
