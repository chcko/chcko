.. raw:: html

    %path = "Mathematik/Vektoren/Transformation und Inverse"
    %kind = kinda["Texte"]
    %level = 11
    <!-- html -->


Koordinatentransformation und Inverse Matrix
============================================

Nicht immer sind die Basisvektoren unabhängig, d.h.  orthogonal zueinander.

Wenn man etwa die Zutaten von einer Auswahl von Kuchen als Vektorraum auffasst
(*Zutatenvektorraum*), dann ist jeder Kuchen ein Vektor, d.h. eine unabhängige
Auswahl aus mehreren Variablen (Quantitäten der Zutaten, 0 falls nicht
verwendet).

Die Zutaten kann man als orthogonal zueinander ansehen. Der Kontext macht 
einen genaueren Vergleich nicht notwendit.
*Das skalare Produkt ist 0.*

Die Kuchen wollen wir aber genauer vergleichen und zwar über deren Zutaten.
Dann werden etwa Kuchen A und Kuchen B sicher gleiche Zutaten haben.
Die Einheitsvektoren im *Kuchenvektorraum* sind nicht orthogonal zueinander,
wenn man genauer hinschaut, was man aber nicht tun muss.
*Das skalare Produkt ist nicht 0.*

Ein Vektor im Kuchenvektorraum (Wieviel von jeder Sorte Kuchen?) kann auf den Vektorraum der Zutaten
transformiert werden, indem man ihn mit einer Matrix multipliziert. 
Jede Spalte in dieser Matrix stellt einen Kuchen dar.

Was man bei Matrizen und Vektoren macht, ist eine Positionskodierung. Die Position einer Zahl
bestimmt, was sie bedeutet. Das macht man auch im Zahlensystem so (Einer, Zehner, Hunderter,...).

In diesem Beispiel mit den Kuchen und den Zutaten sind die Anzahl der Variablen (=Dimension) 
in den zwei Vektorräumen nicht notwendigerweise gleich. Die Dimensionen können anders sein, 
etwa 10 Zutaten und 3 Kuchensorten. Die Transformationsmatrix ist dann 10x3 (10 Zeilen, 3 Spalten).
Eine solche `m\times n` Matrix mit `m\not = n` kann man nicht invertieren, 
d.h. man kann nicht aus einem Zutatenvektor auf die Kuchensorten (Kuchenvektor) schließen. 
Oder anders ausgedrückt: Es gibt nicht für jede Kombination von Zutaten eine Kombination 
(*Linearkombination*) von Kuchen, die genau diese Zutatenmengen brauchen.

Fixiert man die Anzahl der Kuchen in einer kleinen Sortenauswahl
wird weniger Information festgelegt, d.h. es werden weniger Auswahlentscheidungen getroffen,
als im Zutatenraum, der im Beispiel als größer angenommen wird. 

.. admonition:: Pseudoinverse

    Man kann sie aber pseudo-invertieren (Moore-Penrose Pseudoinverse).  Im
    Beispiel erzeugt letztere aus den Zutaten einen Kuchensortenvektor der
    minimal Zutatenreste zurück lässt (Methode der kleinsten Quadrate) bzw. die
    Zutaten bestmöglichst ausnützt (maximale Entropie).

Wenn man von einem Vektorraum in einen mit gleicher Dimension transformiert, 
dann kann man wieder auf die urspünglichen Vektoren kommen, 
indem man mit der *inversen Matrix* multipliziert.

Damit die Inverse existiert, muss zusätzlich zur quadratischen Form jede
Spalte/Zeile *linear unabhängig* von den anderen sein, sonst befindet man sich
effektiv in einer kleineren Matrix (*Rang einer Matrix*).  Im Kuchenbeispiel
bedeutet das, dass jede Kuchensorte eine andere Zutatenkombination haben muss,
damit man sie von den anderen unterscheiden kann und damit mit ihr zusätzliche
Information kodiert werden kann.

.. admonition:: Lineare Unabhängigkeit

    Quadratische Matrizen können invertiert werden, 
    wenn eine Spalte (oder Zeile) sich nicht aus den anderen durch Linearkombination
    ergibt. Der Rang der Matrix ist gleich seiner Dimension.

Die Inverse einer quadratischen Matrix kann man allgemein berechnen indem man:

- das `ij` Kreuz weglässt und Determinante berechnet = Minor `M_{ij}`
- das Vorzeichen ändert, falls `i+j` ungerade ist
- dann transponiert, d.h. an der Diagonale spiegelt
  (unten:`ij` bei `A` und `ji` bei `M`)
- alles durch die Determinante teilt

Kurz 

.. math::

    (A^{-1})_{ij} = \frac{1}{det(A)}(-1)^{i+j} M_{ji}


`\frac{1}{det(A)}` schreibt man oft vor der Matrix. Man kann diesen Wert aber
auch mit jeder Zahl in der Matrix multiplizieren.

Für eine *2x2 Matrix* ist `M_{ij}` die diagonal gegenüberliegende Zahl.
Wegen des Transponierens bleibt die Zahl links unten und rechts oben (Nebendiagonale),
aber das Vorzeichen ändert sich. 
Auf der Hauptdiagonalen werden die Zahlen vertauscht und da `i+j` gerade ist,
bleibt das Vorzeichen.

- Hauptdiagonale `\rightarrow` Vorzeichen bleibt
- Nebendiagonale `\rightarrow` Position bleibt

