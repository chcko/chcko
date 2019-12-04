.. raw:: html

    %path = "Versuch in der Klasse"
    %kind = kinda["Meta"]
    %level = 0 
    <!-- html -->

.. role:: asis(raw)
    :format: html latex


Um es in der Klasse zu probieren, müssen der Lehrer und 
die Schüler sich nicht notwendigerweise registrieren.

Schritt-für-Schritt für jeden in der Klasse:

- Der Lehrer denkt sich IDs für Schule, Periode, Lehrer (d.h. für sich), 
  Klasse und jeden Student aus. Die IDs müssen zusammenpassen,
  d.h. alle Schüler der Klasse haben die gleiche ID für Klasse, Lehrer, ...

- Der Lehrer zuerst, dann die Schüler: 

    - http://mamchecker.appspot.com/de öffnen
    - zu ``Änderungen`` (oben links) gehen
    - seine IDs eingeben.  Der Lehrer ist auch ein
      Student, er kann aber das Feld Student auch leer lassen.
    - Auf [OK] drücken.

- Alle Studenten machen eine Übung (z.B. ``/de/?r.bu`` in der Adresszeile eingeben).

- Der Lehrer gibt in der Browseradresszeile die URL ``/de/done?<classId>&*&*`` ein.
  Von rechts nach links heißt die Abfrage:
  
    - alle Übungen (``*``)
    - von allen Studenten (``*``)
    - von der Klasse ``<classID>``. Die tatsächliche ID der Klasse verwenden.

Der Unterschied zum registrierten Benutzer: 
Im nicht registrierten Fall kann jeder Schüler Lehrer spielen,
und anderen Aufgaben geben oder die Ergebnisse abfragen
(weiters dazu in :lnk:`r.de`).


