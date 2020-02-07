# Studienprojekt "Lernen einer Montageaufgabe"

### Befehle

Alle Befehle bestehen aus einem Bezeichner (die ersten 3 Zeichen) und weitere durch Parameter getrennte Parameter.

| Bezeichner | Befehl                    | Beschreibung                                                                     |
|------------|---------------------------|----------------------------------------------------------------------------------|
| NXP        | [next_part](#next_part)   | Gibt zurück, welches Teil als nächstes mit dem linken Arm gegriffen werden soll  |
| GRP        | [grab_point](#grab_point) | Gibt zurück, an welchen Koordinaten das derzeitige Teil gegriffen werden soll und wie der Greifarm sich drehen muss   |
| NAP        | [nail_point](#nail_point) | Gibt zurück, an welchen Koordination zwei Teile zusammengenagelt  werden sollen  |

#### next_part

| Position | Parameter | Beschreibung                                                   |
|----------|-----------|----------------------------------------------------------------|
| 0        | arm       | Kann die Werte `left` oder `right` annehmen.                   |
|          |           |                                                                |
|          | return    | Die ID eines Bauteils oder `None`, falls Montage abgeschlossen |

##### grab_point

| Position | Parameter | Beschreibung                         |
|----------|-----------|--------------------------------------|
|          |           |                                      |
|          | return    | X und Y Offset um sich zum Greifpunkt zu bewegen und Rotations-Offset um das Teil gerade zu greifen|

##### nail_point

| Position | Parameter | Beschreibung                         |
|----------|-----------|--------------------------------------|
|          |           |                                      |
|          | return    | X und Y Koordinaten des Greifpunktes |

### Fehlermeldungen

| Bezeichner | Fehler          | Beschreibung                                    |
|------------|-----------------|-------------------------------------------------|
| eunc       | unknown command | Das letzte eingehende Kommando existiert nicht  |
| einc       | invalid command | Der Inhalt des Kommando wurde nicht verstanden  |
| eint       | internal error  | Bei der Verarbeitung ist ein Fehler aufgetreten |
