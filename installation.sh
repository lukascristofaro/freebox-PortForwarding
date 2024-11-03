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



echo "Installatio terminée ! Utilisez 'fbpf' pour lancer le programme."