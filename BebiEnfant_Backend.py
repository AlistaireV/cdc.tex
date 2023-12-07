#Backend
# BeTag du bébé qui doit povoir communiquer avec celui des parents
from microbit import *
import radio
import random
radio.config(group=23)
radio.on()

key = "Betag"

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
    decryption_message = encrypted_packed.split('|')
    message_en_clair = decryption_message[2].split(':')
    encrypted_packet = tuple(message_en_clair)
    nonce,content,hashed_value = encrypted_packet
    dictionnary = {}
    lst = ['00','01','02','03']
    for element in lst : 
        dictionnary[element] = [] 
    if decryption_message[0] == '00' :
        for clef in dictionnary : 
            if clef == '00' : 
                if nonce in dictionnary['00'] : 
                    display.scroll('ERROR message already received')
                else : 
                    dictionnary['00'].append(nonce)
                    message_decripte_vigenere = vigenere(content,key,True) #Here we will decrypt the content of the message
                    hashing_value = hashing(message_decripte_vigenere)
                    if int(hashing_value) == int(hashed_value) :  
                        display.scroll("Excellent")
                        return message_decripte_vigenere


def calculate_challenge (challenge) : 
    return int(challenge)*5

def send_packet(type_message,contenu,key): 
    display.scroll(contenu,300)
    contenu_vigenered = vigenere(contenu,key)
    nbre_aleatoire = random.randrange(5000)
    encrypted_message = str(nbre_aleatoire) + ':' + contenu_vigenered + ':' +str(hashing(str(contenu)))
    long_message = len(encrypted_message)
    radio_send = '{0}|{1}|{2}'.format(type_message,str(long_message),encrypted_message)
    display.scroll(radio_send,300)
    radio.send(radio_send)

def establishment_connexion (message) :
    global key
    if message : 
            message_code = unpack_data(message,key)
            response_challenge = calculate_challenge(message_code)
            display.scroll(response_challenge,300)
            send_packet("00",response_challenge,key)
        
display.scroll('Welcome')
if __name__ == '__main__' : 
    while True : 
        message = radio.receive()
        establishment_connexion(message)
        