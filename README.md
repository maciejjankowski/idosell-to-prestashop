# idosell-to-prestashop

[meta](/meta/readme.md)

## Migracje danych

- [Ogólny opis procesu migracji i narzędzia](generic_importer.md)
- [Jak przygotować i przenieść dane do PrestaShop za pomocą Pythona](how_to_migrate.md)
- [Mini kurs Migracja Danych](minikurs.md)

## Uruchomienie

0. Zrób backup bazy danych (!) :]
1. Wgranie danych do folderu `data` do pliku `idosell_clients.csv`
2. uruchomienie polecenia: `python map_csv.py`
3. zaimportowanie `presta_clients.csv` do prestashop
4. wysłanie maili z nowym hasłem do klientów z pliku `presta_passwords.csv`
