.. raw:: html

    %path = "Mathematik/Funktionen"
    %kind = kinda["Texte"]
    %level = 9
    <!-- html -->

Eine **Funktion (= Abbildung)** kann als Menge von Wertepaaren `(x,y)` mit
`x\in X` (**Definitionsmenge**) und `y\in Y` (**Wertemenge**) identifiziert
werden.  Wichtig ist die **Eindeutigkeit**: für ein `x` gibt es genau ein `y`.
`x` kann man aus einer Menge frei wählen.
Man nennt `x` **unabhängiger Wert, Urbild, Veränderliche, Argument oder Stelle**.
`y` ist durch `x` bestimmt. Es ist keine zusätzliche Information notwendig.
Das macht letztendlich den Begriff Funktion wichtig.  
Man nennt `y` **abhängige Variable, Bild oder Funktionswert**.

Ist diese Eindeutigkeit nicht gegeben, dann spricht man von einer **Relation**.

Ein Funktion `f` hat ein Richtung von der Menge aller `x` (`X`) auf die Menge
aller `y` (`Y`). Man schreibt `f:X\rightarrow Y`.

Die Wertepaare können normalerweise nicht alle angegeben werden,
deshalb beschreibt man eine Funktion mit einer Rechenvorschrift, 
d.h. einem **analytischen Ausdruck**, z.B. `y=x^2+1`.
Das ist im Grunde ein Algorithmus, ein kleines Programm.

.. admonition:: Grundkonzepte:

    - Definitionsmenge
    - Wertemenge
    - Abbildung

Wenn man keinen eigenen Buchstabe `f` für die Funktionen haben will,
kann man auch schreiben: `y(x)`, d.h. die Klammern sagen aus, 
dass `y` sich aus `x` eindeutig ergibt, d.h. Funktion von `x` ist.
Manchmal kann `f` die Funktion meinen oder den Funktionswert.  
    
Konzentriert man sich nur auf die Abbildung, so schreibt man statt `g(f(x))` 
auch `g\circ f` und das heißt: bilde zuerst mittels `f`, dann mittels `g` ab,
d.h. von rechts nach links in beiden Schreibweisen.

Es kann mehrere `x` mit gleichem `y` geben und es ist immer noch eine Funktion.
Gibt es nur ein Urbild `x` für ein Bild `y`, dann ist die Funktion
linkseindeutig (**injektive**), d.h. sie bewart Unterscheidbarkeit oder
verliert nicht an Information. 
Wird darüber hinaus noch jedes element der
Bildmenge erreicht (**surjektiv**), dann ist die Funktion unkehrbar eindeutig,
eineindeutig oder **bijektiv**.  Dann kann man auch `y` beliebig wählen und `x`
ist dadurch bestimmt (`x(y)`, **Umkehrfunktion**).

Wenn die Bilder von Elementen, die sich nahe sind, auch nahe beisammen sind,
dann ist die Funktion **stetig**. Nahe ist intuitiv, muss aber mathematisch
erst definiert werden.  Das geschieht über eine **Metrik** `d` (`d(x,y)\ge 0`,
`d(x,y)=d(y,x)` und `d(x,z)\le d(x,y)+d(y,z)`, z.B. `d(x,y)=|y-x|`) 
(oder auch abstrakter in der Topologie über eine Menge von (offenen) ineinander
verschachtelten Mengen.)

.. admonition:: Stetigkeit bei `x`

   Für jedes `\varepsilon > 0` gibt es eine `\delta`, so dass 
   für alle y mit `d(x,y)<\delta` gilt: `d(f(x),f(y))<\varepsilon`. 

   Für jede `\varepsilon`-Umgebung gibt es eine `\delta`-Umgebung.
    
Eine Funktion setzt keine Ordnung voraus. Ist sie aber gegeben,
dann sagt man eine Funktion ist **(streng) monoton** steigend,
wenn aus `x\le y` (`x<y`) folgt: `f(x)\le f(y)` (`f(x)<f(y)`).
(Streng) monoton fallend wird analog definiert.

Verwandt mit Funktion ist Morphismus (:lnk:`r.cs`).

Zur graphischen Darstellung einer Funktion in einem **Koordinatensystem**: 

- Werden die Werte der beteiligten Variablen `X` und `Y` mittels einer Einheit
  auf Zahlen abgebildet
- Es wird eine Längeneinheit für die Darstellung gewählt (z.B. cm).
  Das Verhältnis dieser Längeneinheit zur realen Einheit (kg, km, m/s,...) ist
  der **Maßstab**.
- Für einen Wert der unabhängigen Variablen `X` geht man den Zahlenwert 
  in dieser Längeneinheit nach links (`x`-Koordinate, Abszisse).
- für einen Wert der abhängige Variable `Y` geht man den Zahlenwert 
  in dieser Längeneinheit nach oben (`y`-Koordinate, Ordinate).
- Das wiederholt man für einige Werte und man erhält Punkte 
  Die `(x,y)`-Paare dieser Punkte kann man als Zwischenschritt auch
  in eine Tabelle eintragen (**Wertetabelle**).
- Weil es sich meistens um stetige Funktionen handelt, 
  kann man eine Kurve durch diese Punkte legen. 
  Ist die Kurve eine Gerade, dann spricht man von einer **linearen Funktion**.

Beispiele für Graphen von bestimmten grundlegenden Funktionstypen mit
einer unabhängigen Variablen gibt es hier: :lnk:`r.cf`.

