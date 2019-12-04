.. raw:: html

    %path = "Mathematik/Funktionen/exponentiell"
    %kind = kinda["Übungen"]
    %level = 11
    <!-- html -->

.. role:: asis(raw)
    :format: html latex

Grundlegendes
-------------

In der **exponentiellen Funktion**

.. math::

    y = a^x

nennen wir

- `x` den **Exponenten**
- `a` die **Basis**
- `y` die **exponentielle Funktion** von `x` zur Basis `a`

Der **Exponent** sagt, wie oft die *Multiplikation* mit `a` wiederholt wird.
`a` muss eine positive reelle Zahl sein : `a\in\mathbb{R}`.

.. admonition:: Multiplikaton

    Multiplikation ist eine Operation der realen Welt, die als
    Zahl codiert wird. In der Zahlenmenge `\mathbb{Q}`
    ist die Operation Teil der Zahl: `2` meint `\cdot 2` und `1/2` meint `/2`.
    Das Zeichen `\cdot` steht für die Multiplikation und `/` steht für die umgekehrte (inverse)
    Operation, die Division, welche mit der Einbindung der Brüche in `\mathbb{Q}` Teil der Zahl wurde.
    Also sprechen wir nur mehr von Multiplikation und meinen die Anwendung
    der Operation aus `\mathbb{Q}\subset\mathbb{R}`.

Wenn `a` größer als `1` ist, dann wächst `y` mit `x` *strikt monoton*: `x_1<x_2 \Rightarrow y_1<y_2`.

.. tikz:: \begin{axis}[grid=both,axis lines=middle,xmin=-3,xmax=3,ymin=0,ymax=8, samples=50]
     \addplot[green]  {pow(2,x)} node[above]{$y=2^x$};
    \end{axis}

Wenn `a` kleiner als `1` ist, dann fällt `y` mit `x` *strikt monoton*: `x_1<x_2 \Rightarrow y_1>y_2`.

.. tikz:: \begin{axis}[grid=both,axis lines=middle,xmin=-3,xmax=3,ymin=0,ymax=8, samples=50]
     \addplot[green]  {pow(1/2,x)} node[above]{$y=(\frac{1}{2})^x$};
    \end{axis}


Diskussion
----------
    
Vergleichen wir die Anzahl der Wertekombinationen von `n` bits:

.. math::
    
    2^n

mit dem Wachstumsprozess, wie etwa das Anwachsen des Kapitals mit der jährlichen Verzinsung

.. math::

    (1+\frac{i}{100})^n

oder das besonders interessante natürliche Wachstum

.. math::

    e^x = \lim_{n->\infty}(1+\frac{1}{n})^{nx} = 
    \lim_{m->\infty}(1+\frac{x}{m})^m = (1+\frac{x}{\infty})^\infty

`e` ist `Eulersche Zahl <https://de.wikipedia.org/wiki/Eulersche_Zahl>`_
deren Bedeutung auf dem gegebenen Zusammenhang beruht.

Der Schlüssel zum Vestehen der Gemeinsamkeiten steckt in der Interpretation
von **Information** als Wachstumsprozess.
Jedes Bit vergößert um `1` Mal die vorhandene Anzahl von Wertekombinationen.

Notieren wir diesen Aspekt des Bits mit `(1+1)`, um zu betonen, dass `1` dazu kommt.
Die Klammern machen den Ausdruck zu einem Operator, einem Element der Zahlenmenge `\mathbb Q`.
`n` wiederholte Anwendungen von `(1+1)` erzeugen eine Vielzahl der Größe

.. math::

    (1+1)^n = 2^n

Jedes Bit wird zur bestehenden Menge von Wertekombinationen "dazuverzinst".

Das Informationmaß einer realen Variablen der Größe `C` ist die Anzahl
`n=\log_2 C` Bits, die notwendig sind, damit wir auf `C` Kombinationen kommen.

.. admonition:: Vergleich mit welcher anderen Variablen?

   Statt Bits könnten wir ebensogut die betrachtete Variable selbst nehmen,
   weil diese ist physikalisch present. Kombinationen sind aber auch
   physikalisch und auch die Auswahl von Werten, welche letztendlich Veriablen
   erzeugt, ist ein physicalischer Prozess.  Die Anzahl der beteiligten
   Variablen spielt dabei eine Rolle. Das bedeutet erstens, dass Information
   physikalisch ist und zweitens, in Hinsicht auf die Quantenmechanik, dass die
   Anzahl der beteiligten Variablen immens groß ist und die individuellen
   Beiträge minimal sind.

Wenn wir von der *Anzahl an Variablen* starten, dann gibt uns die
*Exponentialfunktion* die *Anzahl and Wertekombinationen*. Wenn wir von der
*Anzahl der Werte* starten, dann gibt uns der *Logarithmus* die *Anzahl der
Variablen*, die zur Wertegenerierung notwendig ist.

Bei der **Zinsrechnung** schauen wir auf die Geldmenge (die `1`), 
welche auf der Bank `i` Prozent zinsen abgibt.
In `n` Jahren wächst die `1` zu

.. math::

    (1+i/100)^n = q^n
    
Der *Wachstumsfaktor* `q` ist nicht `2`, sondern normalerweise nur etwas über `1`. Das
"Informationsmaß" in diesem finanziellen Kontext würde die Anzahl
der Jahre sein.

Der essentielle Unterschied bezüglich den Bits 
ist, dass, was hinzugefügt wird, ein *Bruchteil* von dem ist, was da ist.
Aber ob Bruchteil oder nicht ist nur ein Frage der Einheit.

Die Einheiten von Lebewesen sind Zellen und die ultimativen Einheiten der
realen Welt sind Quanten.  Beide sind sehr klein im Vergleich zu den Dingen
unserer täglichen Wahrnehmung.  Mit solchen kleinen Einheiten können wir auch
beliebig oft (= unendlich oft) "verzinsen":

.. math::

    \lim_{m->\infty}(1+\frac{x}{m})^m = \lim_{n->\infty}(1+\frac{1}{n})^{nx} = e^x

In der ersteren Gleichung können wir sehen, dass wir mit dem Verändern der
*Verzinsungsschritte* auch die *Wachstumsfaktor* verändern. Wegen der
Bedeutung von `e^x` wird der Wachstumsfactor `q` in `y=q^n` oft zum Exponenten von `e`
verlegt (`y=e^{kx}`).  `k = \ln q` heißt dann *Wachstumskonstante*.

.. admonition:: Natürliche Verzinsung in der Finanzwelt

  Auch in der finanziellen Welt sind die tatsächlichen 
  Verzinsungsschritte sehr klein. Aber die Bank gibt sie ihren Kunden in
  größeren Zeiteinheiten weiter. 

`x` ist die Information in der **natürlichen Informationseinheit** 
`nat <https://de.wikipedia.org/wiki/Nit_(Informationseinheit)>`_.
Im Pinzip teilen wir dabei eine Variable in unendliche viele undendlich kleine Variablen auf,
so dass der Wachstumsfaktor pro Schritt beinahe bei `1` liegt.

