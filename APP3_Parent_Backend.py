#Backend
# BeTag des parents qui doit povoir communiquer avec celui du bébé
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

MILK_COUNT = 0
SET_COUNT=0
content = 0

def menu():
    """ Cette fonction et l interface menu 
        Cette fonction permet d avoir un menu avec une image et d'acceder aux différentes fonctions du BEtag
        pré: start ()
        post: affiche une image de menu et donne accès à tous les commande possible
    """
    while True:
        display.show(Image.DUCK)
        message = radio.receive()
        if button_a.was_pressed() : 
            setting()
        elif button_b.was_pressed():
             establish_connexion(key)

        return message

def setting():
    """Cette fonction permet de faire un choix de la fonction 
    Cette fonction permet de faire un choix entre toutes les fonctions du tag 
    pré: un appel grâce au bouton du menu 
    post: affiche des chiffres pour sélectionner la fonctionnalité 
    """
    display.scroll(" choose your function ") 
    global SET_COUNT 
    display.show(SET_COUNT)
    while True:
        if SET_COUNT <= -1:
            SET_COUNT = 0
            display.show(SET_COUNT)
            sleep(500)
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
            pass
        if pin_logo.is_touched():
            if SET_COUNT == 1:
                milk()
                pass

if __name__ == '__main__':
    setting()
     
def milk():
    """Cette fonction permet de compter la dose de lait donnée au bébé
    Cette fonction permet de compter la dose de lait donnée au bébé et l'envoyer au BEtag bébé
    pré: le bouton a doit être pressé dans le menu pour activer la fonction
    post: affiche le compteur de dose de lait et l'envoie au BEtag enfant
    """
    global MILK_COUNT
    display.scroll("Milk")
    display.show(MILK_COUNT)
    
    while True:
        if MILK_COUNT <= 0:
            MILK_COUNT = 0
            display.show(MILK_COUNT)
            sleep(500)
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
            display.show(MILK_COUNT)  # je fais un test
            sleep(500)
        if pin_logo.is_touched():
            menu()

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


def unpack_data (encrypted_packed,key) : 
    global content
    decryption_message = encrypted_packed.split('|')
    message_en_clair = decryption_message[2].split(':')
    encrypted_packet = tuple(message_en_clair)
    nonce,content = encrypted_packet
    dictionnary = {}
    lst = ['00','01','02','03']
    for element in lst : 
        dictionnary[element] = [] 
    if decryption_message[0] == '00' :
        for clef in dictionnary : 
            if clef == '00' :
                nonce_decrypted = vigenere(nonce,key,True)
                if nonce_decrypted in dictionnary['00'] : 
                    display.scroll('ERROR message already received')
                else : 
                    dictionnary['00'].append(nonce_decrypted)
                    display.scroll('Message added connexion')
                    message_decripte_vigenere = vigenere(content,key,True) #Here we will decrypt the content of the message
                    calcul_response(message_decripte_vigenere)
                    return message_decripte_vigenere 
            if clef == '01' : 
                nonce_decrypted = vigenere(nonce,key,True)
                if nonce_decrypted in dictionnary['01'] : 
                    display.scroll('ERROR message already received')
                else : 
                    dictionnary['01'].append(nonce_decrypted)
                    display.scroll('Message added to Milk')
                    message_decripte_vigenere = vigenere(content,key,True) #Here we will decrypt the content of the message
                    return message_decripte_vigenere
            if clef == '02' : 
                nonce_decrypted = vigenere(nonce,key,True)
                if nonce_decrypted in dictionnary['02'] : 
                    display.scroll('ERROR message already received')
                else : 
                    dictionnary['02'].append(nonce_decrypted)
                    display.scroll('Message added')
                    message_decripte_vigenere = vigenere(content,key,True) #Here we will decrypt the content of the message
                    return message_decripte_vigenere
                    
            if clef == '03' : 
                nonce_decrypted = vigenere(nonce,key,True)
                if nonce_decrypted in dictionnary['03'] : 
                    display.scroll('ERROR message already received')
                else : 
                    dictionnary['03'].append(nonce_decrypted)
                    display.scroll('Message added')
                    message_decripte_vigenere = vigenere(content,key,True) #Here we will decrypt the content of the message
                    return message_decripte_vigenere

def establish_connexion(key): 
    global nbre_alea 
    global content
    display.scroll("Connexion ...")
    content= random.randrange(5000)
    nbre_alea = random.randrange(5000)
    nbre_alea_crypted = vigenere(nbre_alea,key)
    message_a_decrypter = vigenere(content,key)
    encrypted_message = nbre_alea_crypted + ':' + message_a_decrypter
    len_message = len(encrypted_message)
    radio_send = '{0}|{1}|{2}'.format('00',str(len_message),encrypted_message)
    radio.send(radio_send)
    return 

def send_message (type_message,contenu,key): 
    contenu_vigenered = vigenere(contenu,key)
    nbre_aleatoire = random.randrange(5000)
    encrypted_message = str(nbre_aleatoire) + ':' + contenu_vigenered
    long_message = len(encrypted_message)
    radio_send = '{0}|{1}|{2}'.format(type_message,str(long_message),encrypted_message)
    display.scroll(radio_send,300)
    radio.send(radio_send)

def calcul_response (message) :
    global key
    global content
    message_deballe = unpack_data(message,key)
    answer_challenge = content *5
    hashing_value_challenge = hashing(str(answer_challenge)) 
    if message_deballe == str(hashing_value_challenge) :
        display.scroll("Clef authentifiée")
        key += str(answer_challenge)
        display.scroll(key)
        
display.scroll('Welcome')
if __name__ == '__main__' :
    radio_message = menu()
    if radio_message : 
        message_recu = unpack_data(radio_message,key)

    
    
        
