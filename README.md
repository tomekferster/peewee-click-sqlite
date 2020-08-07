# peewee-click-sqlite

# Instalacja
Oprócz pakietu [python'a](https://www.python.org/downloads/) należy zainstalować pakiety znajdujące się w pliku
*requirements.txt*. Można tego dokonać przy użyciu cmd:
```bash
pip install -r requirements.txt
```
# Uruchomienie
1. Aby załadować dane do bazy danych, należy uruchomić w konsoli moduł *main.py*. Zostaniemy zapytani o to czy
chcemy, by dane pochodziły z pliku json czy z API. Ładowanie danych do bazy może chwilę potrwać. Po zakończeniu
pojawi się plik *persons.sqlite3*:
* pole z liczbą dni pozostałych do następnych urodzin znajduje się w tabeli 'Dob'
* oczyszczone numery telefonów znajdują się w tabeli 'Person'
* pole 'picture' zostało całkowicie usunięte z tabel (nie jest w żadnym miejscu ładowane do bazy)

Przed ponownym załadowaniem danych należy usunąć *persons.sqlite3* 


2. Aby skorzystać z komend skryptu, w cmd należy wpisać *script.py* oraz nazwę komendy i jej argument (jeśli jest wymagany)
Dostępne komendy :
*   average-age     
*   most-common-cities
*   most-common-passwords
*   most-secure-password
*   people-by-dob-range
*   percent-by-gender





