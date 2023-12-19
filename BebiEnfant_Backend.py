#Backend
#Je t'aime Alistaire
# BeTag des enfants qui doit povoir communiquer avec celui des parents
from microbit import *
import radio
import random
radio.config(group=23)
radio.on()

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

def receive_packet (key,message) : 
    """
    @pre : A reçu un message sous vigenere
    @post : Decripte le message et l'affiche
    """
    message_recu_decryption = vigenere(message,key, True)
    display.scroll(message_recu_decryption)
    return message_recu_decryption

def connexion_establishment (key,message) : 
    """
    @pre : A reçu un message
    @post : Décripte le message et réalise le calcul pour la connexion a établir
            Renvoie la réponse au challenge au BeTag parent sous forme hashé
            Mets à jour la clef pour décrypter
    """
    message_connexion = receive_packet(key,message)
    calcul = calcul_challenge(message_connexion)
    calcul_to_str = str(calcul)
    message_hashe = hashing(calcul_to_str)
    key += calcul_to_str
    return send_message('00',key,message_hashe)
    
def calcul_challenge(message) :
    """
    @Pre : A recu un message qui est décrypte
    @Post : Renvoie la réponse au calcul
    """
    calcul_to_do = int(message)*5
    return calcul_to_do

def send_message (type_message,key,message) :
    """
    @Pre : Un message en clair 
    @Post : Renvoie un message sous le format spécifié en crypte 
    """
    nbre_aleatoire_message = random.randrange(5000)
    nbre_aleatoire_cryption = vigenere(nbre_aleatoire_message,key)
    message_cryption = vigenere(message,key)
    message_complet = nbre_aleatoire_cryption + ":" + message_cryption
    longueur_message_complet = len(message_complet)
    message_radio_complet = "{0}|{1}|{2}".format(type_message,longueur_message_complet,message_complet)
    display.scroll(message_radio_complet)
    return radio.send(message_radio_complet)

def message_recu_radio (key,message,dictionnaire) : 
    """
    @Pre : message = radio.receive() 
           Recoit un message via la radio mais le message est du type Type|Longueur|Contenu
           dictionnaire à disposition pour pouvoir ranger les différents messages dedans 
    @Post : Réalise les différentes méthodes en fonction du type de message reçu

    Le BeTag de l'enfant doit pouvoir recevoir : 
    1) La connexion 
    2) Le MilkCount 

    Le BeTag doit pouvoir envoyer : 
    1) L'état d'éveil
    2) La température
    """
    global MILK_COUNT
    message_separe = message.split("|") #Va créer une liste qui contient 3 positions 
    message_separe_tuple = tuple(message_separe)
    type,longueur,contenu = message_separe_tuple
    contenu_separe = contenu.split(":") #Va créer une liste qui contient 2 positions
    contenu_separe_tuple = tuple(contenu_separe)
    nonce,message_en_vigenere = contenu_separe_tuple
    if type == "00" : 
        if nonce not in dictionnaire["00"] : #Permet de vérifier si on a déjà reçu ce message
            dictionnaire["00"].append(nonce)
            display.scroll("Message added to first dictionnary ")
            connexion_establishment(key,message_en_vigenere) #Fais l'ensemble des instructions pour la connexion
        else : 
            display.scroll("Message already received")
    if type == "01" :
        if nonce not in dictionnaire["01"] : #Permet de vérifier si on a déjà reçu ce message
            dictionnaire["00"].append(nonce)
            display.scroll("Message added to second dictionnary ",50)
            receive_packet(key,message_en_vigenere) #Decrypte le message et le retourne
            MILK_COUNT = receive_packet(key,message_en_vigenere) #Permet de modifier la valeur de milk_count
            display.scroll(MILK_COUNT)
        else : 
            display.scroll("Message already received")

def veilleuse (key) : 
    """
    @Pre : Doit recevoir une commande de la part du BeTag parent qui lui dit que le bébé a été mis au lit
           Si elle reçoit un 'start_veilleuse' elle doit rester allumer tant que la lumière n'est pas 
           au-delà de 80. 
           Dès que la lumière est-au delà de 80 la veilleuse s'éteint
    @Post : Doit s'allumer à partir d'une certaine luminosité 
            Doit s'éteindre dès que la luminosité est assez importante 
    """
    
    display.read_light_level()
    if display.read_light_level() <= 50:
        display.show(Image(
        "99999:"
        "99999:"
        "99999:"
        "99999:"
        "99999"))
        temperature_measurement(key)
        agitation_bebe(key)
            
    elif 50 < display.read_light_level() <= 90 :
        """
        Il faudra vérifier une luminosité qui empêche les bébés de dormir
        """

        temperature_measurement(key)
        agitation_bebe(key)
    else : 
        temperature_measurement(key)
        agitation_bebe(key)

def temperature_measurement (key,type='02') : 
    """
    @Pre : Rien
    @Post : Mesure la température ambiante et envoie un message au BeTag parent uniquement en cas d'urgence
            Càd en cas de dépassement de la température seuille
    """
    if temperature() < 19 : 
        send_message(type,key,"Need heat")
        display.scroll('Need heat')
    elif temperature() > 25 :
        send_message(type,key,'Need to cool down the room')
        display.scroll('Need to cool down')

def agitation_bebe (key,type='03') : 
    
    if 45 < microphone.sound_level() < 60: 
        send_message(type,key,'Bebe peut etre reveille et agite')
    elif microphone.sound_level() > 60 : 
        send_message(type,key,'Bebe reveille')

if __name__ == '__main__' :
    """
    @Pre : Doit pouvoir recevoir des messages radios 
            Doit initialiser le dictionnaire 
            Doit initialiser les valeurs de milk_count, de la key
    """
    key = "Betag"
    MILK_COUNT = 0
    dictionnaire = {}
    lst = ['00','01']
    for element in lst : 
        dictionnaire[element] = []
    """
    message_parent = "01|24|740:9"
    if message_parent : 
        message_recu_radio(key,message_parent,dictionnaire)
    elif button_a.was_pressed() : 
        display.scroll(MILK_COUNT)

    CA c'est si vous voulez testez sans les microbit avec juste l'interface simulateur
    """
    while True : 
        radio.receive()
        if radio.receive() :
            message_recu_radio(key,radio.receive(),dictionnaire)
        elif button_a.was_pressed() : 
            display.scroll(MILK_COUNT)
        else : 
            veilleuse(key)
    
        
        
            


    
    
        
