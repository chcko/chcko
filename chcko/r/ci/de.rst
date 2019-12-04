.. raw:: html

    %path = "Mathematik/Zahlen/NZQR lang"
    %kind = kinda["Texte"]
    %level = 9
    <!-- html -->

.. contents::

Das folgende ist keine erste Einführung, sondern 
eine Art Diskussion zur Interpretation von Zahlen mit weiterführenden Links
und mit Augenmerk auf Algorithmik (:lnk:`r.cp`).

Natürliche Zahlen (`\mathbb{N}`)
--------------------------------

Die natürlichen Zahlen sind die eigentlichen Zahlen im Sinne, 
dass sie eine Anzahl darstellen. 
Alle anderen Zahlenmengen meinen mehr als nur die Anzahl.

Eine **Anzahl** ist eine reale Variable, welche die Mächtigkeit (**Kardinalität**)
einer anderen Menge angibt. Ein Wert dieser Variable, etwa drei, meint drei
Dinge.  Weitere Eigenschaften werden nicht betrachtet, werden weg-abstrahiert.
Deshalb kann jede natürliche Zahl als **Äquivalenzklasse** (:lnk:`r.co`) 
angesehen werden.

.. admonition:: Hinweis

    Die Mathematik unterscheidet noch genauer: **Kardinalzahlen** wie eben
    und **Ordinalzahlen** zum Bezeichnen einer Ordnung.

Die intuitive Vorstellung von `\mathbb{N}` wird mit den
`Peano Axiomen <http://de.wikipedia.org/wiki/Peano-Axiome>`_
formalisiert.

.. admonition:: Hinweis

    Im Essentiellen ist `\mathbb{N}` eine Konstruktion 
    einer geordneten Vielheit (0 mit Nachfolgern), 
    um damit Werte anderer Variablen (etwa eben Anzahl)
    zu addressieren oder darzustellen, nach Art wie Wörter Konzepte darstellen.

Null 
....

Die Null war eine großartige Erfindung zur Darstellung der Zahlen, die im
römischen Zahlensystem noch nicht da war. Allgemeiner kann man dadurch
Variablen einbeziehen, auch wenn sie nicht immer vorkommen. Das ermöglicht oft
eine allgemeinere Beschreibung. Zum Beispiel ist in 103 der positionscodierte
Zehner da, obwohl keine Zehnergruppierung da ist (:lnk:`r.cn`).
Ein anderes Beispiel sind Vektoren. (:lnk:`r.cg`).

Die ganzen Zahlen `\mathbb{Z}` und die Addition
-----------------------------------------------

`\mathbb{Z}` ist mehr als nur Anzahl.

Als Motivation für die ganzen Zahlen kann man bei `\mathbb{N}`
mit der Anzahl einen Vorgang oder eine Richtung verbunden denken.
2 ist dann nicht nur die Anzahl 2 sondern Anzahl `+` Hinzufügen
(`2 = {2,+} = +2`).

Wenn man sich `\mathbb{N}` als Anzahl kombiniert mit Vorgang
oder Richtung vorstellt, dann braucht man den Umkehrvorgang oder die Gegenrichtung,
um wieder zur Ausgangssituation zurückzukommen.
Man ist damit intuitiv bei den ganzen Zahlen `\mathbb{Z}` gelandert.

`+` meint dazugeben, `-` meint wegnehmen. Die Richtung ist aber Definitionssache.
Das `+` wird oft weggelassen, aber man sollte es hinzudenken, 
da eine ganze Zahl eben nicht nur eine Anzahl ist,
sondern Anzahl und Vorgang/Richtung zusammen. 

Wenn man sich unter `\mathbb{N}` nur Anzahl vorstellt, dann ist
`\mathbb{Z}=\mathbb{N}\times\{+,-\}`. Dann ist `\mathbb{N}` keine Teilmenge
von `\mathbb{Z}`, aber eine 
`isomorphe <http://de.wikipedia.org/wiki/Homomorphismus#Universelle_Algebra>`_
`Einbettung <http://de.wikipedia.org/wiki/Einbettung_(Mathematik)>`_.

.. admonition:: Hinweis

    Eine Einführung von `\mathbb{Z}`, die versucht ausgehend von `\mathbb{N}` 
    möglichst wenig neue Objekte zu verwenden, eben auch kein `+` und `-`, ist die 
    über **Äquivalenzklassen** (:lnk:`r.co`) von Zahlenpaaren `(n,m)` aus 
    `\mathbb{N}` mit der Äquivalenzrelation `(n_1,m_1)\sim(n_2,m_2)\equiv n_1+m_2=n_2+m_1`.
    In der kanonischen Darstellung ist eine Zahl des Paares 0.
    `+2 = (2,0)` und `-2 = (0,2)`.

Mit `+` und `-` als Vorgänge kann man sich die *Addition* algorithmisch als eine Sequenz denken:
das hintereinander Ausführen von Hinzugeben oder Wegnehmen.
`+2+(-2)` heißt 2 hinzugeben und dann 2 wegnehmen.
Vertauscht `((-2)+(+2))` erhält man das gleiche Ergebnis (**Kommutativgesetz**).
Bei mehreren Zahlen kann frei entscheiden, was man zuerst berechnet
`(-2)+((+2)+(+3))=((-2)+(+2))+(+3)` (**Assoziativgesetz**).

.. admonition:: Hinweis

    Die Subtraktion 2-2 ist eine Kurzschreibweise für +2+(-2).

Das Ergebnis von +2+(-2)= 0, das **neutrale Element** der Addition.
+2 ist die **Gegenzahlen** (inverses Element der Addition) von -2 und umgekehrt.
`(\mathbb{Z},+)` ist ein **abelsche Gruppe** (:lnk:`r.cl`).

.. admonition:: Hinweis

    `+` als Teil der Zahl und `+` als binäre Operation meinen nicht dasselbe,
    ebenso für `-`. `-` kann zusätzlich als unitäre Operation (Funktion) angesehen werden,
    welche die Gegenzahl liefert.

Die ganzen Zahlen `\mathbb{Z}` und die Multiplikation
-----------------------------------------------------

Einen Vorgang kann man wiederholen.  Die Multiplikation gibt an, wie oft das
Hinzugeben (+2) oder Wegnehmen (-2) wiederholt wird.  Multiplikation stellt
also algorithmisch eine Schleife dar:

    `3\cdot(-2) = (-2)+(-2)+(-2)`

Die Multiplikation mit 1 heißt einmal wiederholt, also das Ding selbst und unverändert.
1 ist das **neutrale Element** der Multiplikation.

Der Multiplikation mit -1 gibt man die Bedeutung: Umkehrung des wiederholten Vorgangs,
d.h. aus hinzu (+) mach weg (-).

    `(-1)\cdot(-2) = +2`

    `(-1)\cdot(-1)\cdot(-2) = -2`

Damit kann man jede ganze Zahl mit jeder anderen ganzen Zahl multiplizieren und es kommt 
wieder eine ganze Zahl heraus, d.h. eine Anzahl die man hinzugibt oder wegnimmt.
`(\mathbb{Z},\cdot)` ist bezüglich der Multiplikation **abgeschlossen** und es gilt das 
**Assoziativegesetz**.

`(\mathbb{Z},+,\cdot)` ist ein **Integritätsring** (:lnk:`r.cm`).

`(\mathbb{N},+,\cdot)` alleine ist nur ein **Halbring** (:lnk:`r.cm`) .


Die Multiplikation und die Rationalen Zahlen (`\mathbb{Q}`) 
-----------------------------------------------------------

Analog zu `\mathbb{Z}=\mathbb{N}\times\{+,-\}` kann man sich 
das Wiederholen/Vervielfachen vereint mit der Anzahl als neues Element denken. 
Dann ist es naheliegend, dass man diesen Vorgang umkehren möchte.

Welches Wegnehmen muss ich 3 mal wiederholen, damit (-6) herauskommt?:

    (-6)/3 = -2

Analog zu `\mathbb{Z}=\mathbb{N}\times\{+,-\}` kann man über
`\mathbb{N}\times\{\cdot,\div\}` mit Anzahl Multiplikation und Division vereinen.

Beides sind unterschiedliche Mengen.  Man muss also grundsätzlich die binären
Verknüpfungen `\cdot` und `+` getrennt behandeln.  Nur das
**Distributivgesetz** vereint die beiden: 

    `a\cdot(b+c) = a\cdot b + a\cdot c`

    z.B. `2\cdot(3+4)=2\cdot 3+2\cdot 4=14`

Wenn man im speziellen nach dem Teil sucht, der wiederholt (multipliziert)
nichts verändert, also 1 ergibt, so kommt man auf den **Kehrwert** (**Reziprok**) und
der meint die UmKEHRung des Wiederholens, das **inverse Element der Multiplikation**.

Während bei (-6)/3 noch eine ganze Zahl herauskommt, d.h. ein Vielfaches von 1,
ist das beim Kehrwert nicht mehr der Fall.

Es ist naheliegend die Wiederholungen mit deren Umkehrungen zu erweitern. 
Dieser Schritt kann in Analogie zur Erweiterung von `\mathbb{N}` auf `\mathbb{Z}` gesehen werden.

- Dort wurde der Vorgang "hinzu" mit der Anzahl vereint zum Paar (Anzahl,hinzu).
  "hinzu" hat eine Umkehrung, dem "weg".
  Man hat (Anzahl,weg) erweitert.

- In `\mathbb{Q}` erweitert man (Anzahl,vervielfachen) mit *Kehrzahlen* (Anzahl,teilen).

.. admonition:: Hinweis

    Man könnte `\mathbb{Q}`-Elemente analog zu `\mathbb{N}\times\{+,-\}`
    schreiben: 

    - `\cdot 2` entspräche +2 und 
    - `\div 2` entspräche -2

    Die binäre Verknüpfung `\cdot` ist wieder nur Hintereinander-Ausführen und kann weggelassen werden

    `(\cdot 2)\cdot(\div 2) = \cdot 2\div 2 = 1`

    Stattdessen wird

    - `2\cdot 2^{-1} = 1` oder
    - `2\cdot \frac{1}{2} = 1`

    geschrieben, ersteres, weil man die Hochzahlen bei gleicher 
    Basis addieren kann und somit `2\cdot 2^{-1}=2^1\cdot 2^{-1}=2^{1-1}=2⁰=1` ist.


`(\mathbb{Q},\cdot)` ist eine **abelsche Gruppe** mit dem neutralen Element 1.

Weil jede Multiplikation in `(\mathbb{Q},\cdot)` ein Ergebnis in
`(\mathbb{Q},\cdot)` liefern soll (Abgeschlossenheit), nimmt man alle Brüche
`p/q=pq^{-1}` in `(\mathbb{Q},\cdot)` auf.  
3/2 heißt, dass man zuert `\cdot 3` und dann `\div 2` (Kehrwert von 2) macht.

    `\frac{3}{2}=3\cdot 2^{-1}=3\frac{1}{2}=\frac{1}{2}\cdot 3=2^{-1}\cdot 3`

`pq^{-1}` bedeutet, dass man p mal vervielfacht und dann q mal teilt. 
Wenn man zusätzlich eine gleiche Anzahl r mal wiederholt und dann wieder r mal teilt, 
ändert sich nichts 

    `pq^{-1}=rr^{-1}pq^{-1}=rp(rq)^{-1}=\frac{rp}{rq}`

Alle solche Zahlen sind äquivalent und die kanonische Darstellung ist die mit p und q teilerfremd.

.. admonition:: Hinweis

    `\mathbb{Q}` wird formal über Äquivalenzklassen 
    solcher gleichwertiger Zahlenpaare eingeführt:
    `(n_1,n_2)\sim(n_2,m_2)\equiv n_1m_2=n_2m_1`.


`\mathbb{R}` als Erweiterung mit den irrationalen Zahlen `\mathbb{I}`
---------------------------------------------------------------------

Anzahl (`\mathbb{N}`) mit Hinzugeben (+) und Wegnehmen (-) ist `\mathbb{Z}`.
`\mathbb{Z}` mit Wiederholen (`\cdot`) und Teilen (`\div`) führt zu `\mathbb{Q}`.
Wenn wir bei `+,-,\cdot,\div` bleiben, kommen wir gut mit `\mathbb{Q}` aus.

Soll die Operation des Potenzierens umkehrbar sein, muss man wieder erweitern,
da es sich herausstellt, dass es
z.B. kein `p/q` in `\mathbb{Q}` gibt, für das `p^2/q^2=2` ist. 
(Beweis: p/q teilerfremd. Wenn `p^2` gerade, dann auch p. Also `p=2n`, womit
`p^2=4n^2=2q^2` und damit q gerade, was ein Widerspruch ist).

Es gibt aber **Algorithmen**, die rationale Zahlen erzeugen (**Zahlenfolge**),
deren Quadrate immer näher an 2 heranreichen.
Es gibt mehrere solcher Algorithmen, also mehrere Zahlenfolgen, deren **Grenzwert** 2 ist.
Alle zusammen werden als Äquivalenzklasse angesehen.

Die irrationalen Zahlen `\mathbb{I}` besteht aus Äquivalenzklasse von Zahlenfolgen. 
Durch Angabe des Algorithmus, und mit `\sqrt{}` meint man so einen Algorithmus, 
ist die irrationale Zahl bestimmt. 
Man kann eine irrationale Zahl nicht als Dezimalzahl schreiben.
Man kann den Algorithmus auch nie vollständig ausführen, denn der endet nie.
Damit ist die irrationale Zahl wirklich dieser Algorithmus.

Die irrationalen Zahlen werden noch unterteilt in **algebraische** irrationale Zahlen, 
eben solche die mit potenzieren zu tun haben,
und den **transzendente** irrationale Zahlen. 
Letztere gibt es, weil es nicht nur Potenzieren gibt, sondern viele andere Abhängigkeiten, 
etwa Sin, Cos, ... 

Neue Operationen/Funktionen führen zu neuen Zahlen.  Mit den irrationalen
Zahlen als **Äquivalenzklasse von Zahlenfolgen** hat man aber eine Definition,
die so allgemein ist, dass alle algebraischen und auch alle transzendenten
Zahlen und auch `\mathbb{Q}` mit eingeschlossen sind.  

    `\mathbb{R} = \mathbb{Q} \cup \mathbb{I}`

Eine andere sehr brauchbare und faszinierende Erweiterung sind die Komplexen Zahlen `\mathbb{C}` (:lnk:`r.di`).

.. admonition:: Hinweis
    
    Da `\mathbb{R}` unendliche Zahlenfolgen sind, könnte man auch `\infty` und
    `-\infty` als Zahlen mit aufnehmen, wären da nicht `\infty+1=\infty` und dergleichen. 
    Nichtsdestotrotz wird in der komplexen Analysis (Funktionentheorie) 
    `\mathbb{C}` mit `\infty` fruchtbar erweitert. 


