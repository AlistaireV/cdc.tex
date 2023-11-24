from microbit import *
import music
import time

# Adresse de la mémoire flash pour stocker la valeur de count
FLASH_ADDRESS = 0

def write_count_to_flash(count):
    try:
        with open("count", "w") as file:
            file.write(str(count))
    except:
        pass
# ici c est pour stocker ma variable pour quand on l'étains 
def read_count_from_flash():
    try:
        with open("count", "r") as file:
            return int(file.read())
    except:
        return 0

def start():
    for x in range(2):
        music.play(["C4:4", "D4", "E4", "C4"])
    for x in range(2):
        music.play(["E4:4", "F4", "G4:8"])
        time.sleep(5)

def command():
    if button_a.was_pressed():
        setting()

def menu():
    while True:
        display.show(Image.DUCK)
        if command():
            break

def setting():
    global count

    display.scroll("Launch of the milk counter")
    display.show(count)
    while True:
        if button_b.is_pressed():
            count += 1
            display.show(count) #cc
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
            # Sauvegarde la valeur das  la mémoire flash
            write_count_to_flash(count)
            menu()

def main():
    global count
    count = read_count_from_flash()
    start()
    menu()

if __name__ == "__main__":
    main()
