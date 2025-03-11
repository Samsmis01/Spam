import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from stem import Signal
from stem.control import Controller
import re

import subprocess
import os

# Fonction pour vérifier si Tor est installé et l'installer si nécessaire via Termux
def installer_tor():
    """Vérifie si Tor est installé et tente de l'installer si ce n'est pas le cas"""
    try:
        # Vérifier si Tor est installé sur Android via Termux
        tor_installed = subprocess.run(["which", "tor"], capture_output=True, text=True)
        
        if tor_installed.returncode != 0:  # Si Tor n'est pas installé
            print("Tor n'est pas installé. Installation en cours via Termux...")
            # Essayer d'installer Tor via Termux
            subprocess.run(["pkg", "update", "-y"], check=True)  # Mettre à jour les packages
            subprocess.run(["pkg", "install", "tor", "-y"], check=True)  # Installer Tor
            print("Tor a été installé avec succès.")
        else:
            print("Tor est déjà installé.")
    except Exception as e:
        print(f"❌ Erreur lors de l'installation de Tor : {e}")

# Fonction pour valider le numéro
def valider_numero(numero):
    """ Vérifie si le numéro est au format international (+XX...) """
    return bool(re.match(r"^\+\d{10,15}$", numero))

# Fonction pour démarrer Tor
def start_tor():
    """Démarre Tor en arrière-plan."""
    try:
        if not os.path.exists('/data/data/com.termux/files/usr/bin/tor'):
            print("❌ Tor n'est pas installé sur ce système.")
            return None
        tor_command = ['tor']
        tor_process = subprocess.Popen(tor_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Tor démarre...")
        time.sleep(10)  # Attendre quelques secondes pour permettre à Tor de démarrer
        return tor_process
    except Exception as e:
        print(f"❌ Erreur lors du démarrage de Tor : {e}")
        return None

# Fonction pour changer l'IP avec Tor
def changer_ip():
    """ Change l'IP via Tor en envoyant un signal de nouveau circuit """
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()  # Authentification sur le contrôleur Tor
            controller.signal(Signal.NEWNYM)  # Envoi du signal pour un nouveau circuit
        print("🌍 IP changée avec succès via Tor !")
    except Exception as e:
        print(f"❌ Erreur lors du changement d'IP : {e}")

# Fonction pour envoyer un SMS anonyme (sans numéro visible)
def envoyer_sms_anonyme(numero, message):
    """ Envoie un SMS via une API anonymisée (ex: Textbelt) """
    changer_ip()  # Change l'IP avant chaque requête

    url = "https://textbelt.com/text"  # URL de l'API de Textbelt
    params = {
        'phone': numero,
        'message': message,
        'key': 'textbelt',  # Utiliser la clé d'API gratuite ou premium de Textbelt
    }
    try:
        response = requests.post(url, data=params)
        if response.status_code == 200:
            print(f"✔ SMS envoyé avec succès!")
        else:
            print(f"❌ Échec de l'envoi du SMS: {response.text}")
    except Exception as e:
        print(f"❌ Échec de la requête SMS : {e}")

# Fonction pour envoyer un message via Gmail
def envoyer_email_gmail(to_email, subject, body, from_email, from_password):
    """ Envoie un email via Gmail """
    changer_ip()  # Change l'IP avant chaque requête

    try:
        # Configurer l'email
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Configurer le serveur SMTP Gmail
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(from_email, from_password)

        # Envoyer l'email
        server.sendmail(from_email, to_email, msg.as_string())
        server.close()

        print(f"✔ Email envoyé avec succès à {to_email}!")

    except Exception as e:
        print(f"❌ Échec de l'envoi de l'email : {e}")

# Fonction pour envoyer un message WhatsApp via Twilio
def envoyer_message_whatsapp(numero, message, sid, auth_token, from_number):
    """ Envoie un message via WhatsApp avec Twilio """
    client = Client(sid, auth_token)  # Créer une instance du client Twilio

    try:
        message = client.messages.create(
            body=message,
            from_=f'whatsapp:{from_number}',  # Numéro Twilio WhatsApp
            to=f'whatsapp:{numero}'  # Numéro du destinataire WhatsApp
        )
        print(f"✔ Message WhatsApp envoyé avec succès!")
    except Exception as e:
        print(f"❌ Échec de l'envoi du message WhatsApp : {e}")

# Fonction pour afficher le banner stylé
def banner():
    print("\033[1;36m")
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                            ║")
    print("║  ██╗  ██╗███████╗██╗  ██╗████████╗███████╗ ██████╗██╗  ██╗                ║")
    print("║  ██║  ██║██╔════╝╚██╗██╔╝╚══██╔══╝██╔════╝██╔════╝██║  ██║                ║")
    print("║  ███████║█████╗   ╚███╔╝    ██║   █████╗  ██║     ███████║                ║")
    print("║  ██╔══██║██╔══╝   ██╔██╗    ██║   ██╔══╝  ██║     ██╔══██║                ║")
    print("║  ██║  ██║███████╗██╔╝ ██╗   ██║   ███████╗╚██████╗██║  ██║                ║")
    print("║  ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝                ║")
    print("║                                                                            ║")
    print("╚══════════════════════════════════════════════════════════════════════════��═╝")
    print("\033[0m")

# Fonction pour afficher les informations de contact
def afficher_informations():
    print("\033[1;32m")
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                            ║")
    print("║  DÉVELOPPEUR : \033[1;36mHEXTECH \033[1;32m                                                ║")
    print("║  CANAL TÉLÉGRAM : \033[1;36mhttps://t.me/hextechcar \033[1;32m                             ║")
    print("║  INSTAGRAM : \033[1;36mSAMSMS01 \033[1;32m                                                ║")
    print("║  GITHUB : \033[1;36mSamsmis01 \033[1;32m                                                   ║")
    print("║                                                                            ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    print("\033[0m")

# Menu principal
def menu_principal():
    banner()
    afficher_informations()
    print("=" * 50)
    print("📲 SPAM SMS ANONYME, EMAIL ET WHATSAPP 📲")
    print("=" * 50)

    while True:
        choix = input("Choisissez une option (1.SPAL SMS Anonyme, 2. SPAM Email, 3. SPAM WhatsApp, 4. Quitter) : ")
        
        if choix == "1":
            # Vérifier si Tor est installé, sinon installer
            installer_tor()
            
            # Demander un numéro et un message pour envoyer un SMS
            while True:
                numero = input("Entrez le numéro de téléphone du destinataire (Format: +XX...): ").strip()
                if valider_numero(numero):
                    break
                print("❌ Numéro invalide. Essayez encore.")

            message = input("Entrez le message à envoyer : ").strip()
            repetitions = 1799  # Répéter l'envoi 5 fois

            print(f"\n📤 Envoi du message {repetitions} fois...\n")
            for i in range(repetitions):
                print(f"\n📝 Envoi n°{i+1} :")
                envoyer_sms_anonyme(numero, message)

        elif choix == "2":
            # Envoyer un email via Gmail
            to_email = input("Entrez l'adresse email du destinataire : ").strip()
            subject = input("Entrez le sujet de l'email : ").strip()
            body = input("Entrez le message à envoyer : ").strip()
            from_email = input("Entrez votre adresse Gmail : ").strip()
            from_password = input("Entrez votre mot de passe Gmail : ").strip()
            envoyer_email_gmail(to_email, subject, body, from_email, from_password)

        elif choix == "3":
            # Envoyer un message WhatsApp via Twilio
            numero = input("Entrez le numéro WhatsApp du destinataire (Format: +XX...): ").strip()
            message = input("Entrez le message à envoyer : ").strip()
            sid = input("Entrez votre SID Twilio : ").strip()
            auth_token = input("Entrez votre token d'authentification Twilio : ").strip()
            from_number = input("Entrez votre numéro Twilio (Format: +XX...): ").strip()
            envoyer_message_whatsapp(numero, message, sid, auth_token, from_number)

        elif choix == "4":
            print("Merci d'avoir utilisé HEXTECH ! À bientôt !")
            break

        else:
            print("❌ Option invalide. Veuillez choisir une option valide.")

# Point d'entrée du script
if __name__ == "__main__":
    menu_principal()