# BeTag du bébé qui doit povoir communiquer avec celui des parents
from microbit import *
import radio

radio.config(group=23)
radio.on()
import log 


SET_COUNT=0

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
        if button_b.was_pressed():
             establish_connexion("singe")

def setting():
     """Cette fonction permet de faire un choix de la fonnction 
        Cette fonction permet de faire un choix entre toutes le fonctions du tag 
        pré: un appel grace au button du menu 
        post: affiche des chiffres pour sélectionner la fonctionalité 
    """
     display.scroll(" choose your function ") 
     global SET_COUNT 
     display.show(SET_COUNT)
     while True :
        if button_b.is_pressed():
            SET_COUNT += 1
            display.show(SET_COUNT)
            sleep(500)
        if button_a.is_pressed():
            SET_COUNT -= 1
            display.show(SET_COUNT)
            sleep(500)
        if accelerometer.was_gesture('shake'):
            menu()
        if pin_logo.is_touched():
            if SET_COUNT == 1:
                temperature_alert()
            elif SET_COUNT == 2:
                 show_light()
            elif SET_COUNT == 3:
                log_data()
        

            

"""
Faire une boucle while True : 
    Mettre une condition, si delay = autant. 
        Si c'est le cas alors, il faut que le microbit mesure la température et l'envoie au niveau du Be:bi parent uniquement 
        si la température n'est pas dans le bon range (20°C - 24°C)
        Une fois que le Be:bi parent reçoit un message il va chanter en mode 'alerte' en fonction de la température reçue avec différents paliers
        pour éviter de hurler à la mort si la température de la pièce est 19.9°C. Il va falloir mettre une alerte quand on aura dépasser une 
        température de sécurité. Disons 1°C en-dessous ou au-dessus de chaque limite
        
    Si le delay = autant n'est pas respecté alors il faut que le microbit :
        Puisse recevoir des messages et que à la moindre réception de message = temperature () il fasse :
            une mesure de la température et qu'il transmette cette température au Be:bi parent
"""

"""
Seconde fonctionnalité : Boussole au niveau du microbit qui va permettre de voir si le bébé 
se trouve sur le dos (Danger lié à la régurgitation de l'enfant). Si le bébé se retrouve sur le dos 
à deux moments donnés successifs (avec un intervalle de 2 minutes par exemple) alors
le micorbit enfant va envoyer un message ou une alerte au microbit parent
"""
def log_data():
    log.add({
      'Temperature': temperature(),
      'Heure': time_secondes
      'Light': read_light_level()
    })

def temperature_alert() : 
    if time_secondes == 3600 :
        time_secondes = 0
        temp_measurement = temperature()
        if temp_measurement <= 19 :
            display.show(temp_measurement)
            radio.send('Need heat')
        elif temp_measurement >= 25 :
            display.show(temp_measurement)
            radio.send('Need cold')
    else : 
        ask_temperature = radio.receive()
        if ask_temperature == 'ask temperature' : 
            temp_measurement = str(temperature())
            radio.send(temp_measurement)

time_secondes = 0
while True :
    data_monitoring = log_data()
    sleep(1000)
    time_secondes +=1
    alerte_temperature = temperature_alert()

"""
compass.calibrate()
if compass.is_calibrated() == True : 
        orientation1 = compass.heading()
        sleep(12000)
        orientation2 = compass.heading()
        if orientation1 < 45 or orientation1 > 315 and orientation2 < 45 or orientation2 > 315 :
            sleep(12000)
            orientation3 = compass.heading()
            if orientation3 < 45 or orientation3 > 315 : 
                radio.send('Changer la position')
    else : 
        compass.clear_calibration()
"""


# Partie de la veilleuse, avec une certaine luminosité, il faut allumer ou éteindre la veilleuse (Stitch). PS: J'ai juste mis 0 pour l'instant pour dire que c'est sombre, avec des tests je pourrais en savoir plus.
def show_light():
    global light_level
    light_level = display.read_light_level()
    display.show(Image.DIAMOND_SMALL)
    sleep(400)
    display.show(Image.DIAMOND)
    sleep(900)
    display.scroll('Light level:',100)
    display.scroll(light_level,100)
    display.show(Image.DUCK)

def light():
    if light_level <= 50:
        display.scroll('Activate Stitch',100)
        display.show(Image.DUCK)
    else:
        display.scroll('Deactivate Stitch',100)
        display.show(Image.DUCK)
    
while True:
    if button_a.was_pressed():
        show_light()
    elif button_b.was_pressed():
        light()
    elif pin_logo.is_touched():
        menu()



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
    if button_a.was_pressed() :
        random_number = random.randrange(50000)
        send_message=vigenere(str(random_number),password)
        radio.send(send_message)
        math_action= (random_number)*10
        display.scroll(math_action)
    send_message = radio.receive()
    if send_message:
        read_message=vigenere(send_message,password,True)
        display.scroll(read_message)

def main():
    start()
    menu()

if __name__ == "__main__":
    main()
