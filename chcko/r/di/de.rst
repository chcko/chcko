.. raw:: html

    %path = "Mathematik/Zahlen/C"
    %kind = kinda["Texte"]
    %level = 9
    <!-- html -->

.. contents::

Die komplexen Zahlen `\mathbb{C}`
---------------------------------

Bei den reellen Zahlen (:lnk:`r.ci`) haben wir immer wieder neue Mengen zu den
"Zahlen" hinzu genommen. 

Das machen wir bei folgendem Problem auch.

`x^2` nimmt nur positive Werte an. 

- Es geht Information verloren (die Wertemenge ist kleiner) und
- Gleichungen wie `x^2+1=0` können nicht gelöst werden 

Wenn wir ein "Zahl" `i` erfinden die `i^2=-1` ergibt, dann deckt `x^2` mit den Vielfachen
von `i` die ganzen negativen Zahlen ab. `i` nennen man **imaginäre Einheit**.

`i` und deren Vielfache haben mit den reellen Zahlen vorerst nichts zu tun. 
Sie sind orthogonal zu `\mathbb{R}`. Orthogonal bedeutet, dass alle Kombinationen
zulässig sind und das entspricht einer Ebene, der **komplexen Zahlenebene** oder
**Gaussschen Zahlenebene**.

    `z = a + ib \in \mathbb{C}`

Das ist wie ein zweidimensionaler Vektor: 2 orthogonale Richtungen unabhängig addiert.

Es gibt drei Darstellungen 

- `z = a+ib`, also über Komponenten oder
- `z = r(cos\varphi + i sin\varphi)` über Länge `r` und Richtung `\varphi` (Argument, Phase) in Bogenmaß. 

Aber nun folgendes: 

- `i\cdot 1 = i`, also Multiplikation mit `i` macht aus 1 ein `i` das orthogonal zu
  1, der **reellen Einheit**, ist. Das ist eine Drehung um den rechten Winkel nach links.
- `i\cdot i = -1`. Wieder eine Drehung um den rechten Winkel.

Allgemein: Multiplikation mit `i` macht eine Drehung um den rechten Winkel, per Konvention nach links.

Weiters: Multiplikation addiert den Winkel dazu, d.h. Multiplikation führt zur
Addition des Winkels.  Das lässt einen vermuten, dass es eine Darstellung geben
könnte, die den Winkel im Exponenten hat.  Reihenentwicklung von `\sin` und `\cos`
und `e^x` in der Analysis und Vergleich ergibt die **Eulersche Formel**:

- :inl:`r.cy` 

- `z=re^{i\varphi}` heißt dritte **Normaldarstellung** der komplexen Zahl.

Von `\sin` und `\cos` weiß man, dass sie die Periode `2\pi` haben, so auch `e^{i\varphi}`.
Die n-te Wurzel teilt alle Perioden bis `2n\pi` auf unter `2\pi` und somit zu n
unterschiedlichen Werten:

.. math::

    z^{1/n}=r^{1/n}e^{i(\varphi/n+2k\pi/n)}

Allgemeiner:

   In `\mathbb{C}` hat jedes Polynom n-ten Grades genau n Nullstellen 
   (**Hauptsatz der Algebra**). Davon können manche aber zusammenfallen.
   `\mathbb{C}` heißt deshalb **algebraisch abgeschlossen**.

Das heißt, dass nicht nur `x^2`, sondern alle Polynome ganz `\mathbb{C}` auf ganz `\mathbb{C}` abbilden.
Es geht keine Information verloren.

.. admonition:: Hinweis

    In der Funktionentheorie erfährt man, das sich das auf alle Funktionen
    ausdehnen lässt, die in ganz `\mathbb{C}` unendlich oft differenzierbar
    (analytisch, holomorph) sind (ganze Funktionen), da sie sich in
    Taylorreihen entwickeln lassen.

Weiteres:

- a = Re(z) ist der Realteil

- b = Im(z) ist der Imaginärteil

- `\bar{z}=re^{-i\varphi}=a-ib` heißt (komplex) Konjugierte zu z. `\bar{z^n}=\bar{z}^n`.

  `z_1\bar{z_2}` vereint in sich Skalarprodukt (`Re(z_1\bar{z_2})=r_1r_2\cos\Delta\varphi`) und Vektorprodukt
  (`Im(z_1\bar{z_2})=r_1r_2\sin\Delta\varphi`).

- `|z| = \sqrt{z\bar{z}} = \sqrt{a^2+b^2} = r` ist der Betrag (oder Modul) von z.

  Das Quadrat über die Länge einer komplexen Zahl unabhängig von ihrer Richtung
  ergibt sich durch `z\bar{z}` und nicht durch `z^2`.

- `φ = arg(z)` ist Argument (oder Phase) von z. 

  - `arg(z_1z_2)=arg(z_1)+arg(z_2)`

  - `arg(\frac{z_1}{z_2})=arg(z_1)-arg(z_2)`


Anwendung von `\mathbb{C}` 
...........................

Da `\mathbb{C}` eine Erweiterung von `\mathbb{R}` darstellt, 
kann man alles mit `\mathbb{C}` machen, was man mit `\mathbb{R}` macht.
Das essentiell Neue an `\mathbb{C}` sind aber alle Richtungen, statt nur `+` und `-`.

Was heißt Richtung?

:inline:`r.ct`

Die komplexen Zahlen werden in der Physik und Technik im Umfeld von Schwingungen und Wellen 
verwendet, und davon gibt es viele: 

- Mechanik/Festkörper: Wasserwellen, Schallwellen, elastische Wellen,... 

- Elektrotechnik: Wechselstrom, Wechselstromkeis (Widerstand, Kapazität und Induktivität),...

- Elektrodynamik: Elektromagnetische Wellen (Lichtwellen, Radiowellen), ...

- Optik: Lichtwelle, ...

- Quantenmechanik: Teilchenwellen, ....

Letztendlich basieren diese Anwendungen auf dem uneingeschränkteren Rechnen in `\mathbb{C}` 
und auf den mathematisch auf `\mathbb{C}` aufbauenden Ergebnissen etwa der Funktionentheorie. 

Viele physikalische Systeme werden mit Differentialgleichungen beschrieben.
Diese reduzieren sich auf Polynome mit komplexen Lösungen (Fundamentalsatz der Algebra)
und führen zu komplexen Funktionen.


