from microbit import *
import music
import time


MILK_COUNT = 0


def start():
    """ Cette fonction sert à l'allumage
        Cette fonction permet de lancer une musique lors de l'allumage du Betag 
    pré: pousser le boutton d'allumage pour passer de l'état éteint à allumé
    post: fait une musique 
    """
    for x in range(2):
        music.play(["C4:4", "D4", "E4", "C4"])
    for x in range(2):
        music.play(["E4:4", "F4", "G4:8"])

    

def menu():
    """ Cette fonction et l interface menu 
        Cette fonction permet d avoir un menu avec une image et d'acceder aux différentes fonctions du BEtag
        pré: start ()
        post: affiche une image de menu et donne accès à tous les commande possible
    """
    while True:
        display.show(Image.DUCK)
        if button_a.was_pressed() : 
            setting()


def setting():
    """ Cette fonction permet de compter la dose de lait donner au bébé 
        Cette fonction permet de compter la dose de lait donner au bébé et l'envoyer au BEtag bébé
    pré: le button a doit etre préssé dans le menu pour activer la fonction
    post: affiche le compteur de dose de lait et l'envoit au BEtag enfant
    """
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
            menu()

def main():
    start()
    menu()

if __name__ == "__main__":
    main()
