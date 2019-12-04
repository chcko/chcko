.. raw:: html

    %path = "Mathematik/Richtung"
    %kind = kinda["Texte"]
    %level = 11
    <!-- html -->

Die Variablen, mit denen man es normalerweise zu tun hat,
sind Ausdehnungen (Größen, Teilmengen, Differenzen) und nicht Punkte. 
3m meint alle Punkte von von 0 bis 3m.

Zwei unterschiedliche Mengen, für die alle Kombinationen vorkommen, 
kann man als orthogonal zueinander ansehen. 
Der Winkel zwischen ihnen ist `\frac{\pi}{2}`.
Sie spannen die größtmögliche Kombinationsmenge (Fläche) auf. 
Vektorprodukt maximal. Skalares Produkt 0.

Ein zweidimensionaler Vektor `\vec{v}` und eben auch `z\in\mathbb{C}` bezeichnet 
eine solche Ausdehnung. Die eingeschlossene Fläche ist 
`\vec{v_1}\times\vec{v_2}` oder `Im(z_1\bar{z_2})`.

`z_1\bar{z_2}` hat das Skalarprodukt im Realteil und das Vektorprodukt im Imaginärteil.

Größen, die in die gleiche Richtungen zeigen, kann man addieren.  Ungleiche
Richtungen kann man komponentenweise addieren.
`\frac{\vec{v_1}\vec{v_2}}{|\vec{v_1}|}=\vec{v_1}_0\vec{v_2}` ist die
Komponente von `\vec{v_2}`, die in Richtung `\vec{v_1}` addiert werden kann.
`\frac{z_1\bar{z_2}}{|z_1|}` ist die komplexe Zahl mit Realteil addierbar in
Richtung `z_1` und Imaginäteil orthogonal zu `z_1`, multiplizierbar um die
aufgespannte Fläche zu erhalten. Besser man rechnet jedoch normal `z_1+z_2`,
d.h. mit den durch das Koordinatensystem gegebenen Komponenten.

Der Winkel ergibt sich aus dem Verhältnis der aufgespannten Fläche zur maximalen Fläche
`\angle(\vec{v_1},\vec{v_2})=\arcsin\frac{|\vec{v_1}\times \vec{v_2}|}{|\vec{v_1}||\vec{v_2}|}` 
oder aus dem Verhältnis der addierbaren Komponente zur gesamter Länge
`\angle(\vec{v_1},\vec{v_2})=\arccos\frac{\vec{v_1}\vec{v_2}}{|\vec{v_1}||\vec{v_2}|}` 
und im Komplexen zusammen
`\angle(z_1,z_2)=\arg(\frac{z_1\bar{z_2}}{|z_2||z_2|})=\arg{z_1\bar{z_2}}`.

Ein anderes Wort für Richtung ist Phase, das wohl von dem umgangssprachlich
vorbelegten Wort Richtung etwas ins Abstraktere ablenken soll. Essentiell ist
der Vergleich zweier Größen bezüglich addierbarer Komponenten. Dazu werden
Variablen die keine Richtung darstellen, aber eben Einfluss auf Addierbarkeit
haben, auf einen Winkel umgerechnet, der dann Phase heißt.  Beispiel:
Der Zeitpunkt `t` bei Schwingungen wird `\varphi=\frac{2\pi}{T}t` oder die
kombinierte Zeit-, Raum-Position bei Wellen wird
`\varphi=\frac{2\pi}{\lambda}x-\frac{2\pi}{T}t`.  `Ae^{i\varphi}` gibt dann die
momentan addierbare Amplitude wieder.


