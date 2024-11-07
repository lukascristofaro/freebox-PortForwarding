#!/bin/bash

REPO_URL="https://github.com/lukascristofaro/freebox-PortForwarding"
INSTALL_DIR="/usr/local/bin"
LATEST_RELEASE_API="https://api.github.com/repos/lukascristofaro/freebox-PortForwarding/releases/latest"

# Vérifie si l'utilisateur a les privilèges root
if [ "$EUID" -ne 0 ]
  then echo "Veuillez exécuter ce script en tant qu'administrateur (utilisez sudo)"
  exit
fi

apt-get update

# Vérifie si cURL ou wget est installé pour télécharger des fichiers
if ! command -v curl &> /dev/null
then
    echo "Veuillez installer cURL pour télécharger les fichiers."
    exit
fi

# Récupère la dernière version depuis GitHub
echo "Vérification de la dernière version..."

LATEST_VERSION=$(curl -s $LATEST_RELEASE_API | grep -oP '"tag_name": "\K(.*)(?=")')

# Télécharge la dernière version
DOWNLOAD_URL="$REPO_URL/releases/download/$LATEST_VERSION/fbpf"
echo "Téléchargement de la version $LATEST_VERSION..."
if command -v curl &> /dev/null
then
    curl -L $DOWNLOAD_URL -o $INSTALL_DIR/fbpf
else
    wget $DOWNLOAD_URL -O $INSTALL_DIR/fbpf
fi

# Met à jour les permissions
chmod +x $INSTALL_DIR/fbpf


# Installation de jq si non présent
if ! command -v jq &> /dev/null; then
    echo "Installation de jq..."
    apt-get update
    apt-get install -y jq
fi

# Configuration des variables
URL_FREEBOX="http://mafreebox.freebox.fr"
APP_ID="org.cristofaro.fbpf"
APP_NAME="freebox-PortForwarding"
APP_VERSION="1.0.0"
APP_DEVICE_NAME=$(hostname)

# Vérification de la disponibilité de l'API de la Freebox
if ! curl -s --head "$URL_FREEBOX" | grep "200 OK" > /dev/null; then
    echo "Erreur : Impossible de se connecter à la Freebox à l'adresse $URL_FREEBOX"
    exit 1
fi

# Récupération de la version de l'API
API_VERSION=$(curl -s -X GET "$URL_FREEBOX/api_version" | jq -r '.api_version')
if [ -z "$API_VERSION" ]; then
    echo "Erreur : Impossible de récupérer la version de l'API de la Freebox."
    exit 1
fi
echo "API version : $API_VERSION"

API_MAJOR_VERSION=$(echo "$API_VERSION" | cut -d '.' -f 1)

echo "API major version : $API_MAJOR_VERSION"

# Demande d'autorisation et récupération du token de l'application
RESPONSE=$(curl -X POST "$URL_FREEBOX/api/v$API_MAJOR_VERSION/login/authorize/" \
    -H "Content-Type: application/json" \
    -d "{\"app_id\":\"$APP_ID\", \"app_name\":\"$APP_NAME\", \"app_version\":\"$APP_VERSION\", \"device_name\":\"$APP_DEVICE_NAME\"}")

echo $RESPONSE

TRACK_ID=$(echo $RESPONSE | jq -r '.result.track_id')
echo "Track ID : $TRACK_ID"

AUTH=true

echo "En attente de validation de l'application sur la Freebox"

while [ "$AUTH" = true ]; do
    CHALLENGE=$(curl -s -X GET "$URL_FREEBOX/api/v$API_MAJOR_VERSION/login/authorize/$TRACK_ID")
    STATUS=$(echo $CHALLENGE | jq -r '.result.status')
    if [ "$STATUS" = 'pending' ]; then
        sleep 5
    elif [ "$STATUS" = 'granted' ]; then
        echo "Application validée"
        echo "Token de l'application : $APP_TOKEN"
        AUTH=false
    else
        echo "Erreur : $STATUS"
        exit 1
    fi
done

cat <<EOF> /etc/freebox-port-forwarding.conf
URL_FREEBOX=$URL_FREEBOX
APP_ID=$APP_ID
APP_NAME=$APP_NAME
APP_VERSION=$APP_VERSION
APP_DEVICE_NAME=$APP_DEVICE_NAME
API_VERSION=$API_VERSION
API_MAJOR_VERSION=$API_MAJOR_VERSION
TRACK_ID=$TRACK_ID
APP_TOKEN=$APP_TOKEN
EOF


echo "Installatio terminée ! Utilisez 'fbpf' pour lancer le programme."