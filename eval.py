import csv
import operator
import os

data_list = []  # Liste der Datensatz-Dictionaries
header = []  # Liste der Feldnamen
csv_file = 'data/data_original.csv'  # Dateipfad der auszuwertenden Dateien
output_folder = 'output/'


def menu():
    while True:
        user_input = input('\t\t1 -> Teilaufgabe 1 ausgeben\n\
        2 -> Suche nach Daten (2.1)\n\
        3 -> Filtern\n\
        4 -> Programm beenden\n')
        if user_input == '1':
            exercise1()
        elif user_input == '2':
            search(data_list)
        elif user_input == '3':
            print("Sie haben nun die Möglichkeit, in 2 numerischen Feldern zu suchen, "
                  "und diese dann mit UND oder ODER logisch zu verknüpfen!")
            list1 = filter_numeric(data_list)
            list2 = filter_numeric(data_list)
            filter_connect(list1, list2)
        elif user_input == '4':
            exit()
        else:
            print('Ungügltige Eingabe')


def exercise1():
    list1 = filter_by(data_list, 'Kreisart', 'LK')
    list1 = search_for_value(list1, 'Aufklaerungsquote', '<', 50)
    save_list(list1, ['Stadt-/Landkreis', 'Straftat', 'Aufklaerungsquote'], 'aufgabe1-1.csv')

    list2 = count_all_cases(data_list, 'Straftat')
    save_list(list2, ['Straftat', 'Summe'], 'aufgabe1-2.csv')

    list3 = sort_by(list2, 'Summe', 'absteigend')
    save_list(list3, ['Straftat', 'Summe'], 'aufgabe1-3.csv')


def load_list():
    # Läd die Datei und speichert den Inhalt in data list und die Feldnamen in Header
    global data_list, header

    with open(csv_file, 'r+', encoding='windows-1252') as f:
        f.readline()
        # skips the numbering in line 1
        reader = csv.DictReader(f, delimiter=';')
        header = reader.fieldnames
        for row in reader:
            if row[header[0]] == '------' or row[header[0]] == '1':
                # skips numbering and summeries
                continue
            data_list.append(row)
        # Funktioniert jetzt mit original-datei
    print('Daten geladen!')
    return True


def save_list(save_data_list, save_header, filename):
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
    # searches for data in a data-list, where a value is greater than the parameter value
    operators = {'>': operator.gt,
                 '<': operator.lt,
                 '>=': operator.ge,
                 '<=': operator.le,
                 '=': operator.eq}
    return_list = []
    op = operators[operator_string]
    for data in search_data_list:
        if op(float(data[key]), float(value)):
            return_list.append(data)
    return return_list


def search_for_string(search_data_list, key, value):
    # searches for a given value in a given column in a data-list
    return_list = []
    for data in search_data_list:
        if value in data[key]:
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
        return_list.append({key: k, 'Summe': v})
    return return_list


def sort_by(sort_data_list, sort_key, sort_how):
    # returns list of dictionaries sorted by a sort-key
    sorted_list = []
    if sort_how == 'aufsteigend':
        sorted_list = sorted(sort_data_list, key=lambda k: k[sort_key], reverse=False)
    if sort_how == 'absteigend':
        sorted_list = sorted(sort_data_list, key=lambda k: k[sort_key], reverse=True)
    return sorted_list


def print_list(print_data_list):
    # prints given data-list into console
    for data in print_data_list:
        print(data)
        # TODO: Ausgabe formatieren
    return True


def save_or_print(output_data_list):
    # decides whether to print a data-list into console or save in csv file
    choice = input("Wollen sie das Ergebnis in der Console anzeigen lassen "
                   "oder in einer CSV Datei speichern? Type Console or CSV")
    if choice == 'Console':
        print_list(output_data_list)
    elif choice == 'CSV':
        name = input("Geben sie den Namen ein, unter der Sie die Ergebnisse speichern wollen")

        # TODO: Value check
        # schneidet den Namen ab, wenn ein Punkt eigegeben wurde. aufgabe.csv --> aufgabe
        name = name.split("." or "," or "|")[0]

        save_list(output_data_list, header, name + '.csv')
    else:
        print("Falsche Eingabe")


def search(search_data_list):
    # add comment
    prompt = 'Welches Feld soll durchsucht werden? Verfügbare Werte:\n'
    for key in header:
        prompt += '(' + key + ') '
    prompt += '\n'
    # TODO: Prompt überarbeiten
    key = input(prompt)

    if key not in header:
        print('Wert ist nicht verfügbar')
        return False

    # Suche nach Teilstrings ist möglich
    value = input('Nach welchem Wert soll gesucht werden?')
    search_data_list = search_for_string(search_data_list, key, value)

    if len(search_data_list) == 0:
        print("Keine Einträge gefunden")
        return True
    else:
        save_or_print(search_data_list)


def filter_numeric(filter_data_list):
    # filters in numeric fields of a data list, by key, value and comparison operator
    numeric_keys = ['Schluesse', 'Gemeindeschluessel', 'erfasste Faelle', 'HZ nach Zensus', 'Versuche - Anzahl',
                    'Versuche - Anteil in %', 'mit Schusswaffe gedroht', 'mit Schusswaffe geschossen',
                    'aufgeklaerte Faelle', 'Aufklaerungsquote', 'Tatverdaechtige insgesamt',
                    'Tatverdaechtige - maennlich', 'Tatverdaechtige - weiblich', 'Nichtdeutsche Tatverdaechtige - Anzahl',
                    'Nichtdeutsche Tatverdaechtige - Anteil in %']

    prompt = 'In welchem numerischen Feld möchten sie suchen?\n'
    for key in numeric_keys:
        prompt += '(' + key + ') '
    prompt += '\n'
    key = input(prompt)
    if numeric_keys.__contains__(key):
        value = input("Nach welchem Wert wollen sie suchen?")
        vergleich_operator = input("Geben sie einen Vergleichsoperator ein! (=, >, <, >=, <=")
        list = search_for_value(filter_data_list, key, vergleich_operator, value)
        return list

    else:
        print('Falsche Eingabe')


def filter_connect(filter_data_list1, filter_data_list2):
    # merges the 2 filtered data lists and connects them with AND or OR
    output_list = []
    hilf = []
    log_op = input('Wollen sie die Liste mit UND oder ODER logisch verknüpfen?\n'
                   'UND/ODER')

    # writes both lists in 1 list (OR), leaves out data that is already in the list
    if log_op == 'ODER':
        for row in filter_data_list1:
            output_list.append(row)
        for row in filter_data_list2:
            if output_list.__contains__(row):
                pass
            else:
                output_list.append(row)
        save_or_print(output_list)

    # writes rows in the output list, that are in both lists (AND)
    elif log_op == 'UND':
        for row in filter_data_list1:
            hilf.append(row)
        for row in filter_data_list2:
            if hilf.__contains__(row):
                output_list.append(row)
            else:
                pass
        save_or_print(output_list)

    else:
        print('Falsche Eingabe')


load_list()
menu()
