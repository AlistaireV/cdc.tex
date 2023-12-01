from microbit import *
import music
import time


# Code in a 'while True:' loop repeats foreve# Imports go at the top
from microbit import *
from math import *
import radio


radio.config(group=23)

def vigenere(message, key, decryption=False):
    text = ""
    key_length = len(key)
    key_as_int = [ord(k) for k in key]

    for i, char in enumerate(str(message)): #le i fait réf à la position du str et le char fait réf ay caractère de la position 
        key_index = i % key_length
        #Letters encryption/decryption
        if char.isalpha():
            if decryption:
                modified_char = chr((ord(char.upper()) - key_as_int[key_index] + 26) % 26 + ord('A'))
            else : 
                modified_char = chr((ord(char.upper()) + key_as_int[key_index] - 26) % 26 + ord('A'))
            #Put back in lower case if it was
            #La fonction ord() permet de renvoyer la valeur unicode associé au caractère
            #la fonction chr() fait l'inverse càd qu'elle renvoie le caractère associé à la valeur unicode
            if char.islower():
                modified_char = modified_char.lower()
            text += modified_char
        #Digits encryption/decryption
        elif char.isdigit():
            if decryption:
                modified_char = str((int(char) - key_as_int[key_index]) % 10)
            else:  
                modified_char = str((int(char) + key_as_int[key_index]) % 10)
            text += modified_char
        else:
            text += char
    return text

while True :
    password='singe'
    message_send = radio.receive()
    if message_send : 
        message_decrypte = vigenere(message_send,password,True)
        math_action = int(message_decrypte)+10
        radio.send(vigenere(str(math_action),password))
        display.scroll(math_action)
    
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
            display.show(MILK_COUNT) #je fais un test
            
            sleep(500)
        if pin_logo.is_touched():
            menu()
def main():
    start()
    menu()

if __name__ == "__main__":
    main()
