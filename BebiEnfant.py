# BeTag du bébé qui doit povoir communiquer avec celui des parents
from microbit import *
import radio

radio.config(group=23)
radio.on()
import log 

"""
Fonctionnalités : 
1) Veilleuse : 
Questions : 
- Quand est-ce que la fonction est utilisée ? 
    - Dès que le bébé va être mis dans son lit. La veilleuse n'étant pas utile quand il est réveillé
    - Ca offre plus de flexibilité utilisateur en plus 

2) Mesure de température de la pièce : 
Questions : 
- Quand est-ce que la fonction est utilisée ? 
    - Globalement tout le temps 
    - Comme il n'y a pas de timer implanté directement dant le microbit, comment faire pour mesurer à intervalle
    "régulier" ? 
        - Création d'un timer 
        - Faire une mesure dès qu'une autre fonctionnalité est utilisée 
        - Etre capable de mesurer via une demande du BeTag Parent 

3) Giroscope avec fonctionnalité de détection d'état d'éveil du bébé : 


4) Recording de l'ensemble des données 
Questions : 
- Est-ce que l'ensemble des données sont envoyées au BeTag parent ? 
Avantage de cet envoi: 
    - Le BeTag enfant pourra rester opérationnel et les parents pourront consulter les données "à distance"
    - La consultation des données du BeTag enfant n'empêche pas de continuer le recording et les alertes continueront
    à être émises. 
"""

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

        calculate_challenge_response(int(decrypted_message))

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
def establish_connexion(key):
    """
    Etablissement de la connexion avec l'autre micro:bit
    Si il y a une erreur, la valeur de retour est vide

    :param (str) key:                  Clé de chiffrement
	:return (srt)challenge_response:   Réponse au challenge
     
     Etapes à suivre : 
     1) Le BeTag va envoyer un random number codé sous vigenere 
     2) Sous quelle forme ? Type | Longueur | Nonce : Message 
     3) L'autre Tag reçoit
     4) Entre-temps le BeTag qui envoie la connexion il calcule pour le challenge 
     5) Il reçoit la notif de réponse sous vigenere de 'lautre BeTag 
     6) Si la réponse est ok alors le mot de passe devient password+random number et la co est établi
    """
    nbre_aleatoire = random.randrange(50000)
    send_packet(key,'00',nbre_aleatoire)
    answer = calculate_challenge_response(nbre_aleatoire)
    radio_answer = radio.receive()
    if radio_answer :
        decryption_message = unpack_data(radio_answer,key)
        if int(decryption_message) == answer :
             display.scroll('Connexion established')
             key = key

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

def menu(key):
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
             establish_connexion(key)

def setting(key):
     """Cette fonction permet de faire un choix de la fonnction 
        Cette fonction permet de faire un choix entre toutes le fonctions du tag 
        pré: un appel grace au button du menu 
        post: affiche des chiffres pour sélectionner la fonctionalité 
    """
     display.scroll(" choose your function ") 
     global SET_COUNT 
     display.show(SET_COUNT)
     while True :
        # il faudrait ajouter un 'if radio.receive() == "Start Veilleuse"  ou un truc du style
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
                temperature()
            elif SET_COUNT == 2:
                 dictionnaire_veilleuse["Allumage"] = 'Start'
                 veilleuse(key)
            #elif SET_COUNT == 3:
            #log_data()
            # Pour moi le log_data() doit apparaitre à tout moment. Les infos vont s'envoyer de manière constance
            # ou alors le SET_COUNT == 3 doit permettre d'envoyer le data_log
        
def log_data():
    #Objectifs : stockage de données récupérables par l'utilisateur
    log.add({
      'Temperature': temperature(),
      'Heure': time_secondes
      'Light': read_light_level()
    })


def calibration():
    display.scroll(compass.heading())
    compass.calibrate()
    if compass.is_calibrated() == True : 
        orientation1 = compass.heading()
        sleep(12000)
        orientation2 = compass.heading()
        gap = abs(orientation2-orientation1)
        if gap <= 15:
            radio.send('Endormie')
        elif gap <= 45:
            radio.send('Agite')
        else:
            radio.send('Tres agite')
        orientation3 = compass.heading()
        if orientation3 == 180: 
            radio.send('Changer la position')
    else : 
        compass.clear_calibration()

def veilleuse (key) : 
    """
    @Pre : Doit recevoir une commande de la part du BeTag parent qui lui dit que le bébé a été mis au lit
           Si elle reçoit un 'start_veilleuse' elle doit rester allumer tant que la lumière n'est pas 
           au-delà de 80. 
           Dès que la lumière est-au delà de 80 la veilleuse s'éteint
    @Post : Doit s'allumer à partir d'une certaine luminosité 
            Doit s'éteindre dès que la luminosité est assez importante 
    """
    if dictionnaire_veilleuse["Allumage"] != None :
        show_light(key)


def show_light (key) :
    light_level = display.read_light_level()
    if light_level <= 50:
        display.scroll('Activate Stitch',100)
        display.show(Image.DUCK)
        temperature(key)
    elif 50 > light_level =< 90 :
        """
        Il faudra vérifier une luminosité qui empêche les bébés de dormir
        """
        display.scroll('Deactivate Stitch',100)
        display.show(Image.DUCK)
        temperature(key)

    else : 
        dictionnaire_veilleuse["Allumage"] = None
        temperature(key)
 
        #display.scroll('Light level:',100)
        #display.scroll(light_level,100)
        #On peut laisser les deux lignes si vous voulez mais je pense pas que ca intéressera le bébé
        #Par contre ces données peuven têtre envoyé sur le data logger s'il faut

def temperature (key,type='02') : 
    """
    Cette fonctionnalité pourrait être intéressante dans la fonctionnalité de mesure de luminosité 
    car c'est pendant que le bébé dort que la température est le paramètre important à surveiller
    MAIS 
    Il faut une récurrence de mesure 
    @Pre : Ne s'active que lorsque le bébé est en phase de dodo
    @Post : Va mesurer la température et utiliser le codage selon Vigenere pour envoyer des données
    au BeTag parent 
    """
    measure_temperautre = temperature()
    if measure_temperautre <= 19 :
        send_packet(key, type, str(measure_temperature)+'- Need heat') #Utilisation def send_packet pour envoie
        #de données cryptées 
    elif measure_temperautre >= 25 :
        send_packet(key, type, str(measure_temperature)+'- Need cold') #Utilisation def send_packet pour envoie
        #de données cryptées

"""
PARTIE KAAN-ALISTAIRE AVANT RESTRUCTURATION DU CODE

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

time_secondes = 0
while True :
    data_monitoring = log_data()
    sleep(1000)
    time_secondes +=1
    alerte_temperature = temperature_alert()

def temperature_alert() :
    #Objectifs : Mesure de température 1X/h pour vérifier la température de la pièce du bébé 
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

"""