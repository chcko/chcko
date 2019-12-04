.. raw:: html

    %path = "Mathematik/Funktionen/Integral von 1÷z"
    %kind = kinda["Texte"]
    %level = 12
    <!-- html -->

Aus der reellen Analysis wissen wir, dass
`\frac{dy}{dx}=\frac{d\,e^x}{dx}=e^x=y`, weswegen die Umkehrung
`\frac{dx}{dy}=\frac{d\,\ln y}{dy}=\frac{1}{y}` für `y>0`.  Für die
Stammfunktion von `\frac{1}{y}` kann man auch negative `y` mit einschließen,
wenn man den Betrag nimmt: `\int\frac{1}{y}dy=ln|y|+C`.  Das ergibt sich aus der
Symmetrie von `\frac{1}{y}`.  Bei 0 besteht eine Singularität, d.h. man kann dort nicht
darüber integrieren. 

In `\mathbb{C}` ist `e^z=e^{x+iy}=e^xe^{iy}`,
d.h. der Realteil wird Betrag `e^x` und der Imaginärteil wird Argument des Wertes.
Daher kommt auch die Periode `2\pi i` entlang der imaginären Achse.
Die Stammfunktion von `\frac{1}{z}` ist die Umkehrfunktion von `e^z`,
d.h. der Betrag wird Realteil `ln|z|` und das Argument wird Imaginärteil:

`\int \frac{1}{z}dz=ln|z|+i\arg(z)+C`.

In `\mathbb{C}` kann man um die Singularität herum integrieren:

.. math::

    \oint_{|z|=1}\frac{1}{z}dz = 
    (\ln|z| + i\arg z)\bigr|_{\arg z=0,\,|z|=1}^{\arg z=2\pi,\,|z|=1} = 2\pi i

Das ist ein Vorläufer des Residuensatzes.

