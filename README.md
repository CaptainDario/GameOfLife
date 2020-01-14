# gameOfLife

ModSim2019/2020 Projekt

Mitglieder:
* Louis Donath 798279


Eine Implementierung von Conway's "Game of Life".

Ziele:

* Spiel:
    * Spielbrett:
        * Grid (unedliche Generieung, wenn die Objekte sich bewegen)
        * auswaelbarer Startkonfig ✓
    * Regeln (wikipedia): ✓
        * Eine tote Zelle mit genau drei lebenden Nachbarn wird in der Folgegeneration neu geboren. ✓
        * Lebende Zellen mit weniger als zwei lebenden Nachbarn sterben in der Folgegeneration an Einsamkeit. ✓
        * Eine lebende Zelle mit zwei oder drei lebenden Nachbarn bleibt in der Folgegeneration am Leben. ✓
        * Lebende Zellen mit mehr als drei lebenden Nachbarn sterben in der Folgegeneration an Überbevölkerung. ✓
    * Zoomen (Raster vergroessern/verkleinern) ✓
    * bewegen (auf dem Raster hin und her bewegen):
        * auf dem spielfeld hin- und her bewegen ✓
        * unedliche Spielbrett Generierung (wenn Grenzen erreicht?)
 
* UI:
    * (Tutorial)
    * Main menu:
        * board laden
        * zufaelliges board
        * selber board erstellen board
    * Menubar:
        * play/pause ✓
        * neues Spiel button 
        * einen Schritt-weiter-button
        * zoom in/out button ✓
        * neues Spiel Button
 
* Performance:
    * Multithreaded Generationsberechnung
 
* PyInstaller executable:
    * windows
    * Linux 
    * MacOS
