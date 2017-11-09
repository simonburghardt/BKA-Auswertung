import csv

data_list = []  # Liste der Datensatz-Dictionaries
header = []  # Liste der Feldnamen
csv_file = "data/data.csv"  # Dateipfad der auszuwertenden Dateien


def load_list():
    # Läd die Datei und speichert den Inhalt in data list und die Feldnamen in Header
    global data_list, header

    # with open(csv_file, "r+", encoding='utf-8') as f:
    with open(csv_file, "r+") as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            data_list.append(row)
        header = reader.fieldnames
        # TODO: Läd aktuell nicht richtig
    print("Daten geladen!")
    return True


def save_list():
    user_input = input("Soll die Liste '" + csv_file + "' wirklich gespeichert werden? \'Ja\' zur Bestätigung eingeben")
    if user_input == "" or not (user_input[0].upper() == 'J'):
        print("Keine Liste gespeichert!")
        return False
    with open(csv_file, "w+", encoding='utf-8') as f:
        writer = csv.DictWriter(f, header, delimiter=';', lineterminator='\n')
        writer.writeheader()
        writer.writerows(data_list)
    print("Kontakte gespeichert!")
    return True


load_list()
print(header)
counter = 0
for data in data_list:
    print(data)
    counter += 1
    if counter > 10:
        break
