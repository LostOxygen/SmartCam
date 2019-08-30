# TCP/IP Server für RPI mit OpenCV Funktionalität

### Dependencies:
siehe [Dependecies](https://github.com/LostOxygen/OpenCV#Dependecies)

### Ausführen:
entweder **sudo ./server.py** oder mit **sudo python3 server.py**

### Befehle:
+ **GO** -> Get Offset führt Kreiserkennung aus und schickt X/Y Offset als *GOXoffYoff* zurück
+ **EX** -> Beendet den Server und schließt die Verbindung
+ **CFGx** -> konfiguriert die Kreiserkennung mit dem Config generator (x = 1 oder 2, um Skalierungsfaktor zu berechnen)
+ **IM** -> erstellt ein einfaches Bild
+ **CV** -> erstellt ein Bild mit erkannten Kreisen
+ **KOx** -> gibt Kabel Offset zurück. Muss zweimal gemacht werden (x = 1 oder 2) um beide Seiten des Kabels zu berücksichtigen. Format der Rückgabe: *KOXoffYoffZoff*. Wobei Z die Länge des Kabels angibt. (X,Y) ist die Koordinate der Kabelspitze **relativ** zum Bildmittelpunkt.
+ **FX** -> nimmt Befehl als *FXhexhexhex* entgegen und setzt die LEDs auf *hex* wobei *hex* ein Hexadezimaler Wert der Form 00 bis FF ist.

### Debugging:
Der Server sollte bei Fehlern nicht abstürzen, sondern per Try/Catch eine Exception werfen und einen Fehlercode zurückgeben:

+ **ACK**: Befehl wurde ohne Fehler ausgeführt
+ **NAK**: Befehl wurde aufgrund eines Fehlers nicht ausgeführt
+ **EX**: Server wurde per Befehl beendet
