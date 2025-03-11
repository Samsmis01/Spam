HEXTECH Spam Tool

HEXTECH Spam Tool est un script polyvalent conçu pour effectuer des tests de sécurité et des envois automatisés de messages (SMS, emails, WhatsApp) à des fins éducatives. Il est optimisé pour fonctionner sous Termux sur les appareils Android.

⚠️ Avertissement

Ce script est destiné uniquement à des fins éducatives et de test. L'utilisation de cet outil pour des activités illégales ou sans le consentement explicite des destinataires est strictement interdite. Les auteurs déclinent toute responsabilité en cas d'utilisation abusive.

📋 Fonctionnalités

Envoi de SMS anonymes via des services tiers.

Envoi d'emails en utilisant des comptes Gmail.

Envoi de messages WhatsApp en utilisant l'API de Twilio.

Changement d'adresse IP en utilisant le réseau Tor pour anonymiser les requêtes.


🛠️ Installation

Pré-requis

Termux installé sur votre appareil Android.

Connexion Internet active.


Étapes d'installation

1. Cloner le dépôt :

git clone https://github.com/Samsmis01/Spam.git





2. Accéder au répertoire du script :

cd Spam





3. Donner les permissions d'exécution au script :

chmod +x hextech_spam.py





4. Installer les dépendances requises :

pip install -r requirements.txt





🚀 Utilisation

1. Lancer le script :

python hextech_spam.py





2. Naviguer dans le menu principal pour choisir l'action souhaitée :

Envoi de SMS anonyme

Envoi d'email

Envoi de message WhatsApp

Quitter



3. Suivre les instructions à l'écran pour fournir les informations nécessaires (numéro de téléphone, message, identifiants, etc.).



📝 Notes

Assurez-vous que Tor est installé sur votre appareil pour utiliser les fonctionnalités d'anonymisation. Le script tentera de l'installer automatiquement si nécessaire.

Pour l'envoi d'emails via Gmail, il est recommandé d'utiliser un mot de passe d'application pour des raisons de sécurité.

L'utilisation de l'API Twilio pour WhatsApp nécessite des identifiants valides (SID, token d'authentification) et une configuration préalable sur la plateforme Twilio.


📞 Contact

Développeur : HEXTECH

Canal Telegram : https://t.me/hextechcar

Instagram : SAMSMS01

GitHub : Samsmis01
