# map_csv.py
import csv
from mappers import map_client_record
import time


def read_idosell_csv(csv_file_path):
    """Reads a CSV file with idosell customer records and maps them to PrestaShop format.

    Args:
        csv_file_path (str): The path to the CSV file.

    Returns:
        list: A list of dictionaries, each representing a mapped PrestaShop client record.
    """

    presta_clients = []
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            idosell_client_record = {key.strip(): value.strip() for key, value in row.items()}
            presta_client_record = map_client_record(idosell_client_record)
            presta_clients.append(presta_client_record)
            
    return presta_clients

def main():
    csv_file_path = 'data/idosell_clients.csv'
    presta_clients = read_idosell_csv(csv_file_path)
    last_5_digits = str(int(time.time()))[-5:]
    with open(f'data/{last_5_digits}_presta_clients.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = presta_clients[0].keys()  # Get fieldnames from the first record
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for client in presta_clients:
            if len(client['Email *']) > 0:
                writer.writerow(client)
    
    with open(f"data/{last_5_digits}_presta_passwords.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ['Email *', 'Password *']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        for client in presta_clients:
            client_record = {"Email *": client["Email *"], "Password *": client["Password *"]}
            writer.writerow(client_record)
        
                

if __name__ == "__main__":
    main()
