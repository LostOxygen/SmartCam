# TCP/IP Server für RPI mit OpenCV Funktionalität

### Dependencies:
siehe [Dependecies](https://github.com/LostOxygen/OpenCV#Dependecies)

### Ausführen:
entweder **sudo ./server.py** oder mit **sudo python3 server.py**

### Befehle:
+ **GO** -> Get Offset führt Kreiserkennung aus und schickt X/Y Offset als *GOXoffYoff* zurück
+ **EX** -> Beendet den Server und schließt die Verbindung
+ **CO** -> konfiguriert die Kreiserkennung mit dem Config generator
+ **IM** -> erstellt ein einfaches Bild
+ **CV** -> erstellt ein Bild mit erkannten Kreisen
+ **KO** -> gibt Kabel Offset zurück. Muss zweimal gemacht werden um beide Seiten des Kabels zu berücksichtigen. Format der Rückgabe: *KOYoffZoff*. Wobei Z die Länge des Kabels angibt.
+ **FX** -> nimmt Befehl als *FXxxx* entgegen und setzt alle LEDs auf *xxx*

### Debugging:
Der Server sollte bei Fehlern nicht abstürzen, sondern per Try/Catch eine Exception werfen und einen Fehlercode zurückgeben:

+ **OK**: Der Befehl wurde ohne Fehler umgesetzt
+ **NO**: Ein Verzeichnis/Bild konnte nicht erstellt werden
+ **ER**: Schwerwiegender Fehler. Kreiserkennung/Kamera abgestürzt z.B.
(Fehler oder ein Print steht in der Kommandozeile des Servers)
