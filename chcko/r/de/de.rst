.. raw:: html

    %path = "Abfrageberechtigungen"
    %kind = kinda["Meta"]
    %level = 0 
    <!-- html -->

.. role:: asis(raw)
    :format: html latex


Eine Ebene des Datenschutzes ist über die IDs.
Wie die IDs sich mit den realen Dingen verknüpfen ist nur dir bekannt.
Du könntest Anfangsbuchstaben oder Endbuchstaben der Namen verwenden,
zufällige Zeichen hinzufügen oder eine andere Art Verdunkelung machen,
welche nicht einer einfachen Zuordnung für dich entgegensteht.

Alle nicht registrierten Benutzer fallen in eine Benutzerkategorie. 
Deshalb können alle nicht registrierten Benutzer die gemachten Übungen
aller anderen nicht registrierten Benutzer abfragen.

Wenn du dich registrierst und Instanzen
Schule, Periode, Lehrer, Klasse und Student anlegst,
dann sind diese mit dir verknüpft.
Dann kannst du alle Instanzen unterhalb deiner Instanz abfragen.

| Schule
|     n Perioden
|         n Lehrer
|             n Klassen
|                 n Studenten
    

Zum Beispiel

- Wenn eine Lehrerrolle dir gehört, d.h. du sie angelegt hast, dann kannst du
  mit eine ``done`` Abfrage die gemachten Übungen von Klassen und Studenten abfragen,
  welche die gleichen IDs von Schule bis einschließlich Lehrer haben wie dein Kontext,
  auch wenn sie anderen Benutzern gehören.

- Ein Direktor einer Schule könnte eine Schule-ID anlegen.
  Wenn alle Lehrer diese benutzen, dann kann der Direktor die ganze Hierarchie abfragen.

Wenn du andererseits eine Abfrage startest einer Instanz die nicht dir 
gehört, dann wirst du Instanzen darunter nicht sehen, auch wenn dort Instanzen sind,
die dir gehören.

In ``/<sprache>/done?<schule>&<periode>&<lehrer>&<klasse>&<student>&<problem>``
kannst du IDs nach ``?`` weglassen. ``/<sprache>/done?aclass&*&d>2`` würde alle
Übungen abfragen von allen Student der Klasse ``aclass``, die nicht älter als 2
Tage sind.
Damit das funktioniert, muss ``aclass`` dir gehören.
Wenn ``aclass`` nicht dir gehört, aber die Lehrer ID darüber schon,
dann kannst du mit ``/<sprache>/done?ateacher&aclass&*&d>2`` trotzdem alle
Schüler in ``aclass`` abfragen.

