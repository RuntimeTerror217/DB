import sqlite3

db = "Verein.db"
#Connect to database
conn = sqlite3.connect(db)
#Connect to cursor
cur = conn.cursor()
###Zählt die Menge an Anwesenheiten von einem Mitglied
cur.execute("""
SELECT count(MitgliederID) 
FROM Trainingsanwesenheit
WHERE MitgliederID = 1 
""")

data = cur.fetchall()
print (data)
###Convert SQL tuple to Integer Beispiel:  [(13,)]  -> 13
data_int = int(''.join(map(str, (data[0]))))
print (data_int)

if data_int > 10:
    print("yes")
    cur.execute("""
    SELECT * FROM
        (
        SELECT Datum
        FROM Trainingsanwesenheit
        WHERE MitgliederID = 1
        LIMIT 1
        )
    UNION ALL
        SELECT * FROM
        (
            SELECT Datum
        FROM Trainingsanwesenheit
        WHERE MitgliederID = 1
        LIMIT 1 OFFSET 9
        )
    """)
    data = cur.fetchall()
    ###String output der Abfrage in ein normales Datumsformat ändern###
    #print (data)
    #print (data[0])
    #print (data[1])
    data[0] = str(data[0]).replace(",","")
    data[1] = str(data[1]).replace(",","")
    data[0] = str(data[0]).replace("'","")
    data[1] = str(data[1]).replace("'","")
    data[0] = str(data[0]).replace("(","")
    data[1] = str(data[1]).replace("(","")
    data[0] = str(data[0]).replace(")","")
    data[1] = str(data[1]).replace(")","")
    #print (data[0])
    #print (data[1])
    cur.execute("SELECT round(julianday(?) - julianday(?))", (data[1], data[0]))
    data = cur.fetchall()
    print (data)
    ###Stringmodifikation von beispielsweise [(230.0,)] zu 230.0
    data = str(''.join(map(str, (data))))
    data = str(data).replace(")","")
    data = str(data).replace("(","")
    data = str(data).replace(",","")
    #print (data)
    if data_int < 366:
        print("Trainingsnachweis gültig!")
    else:
        print("Trainingsnachweis ungültig! - Anforderungen noch nicht erfüllt")
else:
    print("no")

#Commit command
conn.commit()
#Close connection
conn.close()