import sqlite3

db = "Verein.db"
#Connect to database
conn = sqlite3.connect(db)
#Connect to cursor
cur = conn.cursor()

cur.execute("""
CREATE TABLE Trainingsanwesenheit
(TrainingsanwesenheitsID INTEGER PRIMARY KEY AUTOINCREMENT,
MitgliederID INTEGER,
Datum TEXT)
""")

#Commit command
conn.commit()
#Close connection
conn.close()