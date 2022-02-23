import sqlite3

db = "Verein.db"
#Connect to database
conn = sqlite3.connect(db)
#Connect to cursor
cur = conn.cursor()

cur.execute("""
INSERT INTO Mitglieder (Vorname, 
Nachname, 
Geschlecht, 
Postleitzahl, 
Straße,
Hausnummer,
EMail,
Telefonnummer,
Geburtsdatum,
Eintrittdatum,
Aboart,
Notiz,
Deleted) VALUES 
("Pascal", "Kraus", "Männlich", 67550, "Wonnegausstraße", 70, "krauspascal@gmail.com", 12345678, "12.12.1990", "12.12.2000", "Feuerwaffen", "Ist stehts bemüht!", 0),
("David", "Bubatz", "Weiblich", 12345, "Eichweg", 5, "Bubatz@Bubatz.com", 12345612, "12.12.1995", "12.12.2005", "Bögen", "Uff, was ein typ ...", 1)
""")

#Commit command
conn.commit()
#Close connection
conn.close()