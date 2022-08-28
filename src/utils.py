import numpy as np
import pandas as pd

import os
import unidecode

INPUT_FOLDER = 'input'
OUTPUT_FOLDER = 'output'
COLUMNS = ['SOCIETE', 'ADRESSE', 'CP', 'VILLE', 'TEL', 'MAIL']
COLUMN_FILIERE = 'FILIERE'
COLUMNS_OUTPUT = ['Titre', 'Téléphone', 'Email', 'Adresse']

def get_one_xls_file(folder):
    """
    Retourne le nom du fichier XLS du dossier.
    """
    xls_files = []
    try:
        for file in os.listdir(folder):
            # Si le fichier est un fichier XLS
            if file.endswith('.xls') or file.endswith('.xlsx'):
                # On l'ajoute à la liste
                xls_files.append(os.path.join(folder, file))

    except FileNotFoundError:
        print('ERROR: Le dossier input n\'existe pas')
        exit()

    # Il ne doit y avoir qu'un seul document XLS dans le dossier input
    if len(xls_files) > 1:
        print('ERROR: Il y a plus d\'un fichier XLS dans le dossier input')
        exit()


    return xls_files[0]


def xls_to_csv(input_file, output_file):
    """
    Convertit le fichier XLS en CSV.
    """
    read_file = pd.read_excel(input_file)
    read_file.to_csv(output_file, index=False)

def filter_columns(data):
    """
    Filtre les colonnes du fichier CSV.
    Dès que la colonne filière est repérée, on garde les colonnes suivantes, jusqu'a la prochaine colonne nommée.
    """
    mode_filiere = True
    for column in data.columns:
        column_name = unidecode.unidecode(column).upper()

        if mode_filiere and column_name[:8] != "UNNAMED:" and column_name != COLUMN_FILIERE: #On arrive à la fin des colonnes de filières
            mode_filiere = False

        #Si on arrive à la première des colonnes des filières, on enregistre la suite
        if column_name == COLUMN_FILIERE:
            mode_filiere = True

        if mode_filiere: #On change le nom de la colonne par le nom dans la première ligne
            new_name =  data[column].iloc[0]
            if pd.isna(new_name):
                data.drop(column, axis=1, inplace=True)
            else:    
                data.rename(columns={column: new_name}, inplace=True) 

        if not mode_filiere and column_name not in COLUMNS: #On supprime les colonnes inutiles
            data.drop(column, axis=1, inplace=True)

    new_names = {}
    for column in data.columns:
        new_names[column] = unidecode.unidecode(column).upper().replace(' ', '')

    data.rename(columns=new_names, inplace=True)

    return data

def format_data(data):
    """
    On formatte les données :
    - On supprime les lignes vides
    - On crée les attributs : title, description, ADRESSEe
    - On met des booléens pour les filières 
    """

    #On enlève les nan
    for column in data.columns:
        data[column] = data[column].astype(str)
        data[column] = data[column].replace('nan', '', regex=True)


    #On supprime la première ligne
    data = data.iloc[1: , :]
    #On supprime les sociétés non renseignées
    data = data[data['SOCIETE'].notna()]


    #FILIERE
    for column in [c for c in data.columns if c not in COLUMNS]:
        data[column] = np.where(data[column] == '', False, True)

    #On crée les attributs title, description, ADRESSEe
    #Title
    data['Titre'] = data['SOCIETE'].str.upper()

    #ADDRESE
    data['Adresse'] = data['ADRESSE'].str.capitalize() if data['ADRESSE'].str != '' else ''
    data['Adresse'] = data['Adresse'] + ' ' + data['CP'] if data['CP'].str != '' else ''
    data['Adresse'] = data['Adresse'] + ' ' + data['VILLE'].str.capitalize() if data['VILLE'].str != '' else ''

    #DESCRIPTION
    data['Téléphone'] = data['TEL'].str.replace(r',', ' ',regex=True)
    data['Téléphone'] = data['Téléphone'].str.replace(r'.', ' ', regex=True)
    data['Email'] = data['MAIL'].str.lower().replace(r' ', '', regex=True)

    data.drop(COLUMNS, axis=1, inplace=True)
    
    return data

def create_csv_filiere(data, file_name):
    """
    Crée un fichier csv par filiere.
    """
    data.to_csv(file_name, index=False, sep=',')