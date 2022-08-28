#!/bin/zsh
echo -e "[1/8]\tSuppression des éventuels fichiers précédents"
rm logs
rm output/* &>> logs
echo -e "[2/8]\tInstallation des dépendances principales"
python3 -m pip install --upgrade pip &>>  logs
python3 -m pip install --user virtualenv &>>  logs
echo -e "[3/8]\tInstallation de l'environnement virtuel..."
python3 -m virtualenv env &>>  logs
echo -e "[4/8]\tInstallation de l'environnement virtuel terminée. Activation de l'environnement..."
source env/bin/activate &>>  logs
echo -e "[5/8]\tEnvironnement activé. Installation des dépendances..."
env/bin/pip install -r requirements.txt &>>  logs
echo -e "[6/8]\tInstallation des dépendances terminée. Lancement de l'application..."
env/bin/python src/main.py | sed "s/^/...\t/" | tee -a logs
echo -e "[7/8]\tApplication terminée. Suppression de l'environnement virtuel..."
deactivate &>>  logs
rm -rf env/ &>>  logs
echo -e "[8/8]\tEnvironnement virtuel supprimé. Fin de l'exécution."