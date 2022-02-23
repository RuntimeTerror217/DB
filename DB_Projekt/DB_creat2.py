import sqlite3

db = "Verein.db"
#Connect to database
conn = sqlite3.connect(db)
#Connect to cursor
cur = conn.cursor()

cur.execute("""
ALTER TABLE Mitglieder
ADD Gültigkeit_Trainingsausweis
""")

#Commit command
conn.commit()
#Close connection
conn.close()