# BeTag du bébé qui doit povoir communiquer avec celui des parents
from microbit import *
import radio

radio.config(group=22)
radio.on()
import log 

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

