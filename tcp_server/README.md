# TCP/IP Server für RPI mit OpenCV Funktionalität

### Dependencies:
+ KreisPi.py (in Projekt gegeben)
+ [Pillow](https://pillow.readthedocs.io/en/stable/): **sudo pip3 install Pillow**
+ [OpenCV](www.alatortsev.com/2018/11/21/installing-opencv-4-0-on-raspberry-pi-3-b/)

### Ausführen:
entweder **./server.py** oder mit **python3 server.py**

### Befehle:
+ **GO** -> Get Offset führt Kreiserkennung aus und schickt X/Y Offset als *GOXoffYoff* zurück
+ **EX** -> Beendet den Server und schließt die Verbindung
+ **CO** -> konfiguriert die Kreiserkennung mit dem Config generator
+ **IM** -> erstellt ein einfaches Bild
+ **CV** -> erstellt ein Bild mit erkannten Kreisen

### Debugging:
Der Server sollte bei Fehlern nicht abstürzen, sondern per Try/Catch eine Exception werfen und einen Fehlercode zurückgeben:
+ **OK**: Der Befehl wurde ohne Fehler umgesetzt
+ **NO**: Ein Verzeichnis/Bild konnte nicht erstellt werden
+ **ER**: Schwerwiegender Fehler. Kreiserkennung/Kamera abgestürzt z.B.
(Fehler oder ein Print steht in der Kommandozeile des Servers)
