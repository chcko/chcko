.. raw:: html

    %path = "URL-Abfragen"
    %kind = kinda["Meta"]
    %level = 0
    <!-- html -->

.. role:: asis(raw)
    :format: html latex

URL
...

Das URL-Format ist ``../<sprache>/<seite>?<abfrage>``.

``<sprache>`` ist ``en``, ``de``, ... (siehe ``languages.py``).
Falls nicht angegeben, wird dein zuletzt verwendete Sprache genommen 
oder die Browsereinstellung herangezogen.

``<seite>`` ist eine von ``content`` (Inhalt), ``done`` (Erledigt), ``todo`` (Aufträge),
``edits`` (Änderungen) and ``contexts`` (Kontexte/Rollen).
``contexts`` ist nur für registrierte Benutzer zugänglich,
die mehrere Kontext/Rollen haben können. ``content`` wird verwendet, falls nicht angegeben.

``<abfrage>`` beginnt nach ``?`` und ist eine mit ``&`` getrennte Liste. 
Darin kann für alle Seiten
``School=<LLL>&Period=<DDD>&Teacher=<RRR>&Class=<SSS>&Student=<TTT>`` enthalten sein.

content (Inhalt)
................

Mit ``../<sprache>/content`` werden alle Inhalte aufgelisted.
Davon kann man mehrere Einträge auswählen.

``../de/content?r.a&r.by=2`` (``r.a`` is äquivalent zu ``r.a=1``) würde
eine deutsche Seite mit einer  ``r.a``-Übung und zwei ``r.by``-Übungen abrufen.
``../de/?r.a&r.by=2``, d.h. ohne ``content``, ergibt das gleiche.

Für registrierte Benutzer erlaubt eine solche Seite Klassen oder Schülern
mit gleichem Schule-Periode-Lehrer Präfix 
**Arbeitsaufträge** (assignments) zu geben.
Die Lehrerrolle des ausgewählten Kontexts muss jedoch dem Benutzer gehören, d.h.
von ihm erstellt worden sein.

Eine Übung besteht aus mehreren Fragen und jede Frage hat Punkte (1, falls
nicht angegeben).  Nach der Überprüfung gibt es am Anfang der Seite eine
Zusammenfassung von erreichten Punkten/mögliche Punkte zweimal, wovon einmal die nicht
ausgefüllten Felder nicht mitgezählt werden.

done (erledigt)
...............

``../<sprache>/done`` listed gemachte Übungen auf, mit Datum und Zeit
und ob richtig. Ein Link erlaubt zur Übung zu gehen oder sie nochmal zu machen.
Man kann ausgewählte Übungen löschen.

Die Abfrage

``../<sprache>/done?<schule>&<periode>&<lehrer>&<klasse>&<student>&<übung>`` 

erlaubt es 

- einen Studenten seine Übungen zu filtern. Dafür braucht er nur ``<übung>``.
- einen Lehrer die Übungen seiner Klassen oder Schüler zu sehen.

Von links werden nicht angeführte IDs mit denen vom aktuellen Kontext ersetzt.
Deslhalb braucht ein Student nur  ``<exercise>``, wenn überhaupt gefiltert werden soll.
``<..>`` sind Platzhalter für die tatsächlichen IDs. 

Für 'alle' kann man ``*`` verwenden.

Jeder Eintrag hat dieses Format:

    name|feld op wert[,feld op wert[,...]]

- ``name`` ist der Name des Datensatzes
- ``feld`` ist ein Feld (Variable) des Datensatzes

    Alle Datensätze haben einen Namen sowie ``userkey`` und ``created``.
    Schule, Periode, Lehrer und Klasse haben keine anderen Felder.
    Der Datensatz für Student hat zusätzlich ``color`` (Farbe).
    Problem hat zusätzlich ``query_string`` (abfrage), ``lang`` (sprache), 
    ``given`` (gegeben), ``created`` (erzeugt),
    ``answered`` (beantwortet), ``collection`` (Unterübungen), 
    ``inputids`` (IDs der Eingabefelder), ``results`` (Resultate), ``oks`` (richtige),
    ``points`` (Punkte), ``answers`` (Antworten), ``nr`` (Nummer).
    Die englischen Ausdrücke müssen verwendet werden.

- ``op`` besteht aus ``~=!<>``, wo ``~`` für ``=`` steht.
  Für das Alter (``answered``) der Übung kann man diese Abkürzungen verwenden::

    d=Tage, H=Stunden, M=Minuten, S=Sekunden

``1DK&*&d>3,d<1`` würde alle Übungen anzeigen, die von Studenten der Klasse ``1DK`` 
vor nicht mehr als 3 Tage (``d``) und mehr als einen Tag gemacht wurden.

.. admonition:: Tip

    Öfter gemachte Abfragen können als Lesezeichen gespeichert werden.

Registrierte Benutzer sind gegen Abfragen von anderen Benutzern und nicht registrierten
Benutzern geschützt.

todo (Aufträge)
...............

``../<sprache>/todo`` listet die Aufträge mit Datum und Zeit von Erhalt und Abgabe auf.

edits (Änderungen)
..................

``../<sprache>/edits`` ermöglicht es die IDs für 
Schule, Periode, Lehrer, Klasse, Student neu anzulegen, zu verändern oder zu löschen.
Für leer gelassene Felder werden die IDs ``myschool``, ``myperiod``, ``myteacher``,
``myclass`` und ``myself`` verwendet.

Werden alle IDs eines Kontextpfades schon verwendet, gibt es eine Meldung.
Werden Pfadpräfixe von anderen Verwendet erscheinen diese kursiv.
Diese anderen Benutzer können dein gemachten Übungen abfragen.


``Neu`` erstellt einen neuen Kontext.
``Ändern`` erstellt einen neuen Kontext, kopiert alle Übungen vom alten und löscht diesen.
``Löschen`` löscht den Kontext mit allen Übungen.

Die **Farbe** dient dazu, leichter zu erkennen, in welchem Kontext man sich befindet.

contexts (Kontexte)
...................

``../<sprache>/contexts`` listet alle Kontexte/Rollen des registrierten Benutzers auf.

Diese Kontexte/Rollen kann man auch über das Menü erreichen,
das aufklappt, wenn die Maus sich über der Studenten-ID befindet.
Über den Menüeintrag wird die aktuelle Seite mit dem neuen Kontext geöffnet.

