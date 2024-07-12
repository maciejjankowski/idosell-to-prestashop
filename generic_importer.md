# Import klientów z idosell do prestashop

## Narzędzia
- Python, PHP, lub inny nowoczesny język programowania
- Arkusz Excel / Sheets
- Platforma ETL (dla gigantycznych ilości danych)

## Kroki migracji
1. Eksport danych z idosell do CSV (np. ido_customers.csv)
2. Mapowanie kolumn (powiązanie kolumn z idosell do kolumn z prestashop) `block_account` => `Active (0/1)`
3. Mapowanie danych (np. w idosell kolumna `block_account` ma wartości `y|n`, w presta należy wtedy ustawić kolumnę `Active (0,1)` według wartości: `y` => `0` i `n` => `1`)
3. Walidacja danych z `ido_customers.csv` według reguł zawartych w dokumentacji [Prestashop](https://devdocs.prestashop-project.org/8/webservice/reference/#names)
4. Backup bazy prestashop
5. Import danych do prestashop
6. Sprawdzenie danych
7. (być może) **SUKCES***
8. _[Opcjonalnie]_ Wysłanie nowych haseł do klientów lub (**bezpieczniej**) reset hasła

## Metody migracji

1. CSV -> mapowanie -> CSV
2. CSV -> mapowanie -> API
3. API -> mapowanie -> CSV
4. API -> mapowanie -> API

### Wady / zalety
**API-API**
- może być wolniejsze niż import z CSV, jeśli sklep docelowy nie obsługuje jednoczesnego wysyłania wielu żądań lub ma niskie limity operacji korzystania z API
- mamy większą kontrolę nad powstającymi błędami i możemy pominąć (i zapisać na później) rekordy, których nie udało się zapisać. Wtedy przynajmniej część danych się zgadza, możemy wtedy je poprawić i uruchomić ponownie import tylko dla brakujących danych
- możemy napisać zaawansowane reguły aktualizacji danych: np. import klienta może powodować zakolejkowanie importu zamówień klienta oraz innych powiązanych rekordów

**import CSV**
- prawdopodobnie będzie najszybsze (o ile mamy poprawne dane, albo robiliśmy już import wcześniej i wiemy co i jak)
- błąd w pliku z danymi może powodować przerwanie całej operacji i wtedy konieczne będą poprawki i powtórki



## Mapowanie kolumn i danych
### Arkusz kalkulacyjny Excel / Sheets
Umożliwiają załadowanie i obróbkę danych w formacie CSV. 

Dla wprawionej osoby stworzenie arkusza do importu na podstawie danych wejściowych nie powinno być trudnym zadaniem. Ważne aby napisać odpowiednie reguły walidacji wszystkich kolumn i poprawić dane, zanim wyeksportujemy je do CSV.
W przypadku arkuszy możemy napotkać na problemy związane z wydajnością przy przetwarzaniu dużych ilości danych

### Python lub PHP
Oba z tych języków umożliwiają łatwe przetwarzanie plików CSV, we wprawnych rękach oferują elastyczność i szybkość oraz praktycznie pozbawione są ograniczeń co do ilości przetwarzanych danych. Oczywiście to tylko sugestia. Równie dobrze można pisać importery w BASICu, C czy Javascripcie.

## Przykładowa walidacja danych w pythonie

```python
import re

def validate_customer_name_prestashop_like(name):
    """
    Waliduje imię i nazwisko klienta, naśladując zachowanie PrestaShop:
    - Maksymalna długość: 255 znaków (dla całego imienia i nazwiska)
    - Dozwolone znaki: litery (ASCII i rozszerzone), spacje, myślniki, apostrofy, kropki
    - Musi zawierać co najmniej jedno imię i jedno nazwisko (oddzielone spacją)
    - Dopuszcza wielokrotne imiona lub nazwiska (oddzielone spacją)
    """

    if len(name) > 255:
        return False

    # Dopuszczalne znaki (uwzględniając polskie znaki diakrytyczne)
    allowed_chars = r"a-zA-Z\u00C0-\u017F\s'-."

    # Wzorzec sprawdzający, czy imię i nazwisko składają się z co najmniej dwóch słów
    # Dopuszcza wielokrotne imiona lub nazwiska
    pattern = fr"^[{allowed_chars}]+ (?:[{allowed_chars}]+ )+[{allowed_chars}]+$"

    if not re.match(pattern, name):
        return False

    return True
```