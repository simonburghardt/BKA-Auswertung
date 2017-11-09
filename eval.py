import csv
import operator
import os
import time

data_list = []  # Liste der Datensatz-Dictionaries
header = []  # Liste der Feldnamen
csv_file = 'data/data.csv'  # Dateipfad der auszuwertenden Dateien
output_folder = 'output/'

operators = {'>': operator.gt,
             '<': operator.lt,
             '>=': operator.ge,
             '<=': operator.le,
             '=': operator.eq}


def load_list():
    # Läd die Datei und speichert den Inhalt in data list und die Feldnamen in Header
    global data_list, header

    with open(csv_file, "r+", encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            data_list.append(row)
        header = reader.fieldnames
        # Funktioniert aktuell nur mit modifizierter Datei
    print("Daten geladen!")
    return True


def save_list(save_data_list, filename):
    # user_input = input("Soll die Liste '" + csv_file + "' wirklich gespeichert werden? \'Ja\' zur Bestätigung eingeben")
    # if user_input == "" or not (user_input[0].upper() == 'J'):
    #     print("Keine Liste gespeichert!")
    #     return False

    if not os.path.exists(output_folder):
        # creates output folder if it doesnt exist
        os.makedirs(output_folder)
    with open(output_folder + filename, "w+", encoding='utf-8') as f:
        writer = csv.DictWriter(f, header, delimiter=';', lineterminator='\n')
        writer.writeheader()
        writer.writerows(save_data_list)
    print("Datensätze gespeichert!")
    return True


def search_for_value(search_data_list, key, operator_string, value):
    return_list = []
    op = operators[operator_string]
    for data in search_data_list:
        if op(float(data[key]), value):
            return_list.append(data)
    return return_list


def search_for_string(search_data_list, key, value):
    return_list = []
    for data in search_data_list:
        if data[key] == value:
            return_list.append(data)
    return return_list


def timestring():
    # used for creating unique files
    return str(time.time())


load_list()
print(data_list)
list1 = search_for_value(data_list, 'Aufklaerungsquote', '<', 50)

save_list(list1, timestring() + "aufgabe1-1.csv")

# print(header)
# counter = 0
# for data in data_list:
#     print(data)
#     counter += 1
#     if counter > 10:
#         break
