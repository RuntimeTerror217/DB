import sqlite3

db = "Verein.db"
#Connect to database
conn = sqlite3.connect(db)
#Connect to cursor
cur = conn.cursor()

cur.execute("""
CREATE TABLE Mitglieder
(MitgliederID INTEGER PRIMARY KEY AUTOINCREMENT,
Vorname TEXT,
Nachname TEXT,
Geschlecht TEXT,
Postleitzahl INTEGER,
Straße TEXT,
Hausnummer INTEGER,
EMail TEXT,
Telefonnummer TEXT,
Geburtsdatum TEXT,
Eintrittdatum TEXT,
Aboart TEXT,
Notiz TEXT,
Deleted INTEGER NOT NULL
Gültigkeit_Trainingsausweis Text)
""")

#Commit command
conn.commit()
#Close connection
conn.close()