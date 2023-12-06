#Backend
# BeTag du bébé qui doit povoir communiquer avec celui des parents
from microbit import *
import radio
import random
radio.config(group=23)
radio.on()
import log 

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

def send_packet(key, type, content):
    """
    Envoie de données fournie en paramètres
    Cette fonction permet de construire, de chiffrer puis d'envoyer un paquet via l'interface radio du micro:bit

    :param (str) key:       Clé de chiffrement
           (str) type:      Type du paquet à envoyer  
           (str) content:   Données à envoyer
	:return none
    
    messsage_to_send = vigenere(content,key) #We code the message we want to send in Vigenere form
    value_message = hashing(content) #Here we'll hash the message we want to send and it will give use a number
    radio.send(type+"|"+len(messsage_to_send)+"|"messsage_to_send) #Envoie du message crypté avec le numéro de hashing à la fin 
    """
    hashed_message = hash(content) #We'll assign a value of hashing to the message to send
    random_number = random.randrange(50000) #Choose a random number which will be directly associated with the message to send 
    encrypted_message = str(random_number) + ' : ' + vigenere(content,key) + ' : ' + str(hashed_message) #The message we'll send is containing the message under a vigenere form + the value of hashing associated with 
    # the bright message 
    len_message = len(encrypted_message) #Calculate the length of the message 
    message_to_send = '{0} | {1} | {2}'.format(type,len_message,encrypted_message) # 'str type' of the message to send

    radio.send(message_to_send)

#Decrypt and unpack the packet received and return the fields value
def unpack_data(encrypted_packet, key):
    """
    Déballe et déchiffre les paquets reçus via l'interface radio du micro:bit
    Cette fonction renvoit les différents champs du message passé en paramètre

    :param (str) encrypted_packet: Paquet reçu
           (str) key:              Clé de chiffrement
	:return (srt)type:             Type de paquet
            (int)lenght:           Longueur de la donnée en caractères
            (str) message:         Données reçues
    
    if encrypted_packet : 
        encrypted_packet.split('|') #Comme dans le message crypté envoyé on a mis un séparateur, on va pouvoir séparer
        #notre message en deux et donc avoir une variable encrypted_message du style ['message en vigenere','valeurassocié'] 
        if encrypted_packet[0] == '01' :
            vigenere(encrypted_packet[1],key)

        elif encrypted_packet[0] == '02' : 
        elif encrypted_packet[0] == '03'
    """
    encrypted_packet = encrypted_packet.split(' | ') #Va permettre de créer une liste de longueur 3 qui contiendra en position 0 'le type' en position '1' la longueur et en position '2' le content 
    encrypted_packet = tuple(encrypted_packet)
    type_message,len_message,content = encrypted_packet
    content = content.split(' : ')
    """
    En splittant la partie content avec les ' : ' ca va permettre d'avoir 
    1) l'ID du message (un random number)
    2) Le message en lui-même
    3) La valeur sous forme d'int du hashing que l'on pourra comparer à celle obtenue après décodage 
    """

    dictionnary = {}
    lst = ['00','01','02','03']
    for element in lst : 
        dictionnary[element] = [] 
    if type_message == '00' :
        display.scroll('New connexion') #Le type 00 fera d'office référence à une nouvelle connexion
        for key in dictionnary : 
            if key == '00' : 
                if content[0] in dictionnary['00'] : 
                    display.scroll('ERROR message already received')
                else : 
                    dictionnary['00'].append(content[0])
        decrypted_message = vigenere(content[1],key,True) #Here we will decrypt the content of the message
        hashing_value = hashing(decrypted_message)
        if hashing_value != content[2] : 
             display.scroll("Invalid Message")

        return decrypted_message

    elif type_message == '01' :
        display.scroll('Milk count') #Le type 01 fera directement référence au compteur de lait
        for key in dictionnary : 
            if key == '01' : 
                if content[0] in dictionnary['01'] : 
                    display.scroll('ERROR message already received')
                else : 
                    dictionnary['01'].append(content[0])
        decrypted_message= vigenere(content[1],key,True) #Here we will decrypt the content of the message 
        hashing_value = hashing(decrypted_message)
        if hashing_value != content[2] : 
             display.scroll("Invalid Message")

        return decrypted_message
    
    elif type_message == '02' :
        display.scroll('Temp measure') #Le type 02 fera référence aux mesures de températures en continues
        for key in dictionnary : 
            if key == '02' : 
                if content[0] in dictionnary['02'] : 
                    display.scroll('ERROR message already received')
                else : 
                    dictionnary['02'].append(content[0])
        decrypted_message = vigenere(content[1],key,True) #Here we will decrypt the content of the message
        hashing_value = hashing(decrypted_message)
        if hashing_value != content[2] : 
             display.scroll("Invalid Message")

        return decrypted_message

    elif type_message == '03' :
        display.scroll('Sommeil agité') #Le type 03 devra toujours être relié à la fonction d'éveil du bébé
        for key in dictionnary : 
            if key == '03' : 
                if content[0] in dictionnary['03'] : 
                    display.scroll('ERROR message already received')
                else : 
                    dictionnary['03'].append(content[0])
        decrypted_message = vigenere(content[1],key,True) #Here we will decrypt the content of the message
        hashing_value = hashing(decrypted_message)
        if hashing_value != content[2] : 
             display.scroll("Invalid Message")

        return decrypted_message 
      
#Unpack the packet, check the validity and return the type, length and content
def receive_packet(packet_received, key):
    """
    Traite les paquets reçue via l'interface radio du micro:bit
    Cette fonction permet de construire, de chiffrer puis d'envoyer un paquet via l'interface radio du micro:bit
    Si une erreur survient, les 3 champs sont retournés vides

    :param (str) packet_received: Paquet reçue
           (str) key:              Clé de chiffrement
	:return (srt)type:             Type de paquet
            (int)lenght:           Longueur de la donnée en caractère
            (str) message:         Données reçue
    """
    unpack_data(packet_received,key)

    
#Calculate the challenge response
def calculate_challenge_response(challenge):
    """
    Calcule la réponse au challenge initial de connection avec l'autre micro:bit

    :param (str) challenge:            Challenge reçu
	:return (srt)challenge_response:   Réponse au challenge
    """
    #challenge = Ici c'est pour répondre au challenge de connexion. 
    #Le message recu va être du type '00 | longueur | nbre_aleatoire : nombre_aléatoire"
    #1) Il faut utiliser vigenere pour décrypter le second nombre_aleatoire
    # Avant d'utiliser cette fonction il y aura déjà eu un unpack_data()
    return int(challenge)**(0.5)+5
    

#Ask for a new connection with a micro:bit of the same group
def establish_connexion():
    global key
    while True : 
        radio_answer = radio.receive()
        if radio_answer :
            decryption_message = unpack_data(radio_answer,key)
            challenge_calcul = decryption_message
            answer  = calculate_challenge_response(challenge_calcul)
            send_packet(key,'00',answer)
            key += str(answer)
            global key

if __name__ == '__main__' :
     establish_connexion()