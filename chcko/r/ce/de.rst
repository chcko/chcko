.. raw:: html

    %path = "Mathematik/Funktionen/Log"
    %kind = kinda["Texte"]
    %level = 10
    <!-- html -->
    
Logarithmus
-----------

Will man vom Ergebnis des Potenzierens wieder zurück zu den Ausgangszahlen,
dann gibt es zwei Wege, nämlich zur Basis und zur Hochzahl.

Zur Basis kommt man durch Potenzieren mit dem Kehrwert, also `(3^2)^{\frac{1}{2}} = 3`,
auch Wurzelziehen genannt.

Zur Hochzahl kommt man durch den **Logarithmus**, also `\log_{3}(3^2)=2`.

Aus dem Rechnen mit Potenzen zu gleicher Basis, 
z.B. `2^32^2=2^{3+2}` 
und `\frac{2^3}{2^2}=2^{3-2}` ergibt sich, dass der Logarithmus aus
*mal* *plus* und aus *teilen* *minus* macht.
Aus Wiederholen von Multiplikation (Potenzieren) 
wird dadurch Wiederholen von Addition (Multiplikation):

.. math::

    \begin{matrix}
    \log ab &= \log a + \log b \\
    \log \frac{a}{b} &= \log a - \log b \\
    \log b^c &= c\log b
    \end{matrix}


Aus der letzten Regel ergibt sich, dass man den Logarithmus zu einer beliebigen
Basis wie folgt berechnen kann:

.. math::

    b^x &= d \\
    x &= \frac{\log d}{\log b}


Exponentialgleichungen, also Gleichungen, wo man den Exponent (die Hochzahl) sucht,
löst man am besten, indem man zuerst so lange umformt, bis man `b^x = d` hat,
dann wendet man auf beiden Seiten den Logarithmus an.

Der Logarithmus bezieht sich immer auf eine bestimmte Basis. 
Wenn diese nicht angegeben ist, dann wird mit `\log` meistens die Basis 10 angenommen,
oft, etwa in Programmiersprachen, aber auch die Eulersche Zahl e=2.71828182846...

Es gilt:

.. math::

    \log_{10} 10 = \log 10 = \text{lg} 10 = 1\\
    \log_e e = \ln e = 1\\
    \log_2 2 = \text{lb} 2 = 1\\
    
