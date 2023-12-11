#Backend
# BeTag du bébé qui doit povoir communiquer avec celui des parents
from microbit import *
import radio
import random
radio.config(group=23)
radio.on()

key = "Betag"
dictionnary = {}
lst = ['00','01','02','03']
for element in lst : 
    dictionnary[element] = []

def hashing(string):
	"""
	Hachage d'une chaîne de caractères fournie en paramètre.
	Le résultat est une chaîne de caractères.
	Attention : cette technique de hachage n'est pas suffisante (hachage dit cryptographique) pour une utilisation en dehors du cours.

	:param (str) string: la chaîne de caractères à hacher
	:return (str): le résultat du hachage
	"""
	def to_32(value):
		"""
		Fonction interne utilisée par hashing.
		Convertit une valeur en un entier signé de 32 bits.
		Si 'value' est un entier plus grand que 2 ** 31, il sera tronqué.

		:param (int) value: valeur du caractère transformé par la valeur de hachage de cette itération
		:return (int): entier signé de 32 bits représentant 'value'
		"""
		value = value % (2 ** 32)
		if value >= 2**31:
			value = value - 2 ** 32
		value = int(value)
		return value

	if string:
		x = ord(string[0]) << 7
		m = 1000003
		for c in string:
			x = to_32((x*m) ^ ord(c))
		x ^= len(string)
		if x == -1:
			x = -2
		return str(x)
	return ""

MILK_COUNT = 0
SET_COUNT=0


def menu():
    """ Cette fonction et l interface menu 
        Cette fonction permet d avoir un menu avec une image et d'acceder aux différentes fonctions du BEtag
        pré: start ()
        post: affiche une image de menu et donne accès à tous les commande possible
    """
    global key
    global MILK_COUNT
    while True:
        veilleuse(key)
	radio.receive()
        message_recu = radio.receive()
        if message_recu : 
            unpack_data(message_recu,key)
        elif button_a.was_pressed() : 
            display.scroll(MILK_COUNT)
            
        
        
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
	if SET_COUNT <=0
	     SET_COUNT = 0
	     display.show(SET_COUNT)
        if button_b.was_pressed():
            SET_COUNT += 1
            display.show(SET_COUNT)
        if button_a.was_pressed():
            SET_COUNT -= 1
            display.show(SET_COUNT)
        if accelerometer.was_gesture('shake'):
            menu()
        if pin_logo.was_touched():
            if SET_COUNT == 1:
                milk()
     



def vigenere(message, key, decryption=False):
    global key
    text = ""
    key_length = len(kkey)
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


def unpack_data (encrypted_packed,key) : 
    global key
    global dictionnary
    global MILK_COUNT
    decryption_message = encrypted_packed.split('|')
    message_en_clair = decryption_message[2].split(':')
    encrypted_packet = tuple(message_en_clair)
    nonce,content = encrypted_packet
    if decryption_message[0] == '00' :
        for clef in dictionnary : 
            if clef == '00' :
                nonce_decrypted = vigenere(nonce,key) 
                if nonce_decrypted in dictionnary['00'] : 
                    display.scroll('ERROR message already received')
                else : 
                    dictionnary['00'].append(nonce_decrypted)
                    message_decripte_vigenere = vigenere(content,key,True) #Here we will decrypt the content of the message
                    response_challenge = calculate_challenge(message_decripte_vigenere)
                    valeur_hashing_response = hashing(str(response_challenge))
                    send_packet("00",valeur_hashing_response,key)
                    key += str(response_challenge)
                    return message_decripte_vigenere
                
            if clef == '01' : #MILK_COUNT
                nonce_decrypted = vigenere(nonce,key) 
                if nonce_decrypted in dictionnary['01'] : 
                    display.scroll('ERROR message already received')
                else : 
                    dictionnary['01'].append(nonce_decrypted)
                    display.scroll('Message added')
                    message_decripte_vigenere = vigenere(content,key,True)
		    MILK_COUNT = message_decripte_vigenere 
                    return message_decripte_vigenere
                    
            if clef == '02' : 
                nonce_decrypted = vigenere(nonce,key) 
                if nonce_decrypted in dictionnary['02'] : 
                    display.scroll('ERROR message already received')
                else : 
                    dictionnary['02'].append(nonce_decrypted)
                    display.scroll('Message added')
                    message_decripte_vigenere = vigenere(content,key,True) #Here we will decrypt the content of the message
                    return message_decripte_vigenere
            if clef == '03' :
                nonce_decrypted = vigenere(nonce,key) 
                if nonce_decrypted in dictionnary['03'] : 
                    display.scroll('ERROR message already received')
                else : 
                    dictionnary['03'].append(nonce_decrypted)
                    display.scroll('Message added')
                    message_decripte_vigenere = vigenere(content,key,True) #Here we will decrypt the content of the message
                    return message_decripte_vigenere


def calculate_challenge (challenge) : 
    return int(challenge)*5

def send_packet(type_message,contenu,key): 
    contenu_vigenered = vigenere(contenu,key)
    nbre_aleatoire = random.randrange(5000)
    nbre_aleatoire_vigenered = vigenere(nbre_aleatoire,key)
    encrypted_message = nbre_aleatoire_vigenered + ':' + contenu_vigenered
    long_message = len(encrypted_message)
    radio_send = '{0}|{1}|{2}'.format(type_message,str(long_message),encrypted_message)
    display.scroll(radio_send,300)
    radio.send(radio_send)


def veilleuse (key) : 
    """
    @Pre : Doit recevoir une commande de la part du BeTag parent qui lui dit que le bébé a été mis au lit
           Si elle reçoit un 'start_veilleuse' elle doit rester allumer tant que la lumière n'est pas 
           au-delà de 80. 
           Dès que la lumière est-au delà de 80 la veilleuse s'éteint
    @Post : Doit s'allumer à partir d'une certaine luminosité 
            Doit s'éteindre dès que la luminosité est assez importante 
    """
    light_level = display.read_light_level()
    
    if light_level <= 50:
        display.show(Image(
        "99999:"
        "99999:"
        "99999:"
        "99999:"
        "99999"))
        temperature_measurement(key)
        agitation_bebe(key)
            
    elif 50 > light_level <= 90 :
        """
        Il faudra vérifier une luminosité qui empêche les bébés de dormir
        """

        temperature_measurement(key)
        agitation_bebe(key)

def temperature_measurement (key,type='02') : 
    """
    Cette fonctionnalité pourrait être intéressante dans la fonctionnalité de mesure de luminosité 
    car c'est pendant que le bébé dort que la température est le paramètre important à surveiller
    MAIS 
    Il faut une récurrence de mesure 
    @Pre : Ne s'active que lorsque le bébé est en phase de dodo
    @Post : Va mesurer la température et utiliser le codage selon Vigenere pour envoyer des données
    au BeTag parent 
    """
    measure_temperature = temperature()
    if measure_temperature <= 19 :
        send_packet(key, type, str(measure_temperature)+'- Need heat') #Utilisation def send_packet pour envoie
        #de données cryptées 
    elif measure_temperature >= 25 :
        send_packet(key, type, str(measure_temperature)+'- Need cold') #Utilisation def send_packet pour envoie
        #de données cryptées

def calibration(key,type='03'):
    display.scroll(compass.heading())
    compass.calibrate()
    if compass.is_calibrated() == True : 
        orientation1 = compass.heading()
        sleep(15000)
        orientation2 = compass.heading()
        gap = abs(orientation2-orientation1)
        if gap <= 15:
            send_packet(type,'Endormie',key)
        elif 15 < gap <= 45:
            send_packet(type,'Agite',key)
        else:
            send_packet(type,'Tres agite',key)
        orientation3 = compass.heading()
        if orientation3 == 180: 
            send_packet(type,'Changer la position',key)
    else : 
        compass.clear_calibration()

def agitation_bebe (key,type='03') : 
    noise_level = microphone.sound_level()
    if 45 < noise_level < 60: 
        send_packet(type,'Bebe peut etre reveille et agite',key)
    elif noise_level > 60 : 
        send_packet(type,'Bebe reveille',key)

        
display.scroll('Welcome')
if __name__ == '__main__' :
    menu()
    
