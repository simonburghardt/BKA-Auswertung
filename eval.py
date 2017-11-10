import csv
import operator
import os
from collections import OrderedDict

data_list = []  # Liste der Datensatz-Dictionaries
header = []  # Liste der Feldnamen
csv_file = 'data/data.csv'  # Dateipfad der auszuwertenden Dateien
output_folder = 'output/'


def menu():
    while True:
        user_input = input("\t\t1 -> Teilaufgabe 1 ausgeben\n\
        2 -> Suchen\n\
        3 -> Filtern\n\
        4 -> Programm beenden")
        if user_input == "1":
            exercise1()
        elif user_input == "2":
            print()
            # TODO: Aufgabe 2-1
        elif user_input == "3":
            print()
            # TODO: Aufgabe 2-2
        elif user_input == "4":
            exit()
        else:
            print('Ungügltige Eingabe')


def exercise1():
    list1 = filter_by(data_list, 'Kreisart', 'LK')
    list1 = search_for_value(list1, 'Aufklaerungsquote', '<', 50)
    save_list(list1, ['Stadt-/Landkreis', 'Straftat', 'Aufklaerungsquote'], 'aufgabe1-1.csv')

    list2 = count_all_cases(data_list, "Straftat")
    save_list(list2, ['Straftat', 'Summe'], 'aufgabe1-2.csv')

    list3 = sort_by(list2, 'Summe', 'absteigend')
    save_list(list3, ['Straftat', 'Summe'], 'aufgabe1-3.csv')

def load_list():
    # Läd die Datei und speichert den Inhalt in data list und die Feldnamen in Header
    global data_list, header

    with open(csv_file, 'r+', encoding='windows-1252') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            data_list.append(row)
        header = reader.fieldnames
        # Funktioniert aktuell nur mit modifizierter Datei
    print('Daten geladen!')
    return True


def save_list(save_data_list, save_header, filename):
    # user_input = input('Soll die Liste '' + csv_file + '' wirklich gespeichert werden? \'Ja\' zur Bestätigung eingeben')
    # if user_input == '' or not (user_input[0].upper() == 'J'):
    #     print('Keine Liste gespeichert!')
    #     return False

    if not os.path.exists(output_folder):
        # creates output folder if it doesnt exist
        os.makedirs(output_folder)
    with open(output_folder + filename, 'w+', encoding='windows-1252') as f:
        writer = csv.DictWriter(f, save_header, delimiter=';', extrasaction='ignore', lineterminator='\n')
        writer.writeheader()
        writer.writerows(save_data_list)
    print('Datensätze gespeichert!')
    return True


def search_for_value(search_data_list, key, operator_string, value):
    operators = {'>': operator.gt,
                 '<': operator.lt,
                 '>=': operator.ge,
                 '<=': operator.le,
                 '=': operator.eq}
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


def filter_by(filter_data_list, key, value):
    # filter list by one key
    # returns filtered list
    return_list = []
    for data in filter_data_list:
        if data[key] == value:
            return_list.append(data)

    return return_list


def count_all_cases(count_data_list, key):
    # returns dictionary with key and sum
    sum_count = {}
    for data in count_data_list:
        key_value = data[key]
        if key_value in sum_count.keys():
            sum_count[key_value] += int(data['erfasste Faelle'])
        else:
            sum_count[key_value] = 0
    return_list = []
    for k, v in sum_count.items():
        return_list.append({key: k, "Summe": v})
    return return_list


def sort_by(sort_data_list, sort_key, sort_how):
    # returns list of dictionarys sorted by sortkey
    sorted_list = []
    if sort_how == 'aufsteigend':
        sorted_list = sorted(sort_data_list, key=lambda k: k[sort_key], reverse=False)
    if sort_how == 'absteigend':
        sorted_list = sorted(sort_data_list, key=lambda k: k[sort_key], reverse=True)
    return sorted_list


load_list()
menu()

# list2 = count(data_list, "Stadt-/Landkreis")
# save_list(list2, ['Stadt-/Landkreis', 'Summe'], 'aufgabe1-2.csv')
# Test-Fragment


# print(header)
# counter = 0
# for data in data_list:
#     print(data)
#     counter += 1
#     if counter > 10:
#         break
