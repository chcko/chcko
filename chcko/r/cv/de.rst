.. raw:: html

    %path = "Mathematik/Entropie"
    %kind = kinda["Texte"]
    %level = 12
    <!-- html -->

Um exklusiv ein Element v (Wert, Zustand, Punkt) von einer Variablen V 
(Kardinalität `|V|=n`, n-Menge) auszuwählen, braucht es `\log_bn` b-Mengen 
(normalerweise `b=2`, bit).

.. math::

    I(V)=log\;n

`I(V)` ist die Breite der Variable, d.h. die Informationsmenge (Anzahl von bits), 
die es braucht, um Werte von V auszuwählen. `I` ist gleich für alle Werte von V.
`I` bezieht sich auf die Variable.

.. admonition:: Zufallsvariable, Variate, Variable

    Im Englischen gibt es Variate für Zufallsvariable (random variable).

    Oft ist diese Unterscheidung zwischen Zufallsvariable und Variable nicht
    notwendig. Beides meinen hier die reale Größe mit Werten, die wiederholt
    auftreten können.

Wenn man jeden bekannten Auftritt (Verweis, Ereignis) `c \in C` der
Werte von `V` betrachtet, dann ist das ein zusätzlicher Weg, um auf die
Werte von `V` zu verweisen.  Man wählt zuerst einen beliebigen Auftritt aus
mit `I(c)=\log |C|` und subtrahiert davon die Auswahl eines Auftritts eines
bestimmten Wertes `v` (`I(c_v)=\log |C_v|`).  `\frac{|C|}{|C_v|}` ist die
Anzahl von `|C_v|` großen Untermengen von `C`.  Um einen solchen Untermenge einmal
auszuwählen braucht es 

.. math:: 

    I(v)=\log\frac{|C|}{|C_v|}=-\log\;p(v)

`I(v)` ist für jedes `v\in V` anders und stellt den optimalen Code dar 
(Entropie Code, Huffman code).

Die durchschnittliche Codebreite ist 

.. math::
    I(V)=-\sum_vp(v)\log\;p(v) 
    
`I(V)` ist die **Entropie** der Variablen `V` (und nicht eines Wertes von `V`).

Wenn für alle `v` `p=\frac{1}{n}` ist, dann sind erhält man wieder `I(V)=log\;n`.

Die Information in einer Variablen hängt von der Wahrscheinlichkeitsverteilung
der Wertauftritte (= Wahrscheinlichkeitsereignis) ab.



