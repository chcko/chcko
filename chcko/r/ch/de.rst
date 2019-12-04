.. raw:: html

    %path = "Mathemtik/Folgen und Reihen"
    %kind = kinda["Texte"]
    %level = 10
    <!-- html -->


Folgen und Reihen
-----------------

Eine **Folge** ist eine Funktion der natürlichen Zahlen.

Die natürliche Zahl ist eine Methode, um auf die Glieder der Folge zu verweisen.
Sie heißt auch Index.

- `a_1` ist das erste Glied der Folge
- `a_2` ist das zweite Glied der Folge
- ...
- `a_n` ist das n-te Glied der Folge

Werden die ersten n Glieder einer Folge aufsummiert, 
dann ist das das n-te glied der Summenfolge oder **Reihe**.

Der Begriff *Funktion* bedeutet: 
Weiß ich das wievielte Glied, dann weiß ich die Zahl dort.

Viele Folgen haben eine Regelmäßigkeit, die es erlaubt sie viel kürzer zu beschreiben
(Kurze Beschreibung = geringe Komplexität).

arithmetische Folge
...................

Bei der arithmetischen Folge ergibt sich ein Glied der Folge aus dem
vorhergehenden durch Addieren einer gleichbleibenden Zahl.

`a_{n+1} = a_n + d`.

Das ist die **rekursive** Darstellung der arithmetischen Folge.

Um zum n-ten Glied zu kommen, wiederholt man das n-1 mal:

`a_n = a_1 + (n-1) d`

Das ist die **Termdarstellung** der arithmetischen Folge.

.. admonition:: Hinweis

    In vielen Programmiersprachen wird bei 0 gestartet, da man dann `nd` hat, statt `(n-1)d`.

Um eine gegebene Folge als arithmetische Folge zu erkennen, schaut man, ob die
Differenz aufeinanderfolgender Glieder gleich bleibt.

arithmetische Reihe
...................

Betrachtet man die Summe die ersten n Glieder, dann kann man eine Regelmäßigkeit erkennen,
und solche sind immer Anlass für einfachere Berechnungsmethoden.

Betrachtet man obige Termdarstellung, kann man erkennen, dass wenn man vom
Anfang der Folge startet immer d dazu kommt, wenn man aber vom letzten (n-ten)
Glied der Folge rückwärts geht immer d wegkommt. Diese Operationen heben sich auf.
Man kann deshalb Anzahl/2 mal die Summe vom ersten und letzten Glied machen.

`\sum_{k=1}^{n} a_k = \frac{n(a_1+a_n)}{2}`

Insbesondere ist `1+2+...n=\frac{(n+1)n}{2}`.


geometrische Folge
...................

Bei der geometrischen Folge ergibt sich ein Glied der Folge aus dem
vorhergehenden durch Multiplikation mit einer gleichbleibenden Zahl.

`a_{n+1} = a_n \cdot q`.

Das ist die **rekursive** Darstellung der geometrischen Folge.

Um zum n-ten Glied zu kommen, wiederholt man das n-1 mal:

`a_n = a_1 q^{n-1}`

Das ist die **Termdarstellung** der geometrischen Folge.

Um eine gegebene Folge als geometrisch zu erkennen, schaut man, ob der
Quotient aufeinanderfolgender Glieder gleich bleibt.

geometrische Reihe
...................

Betrachtet man

.. math::

    \begin{matrix}
    1+&q+q^2+...+q^{n-1}&=&S_n\\
      &q+q^2+...+q^n&=&q S_n\\
    \end{matrix}

so sieht man, dass viele Summanden gleich sind. Durch Subtraktion erhält man

`\sum_{k=1}^{n} q^{k-1} = 1 + q + ... + q^{n-1} = \frac{q^n-1}{q-1}=\frac{1-q^n}{1-q}` 

