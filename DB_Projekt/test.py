### Wandelt die Datumswerte in eine Liste um, die nur aus den Werten der Monaten besteht.
### Beispiel: 2022-03-10 2022-02-22 2022-04-22 -> ['03', '02', '04']
string1 = ("[('2022-03-10',), ('2022-02-22',), ('2022-04-22',), ('2022-01-22',), ('2022-05-22',), ('2022-07-22',), ('2022-06-22',), ('2022-08-22',), ('2022-10-22',), ('2022-09-22',), ('2022-11-22',), ('2022-12-22',), ('2022-04-22',), ('2022-02-22',), ('2022-02-22',), ('2022-04-22',), ('2022-02-22',)]")
string1 = str(string1).replace(",","").replace("(","").replace(")","").replace("[","").replace("]","").replace("'","")
print(string1)
list = string1.split() 
list = [e[5:] for e in list]
print(list)
list = [e[:2] for e in list]
print(list)

### Prüft, ob alle Werte der Liste einzigartig sind.
flag = 1
if set(['01','02','03','04','05','06','07','08','09','10','11','12']).issubset(list):
    flag = 0

if(flag == 0):
    print("An allen Monaten wurde teilgenommen. Die Anforderungen sind erfüllt.")
else:
    print("Nicht an jedem Monat teilgenommen. Die Anforderungen wurden nicht erfüllt.")