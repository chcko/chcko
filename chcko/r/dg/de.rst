.. raw:: html

    %path = "Physik/Schaltkreise/Thevenin"
    %kind = kinda["Beispiele"]
    %level = 13 
    <!-- html -->

.. role:: asis(raw)
    :format: html latex


Wir werden die Übertragungsfunktion eines Bandsperre-Filters mit der Methode von Thevenin ermitteln.

Wir ziehen dazu einen Schaltkreis aus 
`Op Amps for EveryOne (5-10) <http://www.ti.com/lit/an/slod006b/slod006b.pdf>`_.
heran.

.. texfigure:: c1.tex
      :align: center

Das Eingangssignal ist gegenüber Erde. Wir zeichnen die Schaltung neu, um das widerzuspiegeln.

.. texfigure:: c2.tex
      :align: center

Wir suchen `G=\frac{V_o}{V_i}`.  
`V_o` ist die Spannung beim rechten Widerstand. Wir werden dort das Thevenin-Äquivalent berechnen.


.. texfigure:: c3.tex
      :align: center

Wir finden die Ströme mittels der Kirchhoff'schen Regeln. 
Es gibt zwei Schleifen, wo Strom fließt.
Es gibt keinen Strom bei dem Widerstand, wo wir den Stromkreis geöffnet haben.

.. texfigure:: c4.tex
      :align: center

Die resultierenden Gleichungen sind

.. math:: \begin{array}{l l l}
    V_i - I_2 R - \frac{I_2}{iwC} - I_1 R & = 0\\
    V_i - \frac{I_1 - I_2}{iwC} - I_1 R & = 0
    \end{array}

Diese lösen wir nach `I_1` und `I_2`:

.. math:: \begin{array}{l l}
    I_1 &= \frac{\omega C V_i (-2 i+C R \omega)}{-1-3 C R i \omega+C^2 R^2 \omega^2}\\
    I_2 &= -\frac{i \omega C V_i}{-1-3 C R i \omega+C^2 R^2 \omega^2}
    \end{array}

Bei die kleine Schleife bei `V_{th}` berechnen wir mit den bekannten Strömen 

.. math:: V_{th}=\frac{I_2}{iwC} + I_1 R

Als nächstes brauchen wir die Thevenin-Impedanz. Dafür entfernen wir `V_i`
und berechnen die Impedanz wie sie von `V_{th}` aus gesehen wird.

.. texfigure:: c5.tex
      :align: center

Wir zeichnen die Schaltung neu, um besser zu sehen, was parallel und was seriell ist.

.. texfigure:: c6.tex
      :align: center

Dann erhalten wir

.. math:: Z_{th}=\left(\frac{1}{i \omega C}+\frac{R \frac{1}{i \omega C}}{R+\frac{1}{i \omega C}}\right) || R = 
    \frac{R (1+2 i \omega C R)}{1+3 i \omega C R - C^2 R^2 \omega^2}

und

.. math:: V_o = \frac{R}{R + Z_{th}}

Und endlich bekommen wir die **Übertragungsfunktion**:

.. math:: G = \frac{V_o}{V_i} = \frac{(-i+C R \omega)^2}{-2-5 i \omega C R+C^2 R^2 \omega^2}
    = \frac{(1+i \omega C R)^2}{2+5 i \omega C R-C^2 R^2 \omega^2}
    = \frac{(1+ s\tau)^2}{2+5 s\tau+(s\tau)^2}

Hier haben wir `\tau=R C` und `s=i \omega` gesetzt, wie es für Filter üblich ist.
Beim Nenner kann man für `s\tau` die Nullstellen berechnen (-4.56,-0.44).
Das Produkt der Nullstellen ist 2. `G` können wir damit so schreiben 

.. math:: G = \frac{(1+ s\tau)^2}{2(1+\frac{s\tau}{0.44})(1+\frac{s\tau}{4.56})}

