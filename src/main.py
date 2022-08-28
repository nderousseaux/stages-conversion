from utils import *

def xls_files_to_csv(input_folder):
    """
    Première étape de notre programme : Convertir le fichier XLS dans le dossier input en CSV
    """

    #On récupère le fichier XLS du dossier input
    xls_file = get_one_xls_file(input_folder)

    # On convertit le fichier XLS en CSV

    output_file = os.path.join(input_folder, 'data.csv')

    xls_to_csv(xls_file, output_file)
    
    return output_file


def convert_csv_to_csv_filiere(data_file, output_folder):
    """
    Deuxième étape de notre programme : Convertir le fichier CSV en plusieurs fichiers CSV par filière
    Il y aura un fichier csv par filière. Au format `nom-filiere.csv`
    """

    data = pd.read_csv(data_file)

    # On filtre les colonnes
    data = filter_columns(data)

    #On formatte les données
    data = format_data(data)

    #On crée un fichier csv par filière
    for filiere in [c for c in data.columns if c not in COLUMNS_OUTPUT]:
        data_filiere = data[data[filiere] == True]
        data_filiere = data_filiere.drop(columns=[col for col in data_filiere if col not in COLUMNS_OUTPUT])
        create_csv_filiere(data_filiere, os.path.join(output_folder, filiere + '.csv'))

if __name__ == '__main__':
    
    #On convertit le fichier xls en csv
    data_file = xls_files_to_csv(INPUT_FOLDER)

    print('Conversion du fichier XLS en CSV terminée')

    #On convertit le fichier csv data en csv lisibles par google mymaps
    convert_csv_to_csv_filiere(data_file, OUTPUT_FOLDER)

    print('Conversion du fichier CSV terminée')
    print(f'Les fichiers de sortie sont disponibles dans le dossier {OUTPUT_FOLDER}')