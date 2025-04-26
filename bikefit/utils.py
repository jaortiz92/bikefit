import csv


def save_data(data):
    with open('data.csv', 'w') as file:
        write = csv.writer(file)
        for data_name, value_name in data.items(): 
            write.writerow(value_name)