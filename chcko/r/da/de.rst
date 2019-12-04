.. raw:: html

    %path = "Ideen"
    %kind = kinda["Meta"]
    %level = 0
    <!-- html -->

.. role:: asis(raw)
    :format: html latex


- Jeder Inhalt hat eine eindeutige ID = ID_Author.ID_Inhalt.
  Auf diese weise ist keine Koordination für die IDs von Inhalten notwendig.

- Jeder ID entspricht ein Verzeichnis 

  - ID_author

      - ID_content1
      - ID_content2
      - ...

- IDs sollen so kurz wie möglich sein. Deshalb entstehen sie 
  am besten durch Durchnummerierung mit a-z.

    - Ziffern können nicht verwendet werden, da sie keine Python IDs sind.
    - Großbuchstaben würden im Windows Verzeichnissystem nicht unterschieden werden.

- Jedes Inhaltsverzeichnis enthält Python Code und Sprachdateien.

    - einen Pythonteil (``__init__.py``), um gegebene Werte von Übungen
      zufällig zu generieren (nicht notwendig für statische Inhalte).

    - Sprachdateien (Vorlagen zur Generierung von HTML (template)) 
      (``en.html``, ``de.html``, ``it.html``, ``fr.html``,...) 
      ``en.html`` sollte immer vorhanden sein als Ausgangspunkt für weitere Übersetzungen. 

    - ein statischer off-line Schritt ist möglich, um Inhalt aus anderen Formaten
      zu generieren, derzeit von Restructured Text (.rst) mit Sphinx.
      Das ermöglicht es Sphinx Erweiterungen wie ``tikz`` and ``texfigure`` (``tex``,
      ``tikz``, ``chemfig``, ...) für Graphiken zu Verwenden.

- Der Kontextpfad zu Übungen und Schlüsselwörter sind sprachspezifisch
  und deshalb in den Sprachdateien enthalten.

- Mehrere Übungen kann man in einer URL / HTTP Anfrage kombinieren
  und somit über eine URL einen umfangreicheren Arbeitsauftrag erteilen.
  (``content`` Abfrage).

- Übungen/Inhalte können andere Inhalte referenzieren oder einfügen,
  letzteres über den Vorlagen-Mechanismus (Templates).

- Antworten zu Übungen werden in einer Datenbank gespeichert und
  beim laden mit den Texten in den jeweiligen Sprachen vereint.

- Eine Studentenrolle ist gegeben durch einen ID-Pfad / eine Hierarchie::

  Schule 1-n Periode 1-n Lehrer 1-n Klasse 1-n, Student

- Durch diese Hierarchie hat ein Lehrer einen schnellen Zugriff
  auf die gemachten Übungen seiner Klassen und Schüler über eine URL Abfrage.

- Lehrer können ihren Klassen und Schülern Arbeitsaufträge erteilen,
  welche diese über "Aufträge" (``todo`` Abfrage) sehen.

- Lehrer können sehen, welche Übungen ihre Schüler schon gemacht haben
  (``done`` query).

- Benutzer bekommen anfangs einen Kontext mit generierten IDs.
  Sie können sich aber dann eigene machen (``edits`` Abfrage).
  (Benutzer können sich eine Farbe aussuchen,
  um leichter zu erkennen in welchem Kontext sie sich befinden).

- Registrierte Benutzer können mehrere Kontexte verwalten 
  und zwischen ihnen wechseln (``contexts`` Abfrage).
  Eine Registrierung geht auch mit Google, Twitter, Facebook or LinkedIn.

