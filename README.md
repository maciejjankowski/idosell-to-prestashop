# idosell-to-prestashop

## Instalacja

1. dodanie konfiguracji w `secrets.py`:

   ```
   IDOSELL_API_KEY="{KEY}"
   PRESTA_API_KEY="{KEY}"

   IDOSELL_API_URL="{URL}"
   PRESTA_API_URL="{URL}"
   ```
2. Uruchomienie
    1. Wgranie danych do folderu data do pliku idosell_clients.csv
    2. uruchomienie polecenia: `python map_csv.py`
    3. zaimportowanie `presta_clients.csv` do prestashop
    4. wysłanie maili z nowym hasłem do klientów z pliku `presta_passwords.csv`
