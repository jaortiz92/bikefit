import csv


def save_data(data):
    with open('data.csv', 'w') as file:
        write = csv.write(file)
        for data_name, value_name in data.items(): 
            write.rows(value_name)