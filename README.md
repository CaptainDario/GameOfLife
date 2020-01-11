# gameOfLife

ModSim2019/2020 Projekt

Mitglieder:
* Louis Donath 798279


Ziele:

* Spiel
    * Spielbrett:
        * Grid (unedliche Generieung, wenn die Objekte sich bewegen)
        * auswaelbarer Startkonfig ✓
    * Regeln (wikipedia): ✓
        * Eine tote Zelle mit genau drei lebenden Nachbarn wird in der Folgegeneration neu geboren. ✓
        * Lebende Zellen mit weniger als zwei lebenden Nachbarn sterben in der Folgegeneration an Einsamkeit. ✓
        * Eine lebende Zelle mit zwei oder drei lebenden Nachbarn bleibt in der Folgegeneration am Leben. ✓
        * Lebende Zellen mit mehr als drei lebenden Nachbarn sterben in der Folgegeneration an Überbevölkerung. ✓
    * evtl. Ende
    * Zoomen (Raster vergroessern/verkleinern)
    * bewegen (auf dem Raster hin und her bewegen):
        * unedliche Spielbrett Generierung  
 
* User interface:
    * Tutorial
    * Menu ✓
 
* Performance:
    * Multithreaded Generationsberechnung
