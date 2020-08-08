# peewee-click-sqlite

# Instalacja
Oprócz pakietu [python'a](https://www.python.org/downloads/) należy zainstalować pakiety znajdujące się w pliku
*requirements.txt*. Można tego dokonać przy użyciu cmd:
```bash
pip install -r requirements.txt
```
# Uruchomienie
1. Aby załadować dane do bazy danych, należy uruchomić w konsoli moduł *main.py*. Zostaniemy zapytani o to czy
chcemy, by dane pochodziły z pliku json czy z API (zadanie dodatkowe). Ładowanie danych do bazy może chwilę potrwać. Po zakończeniu
pojawi się plik *persons.sqlite3*:
* pole z liczbą dni pozostałych do następnych urodzin znajduje się w tabeli 'Dob'
* oczyszczone numery telefonów znajdują się w tabeli 'Person'
* pole 'picture' zostało całkowicie usunięte z tabel (nie jest w żadnym miejscu ładowane do bazy), hasło jest w postaci plaintext

Przed ponownym załadowaniem danych należy usunąć *persons.sqlite3*. Aby w łatwiejszy sposób pracowało się z danymi w przyszłości,
dane zostały rozdzielone na większą ilość tabel.


2. Aby skorzystać z komend skryptu, w cmd należy wpisać *script.py* oraz nazwę komendy i jej argument lub opcję.
Dostępne komendy :
*   average-age &ensp;&ensp;&ensp;&ensp;&ensp;(opcja '--gender', default='all')
*   most-common-cities&ensp;&ensp;(argument 'number', default=1)
*   most-common-passwords&ensp;(argument 'number', default=1)
*   most-secure-password&ensp;(brak argumentów i opcji)
*   people-by-dob-range&ensp;&ensp;(user prompt)
*   percent-by-gender&ensp;&ensp;(wymagana opcja '--gender')

W razie problemów z jakąkolwiek z komend, należy w cmd wprowadzić *script.py* <nazwa_komendy> --help




