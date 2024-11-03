#!/bin/bash

# Vérification des droits administrateur
if [[ $EUID -ne 0 ]]; then
   echo "Ce script doit être exécuté en tant qu'administrateur. Utilisez sudo." 
   exit 1
fi

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
    echo $CHALLENGE
    STATUS=$(echo $CHALLENGE | jq -r '.result.status')
    if [ "$STATUS" = 'pending' ]; then
        sleep 5
    elif [ "$STATUS" = 'granted' ]; then
        echo "Application validée"
        APP_TOKEN=$(echo $CHALLENGE | jq -r '.result.app_token')
        echo "Token de l'application : $APP_TOKEN"
        AUTH=false
    else
        echo "Erreur : $STATUS"
        exit 1
    fi
done

