import csv

def setNumber(input_str):  
    all_sets = []
    with open('utils/trainsets.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            all_sets.append(row[0])  # Append the first item in each row
    
    for set_str in all_sets:
        temp = set_str.split('-')
        if input_str in temp:
            return set_str
    return None