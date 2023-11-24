# BeTag du bébé qui doit povoir communiquer avec celui des parents
from microbit import *
import radio

radio.config(group=22)
radio.on()
import log 
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
      #'light': fonction circadienne de Kaan ()
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
