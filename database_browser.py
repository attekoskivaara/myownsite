import sqlite3

# Yhdistä tietokantaan
conn = sqlite3.connect('C:\dev\myownsite\db.sqlite3')
cursor = conn.cursor()

# Näytä kaikki taulut tietokannassa
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
taulut = cursor.fetchall()
print("Tietokannan taulut:", taulut)

# Lue tietoja yhdestä taulusta (esim. 'asiakkaat')
#cursor.execute("SELECT * FROM asiakkaat")
rivit = cursor.fetchall()
for rivi in rivit:
    print(rivi)

# Sulje yhteys
conn.close()
