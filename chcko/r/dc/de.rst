.. raw:: html

    %path = "mitmachen"
    %kind = kinda["Meta"]
    %level = 0
    <!-- html -->

.. role:: asis(raw)
    :format: html latex

Voraussetzungen
---------------

Zum mitmachen brauchst du folgendes Wissen

- etwas HTML
- etwas Python (mit numpy und sympy)
- möglicherweise Javascript 
- grundsätzliches Verständnis der verwendeten SW Tools.

Software
--------

Wenn du etwas Vertraut mit Linux bist, verwende es, vielleicht mittels
eines virtuellen PCs wie etwa `Virtualbox <https://www.virtualbox.org/wiki/Downloads>`_. 
Dann kannst due ``git`` und die andere SW mit weniger Problemen betreiben
(z.B. einfache Installation mit Packetmanagern, Unterstützung von Symlinks, ...).
Aber auch unter Windows und Mac gibt es alle notwendigen Tools.

Zur Zusammenarbeit wird `github <https://github.com/mamchecker>`_ verwendet.
Die Übungen enthalten Python Code (auch in den Templates),
weshalb eine Handhabung wie Code, angebracht ist.
Dass ein zweiter den Code überprüft, ist aus Sicherheitsgründen notwendig.

Auf deinem PC brauchst du

- `Git <http://rogerdudler.github.io/git-guide/>`_ 
  (`msys git <http://msysgit.github.io/>`_ unter Windows).
  `Einleitung <http://git-scm.com/book/en/Getting-Started-First-Time-Git-Setup>`_

- `Python <http://www.python.org/download/releases/2.7/>`_  
  mit `pip <http://stackoverflow.com/questions/4750806/how-to-install-pip-on-windows>`_
  (Python 3 wird von Google Appengine noch nicht unterstützt.)

- `Google Appengine <https://developers.google.com/appengine/downloads>`_

- `Doit <http://pydoit.org/>`_ (``pip install doit``)

- `Pytest <http://pytest.org/latest/>`_ zum Testen (``pip install pytest``)

und optional

- `Sphinx <http://sphinx-doc.org/latest/install.html>`_,
  wenn du Restructured Text (rst) verwenden willst.
  (``pip install sphinx``). 
- Latex (use `miktex <http://miktex.org/>`_ unter Windows) für sphinx plugins
  (`sphinxcontrib.tikz <https://bitbucket.org/philexander/tikz>`_,
  `sphinxcontrib.texfigure <https://bitbucket.org/prometheus/sphinxcontrib-texfigure>`_).

- `Coverage <http://nedbatchelder.com/code/coverage/>`_ (``pip install coverage``)

Als Browser hat Chrome die beste `HTML5 <http://html5test.com/results/desktop.html>`_ 
Unterstützung und eine gute Umgebung zum Debuggen von Javascript.

Zum editieren verwende einen Texteditor deiner Wahl. 
Er sollte es ermöglichen ausgewählten Code auszuführen 
(`Pydev <http://pydev.org/manual_adv_interactive_console.html>`_, `Vim <http://www.vim.org/>`_).

Einsteigerhilfe
---------------

Fork auf github.

    - Verwende deinen Browser, um Mamchecker auf github zu verzweigen (fork).

    - Im Terminal (msys bash unter Windows) auf deinem PC mache ``git clone`` auf
      das 'geforkte' Mamchecker, um es auf ein lokales Verzeichnis zu übertragen::

          git clone --recursive https://github.com/mamchecker/mamchecker.git

      Wenn du nicht `--recursive <http://stackoverflow.com/questions/3796927/how-to-git-clone-including-submodules>`_ 
      verwendet hast, dann must du anschließend 
      `git submodule update --init --recursive <http://stackoverflow.com/questions/9493645/fork-github-repo-with-submodules>`_
      machen.

Trage dich als Author ein.

    - Trage dich selbst als Author mit einer ``author_id`` in den Sourcen unter ``authors.yaml`` ein.
      ``default_lang: de`` beeinflusst die ``doit`` Befehle weiter unten.

    - Erstelle eine Verzeichnis (parallel zum existierenden ``r`` Verzeichnis) mit 
      der Authoren-ID als Name (Authorenverzeichnis).

Füge Übungen hinzu. Um zu sehen, wie einfach das ist, schau dir die Beispiele im ``r`` Verzeichnis an.

    - Füge ein Verzeichnis unter dem Authorenverzeichnis hinzu
      und erstelle dort ``__init__.py``, ``en.html``, ``de.html``, ...
      then edit. Verwende dazu ``doit``; 
      es generiert die nächste ID und verwendet sie zum Erzeugen des Übungsverzeichnisses 
      (siehe ``nextids.yaml`` und ``dodo.py``):

      - ``doit -kd. new`` erzeugt ein Übungsverzeichnis.
        Dort kannst du manuell die anderen Dateien erzeugen.
      - ``doit -kd. problem`` erzeugt ein Übungsverzeichnis und dort
        ``__init__.py`` und ``<default_lang>.html``.
        Füge ``en.html`` und möglicherweise andere Sprachdateien manuel hinzu. 
        Entferne ``__init__.py``, wenn es keinen Code braucht.
      - ``doit -kd. rst`` erzeugt ein Übungsverzeichnis und ``<default_lang>.rst``. 
        Nach dem Editieren wandelt ``doit -kd. html`` diese in eine HTML Template Datei um.
        Generierte Dateien fangen mit einem Unterstrich ``_`` an,
        Sphinx generiert z.B. ``_de.html`` von ``de.rst``.

    - ``__init__.py`` enthält die Funktionen ``given`` und ``calc`` und
      optional ``norm``, ``equal``, ``points`` und ``names``.
      (siehe ``from_py`` in ``hlp.py`` und Beispiele im ``r``-Verzeichnis).

    - ``<sprache>.html`` ist HTML und mit ``{{'{{}}'}}`` umgebener oder mit ``%``
      anfangende Python Code (`SimpleTemplate <http://bottlepy.org/docs/dev/stpl.html>`_).
      Verwende auch das templates ``getorshow`` wie in den Beispielen im ``r``-Verzeichnis.
      Das generierte HTML wird dann mit einem ``<div>`` umgeben werden 
      (siehe ``inc`` in ``util.py``).

    - In ``<sprache>.rst`` kann man ``inl`` zum Einfügen (inlining) anderer Übungen
      und ``lnk`` zum referenzieren verwenden 
      (siehe ``inl.py`` und Beispiele im ``r``-Verzeichnis).

    - Die ersten Zeilen der Sprachdateien sind folgende, wobei

      - ``<kind>`` ein sprachspezifische Zeichenkette aus ``kind.py`` ist
      - ``level`` als letztes kommt und das Schuljahr beginnend von Grundschule meint (1, 2, ... )

      for ``<lang>.rst``::
        |
        |    .. raw:: html
        |
        |        %path = "pfad/um/hierarchische/Ordnung/zu/erzeugen"
        |        %kind = kinda["<kind>"]
        |        %level = 0
        |        <!-- html -->
        |
        |    .. role:: asis(raw)
        |        :format: html latex

      for ``<lang>.html``::
        |
        |    %path = "path/to/create/a/hierarchical/order"
        |    %kind = kinda["<kind>"]
        |    %level = 9

    - Von oberhalb dem Verzeichnis, wo app.yaml ist, 
      rufe ``dev_appserver mamchecker`` auf
      und teste deine Übung mit dem Browser (``http://localhost:8080/de/?<yourid>.<problemid>``).
      Gib dazu unsinnige Eingaben ein, fast korrekte und korrekte.

Mach dich bereit für das ``commit``:

    - ``doit -kd. initdb`` muss man ausführen, um ``initdb.py`` zu generieren,
      welche die Inhaltsübersicht erzeugt.

    - In deiner lokalen Kommandozeile im Mamchecker Verzeichnis mache
      
      - ``git status``
      - ``git diff``
      - ``git commit -am "in english write what you did"`` 
      - ``git push`` um die Änderungen auf dein github fork zu übertragen.


    - Es gibt eine Test Script das du lokal ausführen kannst. 
      In der Kommandozeile wo ``dodo.py`` liegt, mache: 
      
        - ``doit test``.

      Das testet mehr als notwendig ist, wenn du nur eine Übung hinzugefügt hast.
      Aber mache es, wenn du sonstige Änderungen im Code gemacht hast.

Füge deinen Betrag zur Sammlung hinzu.

    - In deinem Browser kannst du einen **pull request** erzeugen,
      damit alle Beiträge zusammen kommen.

