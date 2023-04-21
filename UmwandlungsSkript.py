import mysql.connector
import decimal

# Verbindung mit der Datenbank aufbauen
db = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="",
  database="ernaehrungsplan"
)

# Datenabfrage aus der Datenbank
cursor = db.cursor()
cursor.execute("SELECT zutaten FROM gerichte")
results = cursor.fetchall()
cursor.execute("SELECT gewicht FROM gerichte")
results1 = cursor.fetchall()
cursor.execute("SELECT gericht FROM gerichte")
results2 = cursor.fetchall()

# forloop für jedes Gericht
for row, row1, row2 in zip(results, results1, results2):
  zutaten = row[0].split(",")
  gewicht = row1[0].split(",")
  Nährwerte = [0, 0, 0, 0, 0, 0, 0, 0, 0]
  gericht = row2[0].split(",")

  # forloop für jede Zutat eines Gerichts
  for x,y in zip(zutaten,gewicht):
    cursor.execute("SELECT * FROM `nahrungsmittel (produkte)` WHERE Nahrungsmittel=%s", (x,))
    A = cursor.fetchall()
    A = A[0]
    A = list(A)
    del A[:6]
    y1 = decimal.Decimal(y) / 100
    Nährwerte = [x + (y * y1) for x, y in zip(Nährwerte, A)]
  sql = ("UPDATE gerichte SET Preis = %s, Kohlenhydrate = %s, Zucker = %s, Proteine = %s, Fett = %s, `Ungesättigte Fettsäuren` = %s, Kalorien = %s WHERE Gericht = %s")
  #sql = "INSERT INTO gerichte (Gericht, Preis, Kohlenhydrate, Zucker, Proteine, Fett, `Ungesättigte Fettsäuren`, Kalorien, Zutaten, Gewicht) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
  cursor.execute(sql, tuple(Nährwerte) + tuple(gericht))
  db.commit()


cursor.execute("SELECT * FROM gerichte WHERE Portionen != 1 AND Gericht IN (SELECT Gericht FROM gerichte GROUP BY Gericht HAVING COUNT(*) = 1)")
results3 = cursor.fetchall()
for row3 in results3:
  B = list(row3)
  C = B.copy()
  del B[:4]
  del C[-8:]
  print(B)
  print(C)
  B = [x / B[0] for x in B]
  print(B)
  D = C + B
  print(D)
  sql1 = ("INSERT INTO gerichte (Küche, Gericht, Zutaten, Gewicht, Portionen, Preis, Kohlenhydrate, Zucker, Proteine, Fett, `Ungesättigte Fettsäuren`, Kalorien) VALUES(%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s)")
  cursor.execute(sql1, tuple(D))
  db.commit()



