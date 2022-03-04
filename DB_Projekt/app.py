from re import search
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
db = "Verein.db"

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/Daten-einfuegen', methods = ['GET', 'POST'])
def Daten_einfuegen():
    if request.method == 'GET':
        return render_template("Daten_einfuegen.html")
    else:
        mitglieder_daten = (
            request.form['vorname'],
            request.form['nachname'],
            request.form['geschlecht'],
            request.form['straße'],
            request.form['hausnummer'],
            request.form['plz'],
            request.form['email'],
            request.form['telefonnummer'],
            request.form['geburtsdatum'],
            request.form['eintrittsdatum'],
            request.form['abo'],
            request.form['notiz'],
            0,
            'nicht gültig'
        )  
        #print(mitglieder_daten) #zum testen
        mitglied_einfügen(mitglieder_daten)  
        return render_template("Eintrag_erfolgreich.html")

@app.route('/Daten-ergaenzen', methods = ['GET', 'POST'])
def Daten_ergaenzen():
    if request.method == 'GET':
        return render_template("Daten_ergaenzen.html")
    else:
        neue_daten = (
            request.form['vorname'],
            request.form['nachname'],
            request.form['geschlecht'],
            request.form['straße'],
            request.form['hausnummer'],
            request.form['plz'],
            request.form['email'],
            request.form['telefonnummer'],
            request.form['abo'],
            request.form['notiz'],
            request.form['gueltigkeit'],
            request.form['id']
        )
        print(neue_daten)
        mitglied_ergaenzen(neue_daten)  
        return render_template("Eintrag_erfolgreich.html")

def mitglied_ergaenzen(neue_daten):
    print(neue_daten)
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    sql_execute_string = ("""
    UPDATE Mitglieder
    SET 
    vorname = ?,
    nachname = ?,
    geschlecht = ?,
    straße = ?,
    hausnummer = ?,
    Postleitzahl = ?,
    email = ?,
    telefonnummer = ?,
    Aboart = ?,
    notiz = ?,
    Gültigkeit_Trainingsausweis = ?
    WHERE MitgliederID = ?
    """)
    cur.execute(sql_execute_string, (neue_daten))
    conn.commit()
    conn.close()

@app.route('/Eintrag-erfolgreich')
def Eintrag_erfolgreich():
    return render_template("Eintrag_erfolgreich.html")

#Zeigt alle nicht gelöschten Daten oder Sucht nach nicht gelöschten Daten + "sucheingabe*"
@app.route('/Daten-einsehen', methods = ['GET', 'POST'])
def Daten_einsehen():
    if request.method == 'GET':
        member_data = all_member_data()
        return render_template("Daten_einsehen.html", data=member_data)
    else:
        suche = request.form['suche']
        member_data_search = search_member_data(suche)
        return render_template("Daten_einsehen.html", data=member_data_search)

@app.route('/Trainingsanwesenheit', methods = ['GET', 'POST'])
def Trainingsanwesenheit():
    if request.method == 'POST':
        #Hinzufügen von Anwesenheiten
        if request.form['submit'] == 'hinzufuegen':
            Anwesenheitsdaten = (
            request.form['MitgliederID'],
            request.form['Trainingsanwesenheit']
            )

            #print("hinzufügen")
            #print(Anwesenheitsdaten)
            #return render_template("Trainingsanwesenheit.html")

            Trainingstag_einfügen(Anwesenheitsdaten)
            member_data = all_member_data_Trainingsanwesenheit()
            return render_template("Trainingsanwesenheit.html", data=member_data)
        #Überprüfung von Anwesenheitskriterien
        elif request.form['submit'] =='pruefen':
            MitgliederID = request.form['MitgliederIDprüfen']
            #print("überprüfen")
            #print(MitgliederID)
            #return render_template("Trainingsanwesenheit.html")
            
            #Datum = request.form['Trainingsanwesenheit']
            gültig = Anwesenheitskriterienüberprüfung(MitgliederID)
            print (gültig)
            if gültig == 1:
                return render_template("Gültigkeitsmeldung1_ungültig.html")
            elif gültig ==2:
                return render_template("Gültigkeitsmeldung2_ungültig.html")
            elif gültig == 3:
                return render_template("Gültigkeitsmeldung3_gültig.html")
            elif gültig == 4:   
                return render_template("Gültigkeitsmeldung4_gültig.html")
            else:
                return render_template("Fehlermeldung1.html")
            
        #Suche von Anwesenheiten Eines Mitgliedes(ID)    
        elif request.form['submit'] == 'suchen':
            MitgliederID = request.form['MitgliederIDsuchen']
            if MitgliederID == "":
                member_data = all_member_data_Trainingsanwesenheit()
                return render_template("Trainingsanwesenheit.html", data=member_data)
            member_data = search_member_data_Trainingsanwesenheit(MitgliederID)
            return render_template("Trainingsanwesenheit.html", data=member_data)
    elif request.method == 'GET':
        #print("Zeigt alle Daten an")
        #return render_template("Trainingsanwesenheit.html")
        member_data = all_member_data_Trainingsanwesenheit()
        return render_template("Trainingsanwesenheit.html", data=member_data)

### in der html benötigt die form den action befehl, damit der submit button beim click POST aktiviert <form action="http://localhost:5000/Daten-löschen" method="post">
@app.route('/Daten-löschen', methods = ['GET', 'POST'])
def Daten_löschen():
    if request.method == 'GET':
        return render_template("Daten_löschen.html")
    else:
        mitgliederid = request.form['id']
        mitglied_löschen(mitgliederid) 
        return render_template("Löschvorgang_erfolgreich.html")

@app.route('/Vergrößern')
def Vergrößern():
    return render_template("Vergrößern.html")


###Zeigt mir alle Mitgliederdaten an, bei denen der Wert "Deletet" 0 ist, also FALSE
def all_member_data():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("""
    SELECT *, round(julianday('now') - julianday(Eintrittdatum), 1) FROM Mitglieder WHERE Deleted = 0
    """)
    member_data = cur.fetchall()
    return member_data

def search_member_data(suche):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    #Without the comma, (img) is just a grouped expression, not a tuple,
    #and thus the img string is treated as the input sequence. If that string is 74 characters long,
    #then Python sees that as 74 separate bind values, each one character long.
    #>>> len(img)
    #4
    #>>> len((img,))
    #1
    #If you find it easier to read, you can also use a list literal:
    #cursor.execute('INSERT INTO images VALUES(?)', [img])
    sql_string = ("""
        SELECT *, round(julianday('now') - julianday(Eintrittdatum), 1) 
        FROM Mitglieder WHERE (Deleted = 0 AND Nachname LIKE ?||'%')
        OR (Deleted = 0 AND VORNAME LIKE ?||'%') 
        OR (Deleted = 0 AND Aboart LIKE ?||'%')
        OR (Deleted = 0 AND Gültigkeit_Trainingsausweis LIKE ?||'%')
        """) 
    cur.execute(sql_string, (suche, suche, suche, suche,))
    member_data_search = cur.fetchall()
    return member_data_search

def mitglied_einfügen(mitglieder_daten):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    sql_execute_string = 'INSERT INTO Mitglieder (Vorname, Nachname, Geschlecht, Postleitzahl, Straße, Hausnummer, EMail, Telefonnummer, Geburtsdatum, Eintrittdatum, Aboart, Notiz, Deleted, Gültigkeit_Trainingsausweis) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    cur.execute(sql_execute_string, mitglieder_daten)
    conn.commit()
    conn.close()

def Trainingstag_einfügen(Anwesenheitsdaten):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    sql_execute_string = 'INSERT INTO Trainingsanwesenheit (MitgliederID, Datum) VALUES (?, ?)'
    cur.execute(sql_execute_string, Anwesenheitsdaten)
    conn.commit()
    conn.close()

def mitglied_löschen(mitgliederid):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    sql_execute_string = ("""
    UPDATE Mitglieder SET Deleted = 1 WHERE MitgliederID = ?
    """)
    cur.execute(sql_execute_string, (mitgliederid,))
    #Zum Testen
    #print("UPDATE Mitglieder SET Deleted = 1 WHERE MitgliederID =?" + mitgliederid)
    conn.commit()
    conn.close()

def all_member_data_Trainingsanwesenheit():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("""
    SELECT * FROM Trainingsanwesenheit
    ORDER BY Datum DESC
    """)
    member_data = cur.fetchall()
    return member_data

def search_member_data_Trainingsanwesenheit(MitgliederID):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    sql_string = ("""
    SELECT * FROM Trainingsanwesenheit
    WHERE MitgliederID LIKE ?||'%'
    ORDER BY Datum DESC
    """)
    cur.execute(sql_string, MitgliederID)
    member_data = cur.fetchall()
    return member_data

def Anwesenheitskriterienüberprüfung(MitgliederID):
    conn = sqlite3.connect(db)
    #Connect to cursor
    cur = conn.cursor()
    ### Datumsformatierung von beispielsweise: 2022-02-12 -> 2022
    #Datum_Jahr = Datum[0:4]

    ###Zählt die Menge an Anwesenheiten von einem Mitglied pro Jahr (Jahr des letzten Eintrags)
    cur.execute("SELECT count(MitgliederID) FROM Trainingsanwesenheit WHERE MitgliederID = ?", (MitgliederID))
    data = cur.fetchall()

    ###Convert SQL tuple to Integer Beispiel:  [(13,)]  -> 13
    data_int = int(''.join(map(str, (data[0]))))
    print ("Anzahl der Anwesenheiten: ", data_int)
    ### Prüft, ob mehr als 17 Anwesenheiten vorhanden sind
    if data_int > 17:
        print("more than 17")
        ### Fragt den 1. Datensatz und den 18. Datensatz eines Anwesenheitsdatums eines Mitgliedes im selben Jahr.
        sql_string = ("""
        SELECT * FROM
            (
            SELECT Datum
            FROM Trainingsanwesenheit
            WHERE MitgliederID = ?
            ORDER BY Datum DESC
            LIMIT 1
            )
        UNION ALL
            SELECT * FROM
            (
                SELECT Datum
            FROM Trainingsanwesenheit
            WHERE MitgliederID = ?
            ORDER BY Datum DESC
            LIMIT 1 OFFSET 17
            )
            
        """)
        cur.execute(sql_string, (MitgliederID, MitgliederID,))
        data = cur.fetchall()
        #print(data)
        #print (data)
        #print (data[0])
        #print (data[1])
        ###String output der Abfrage in ein normales Datumsformat ändern###
        #data = str(data).replace(",","").replace("(","").replace(")","").replace("[","").replace("]","").replace("'","")
        #list = data.split() 
        #list = [e[:4] for e in list]
        #print(list)

        ### Prüft, ob der 1. (der Letzte) und der 18. Anwesenheitseintrag im gleichem Jahr waren.
        ### Bei ja, wird die Gültigkeit auf "'gültig' + dasJahr" geändert an dem die Bedingungen erfüllt wurden
        ### Bei einem neuen Eintrag für das nächste Jahr, enfällt dann wieder die Gültigkeit!
        ### Die Gültigkeit wird immer nur für das angegebene Jahr geprüft.
        ### Danach ist der Schein sowieso noch das nächste gültig (wie beim Flugschein)
        #if list[0] == list[1]:
        #    status = 'gültig ' + list[0]
        #    print("Trainingsnachweis gültig!")
        #    cur.execute("UPDATE Mitglieder SET Gültigkeit_Trainingsausweis = ? WHERE MitgliederID = ?", (status, MitgliederID,))
        #    conn.commit()
        #    conn.close()
        #    return
        #else:
        #    print("Nicht gültig! Da die 18 Anwesenheiten nicht innerhalb des gleichen Jahres stattfanden.")
        #    cur.execute("UPDATE Mitglieder SET Gültigkeit_Trainingsausweis = 'nicht gültig' WHERE MitgliederID = ?", (MitgliederID,))
        #    conn.commit()
        #    conn.close()

        for i in range(0, 2):
            data[i] = str(data[i]).replace(",","").replace("'", "").replace("(", "").replace(")","")
        print (data[0])
        print (data[1])
        ###	Brechnet Differenz zwischen zwei Datumseinträgen in Tagen: ('2023-05-18',) - ('2023-01-27',)
        cur.execute("SELECT round(julianday(?) - julianday(?))", (data[0], data[1]))
        data = cur.fetchall()
        print (data)
        ###Stringmodifikation von beispielsweise [(230.0,)] zu 230.0
        data = str(''.join(map(str, (data))))
        data = str(data).replace(")","")
        data = str(data).replace("(","")
        data = str(data).replace(",","")
        data_int = int(float(data))
        print (data)
        if data_int < 366:
            print("Trainingsnachweis gültig!")
            cur.execute("UPDATE Mitglieder SET Gültigkeit_Trainingsausweis = 'gültig' WHERE MitgliederID = ?", (MitgliederID,))
            conn.commit()
            conn.close()
            gültig = 3
            return gültig
        else:
            print("Immer noch nicht gültig! Da die 18 Anwesenheiten länger als 1 Jahr gebraucht haben.")
            cur.execute("UPDATE Mitglieder SET Gültigkeit_Trainingsausweis = 'nicht gültig' WHERE MitgliederID = ?", (MitgliederID,))
            conn.commit()
            conn.close()
            gültig = 1
            return gültig
    else:
        ### Prüft, ob weniger als 18 Anwesenheiten in einem Jahr vorhanden sind. Wenn ja, werden diese abgefragt
        if data_int < 18:
            print("less than 18")
            sql_string = ("""
                SELECT Datum
                FROM Trainingsanwesenheit
                WHERE MitgliederID = ?
                ORDER BY Datum DESC    
                LIMIT 17
                """)
            cur.execute(sql_string, (MitgliederID))
            Dautumswerte = cur.fetchall()
            print(Dautumswerte)

            ###Gibt mir eine Liste der Jahre aus den Anwesenheits Daten aus.
            ###Das Jahr des letzten Anwesenheitsdatums aus -> list_jahre[0]
            #Dautumswerte_Jahre = str(Dautumswerte).replace(",","").replace("(","").replace(")","").replace("[","").replace("]","").replace("'","")
            #list_jahre = Dautumswerte_Jahre.split() 
            #list_jahre = [e[:4] for e in list_jahre]
            #print(list_jahre)

            ### Wandelt die Datumswerte in eine Liste um, die nur aus den Werten der Monaten besteht.
            ### Beispiel: 2022-03-10 2022-02-22 2022-04-22 -> ['03', '02', '04']
            #Dautumswerte = ("[('2022-03-10',), ('2022-02-22',), ('2022-04-22',), ('2022-02-22',), ('2022-02-22',)]")
            Dautumswerte = str(Dautumswerte).replace(",","").replace("(","").replace(")","").replace("[","").replace("]","").replace("'","")
            print(Dautumswerte)
            list = Dautumswerte.split() 
            list = [e[5:] for e in list]
            #print(list)
            list = [e[:2] for e in list]
            #print(list)
            ### Prüft, ob alle Werte der Liste einzigartig sind.
            flag = 1
            if set(['01','02','03','04','05','06','07','08','09','10','11','12']).issubset(list):
                flag = 0

            if(flag == 0):
                print("Trainingsnachweis gültig!")
                cur.execute("UPDATE Mitglieder SET Gültigkeit_Trainingsausweis = gültig WHERE MitgliederID = ?", (MitgliederID,))
                conn.commit()
                conn.close()
                gültig = 4
                return gültig
            else:
                print("Nicht an jedem Monat teilgenommen. Die Anforderungen wurden nicht erfüllt.")
                cur.execute("UPDATE Mitglieder SET Gültigkeit_Trainingsausweis = 'nicht gültig' WHERE MitgliederID = ?", (MitgliederID,))
                conn.commit()
                conn.close()
                gültig = 2
                return gültig

        else:
            print("Fehler: Weder mehr als 17 noch weniger als 18 - kann nicht sein!")
            gültig = 5
            return gültig
###in procress
def mitglieder_aktualisieren():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    sql_execute_string = 'UPDATE Mitglieder (Vorname, Nachname, Geschlecht, Postleitzahl, Straße, Hausnummer, EMail, Telefonnummer, Geburtsdatum, Eintrittdatum, Aboart, Notiz) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    cur.execute(sql_execute_string)
    conn.commit()
    conn.close()


#debug = True can be turned off, after developing
if __name__ == '__main__':
    app.run(debug = True, port = 5000)