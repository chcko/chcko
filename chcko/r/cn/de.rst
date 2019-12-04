.. raw:: html

    %path = "Mathematik/Zahlen/Darstellung"
    %kind = kinda["Texte"]
    %level = 9
    <!-- html -->

Eine Anzahl ist etwas reales und unabhängig von deren Darstellung.

Hier werden nur `Stellenwertsysteme <http://de.wikipedia.org/wiki/Stellenwertsystem>`_ 
diskutiert, aber es gibt andere Systeme. Siehe 
`Wikipedia Artikel <http://de.wikipedia.org/wiki/Zahlensystem>`_.

Darstellung von Zahlen
======================

Man kann nicht für jede Anzahl ein individuelles Zeichen machen.  Stattdessen
verwenden wir Zeichen bis zu einer bestimmten Anzahl und, sobald diese erreicht
ist, zählen wir Häufchen von dieser Anzahl.

.. admonition:: Hinweis

    Ein Zahlensystem kann man mit einem Buchstaben oder Lautsystem vergleichen.
    In einer Sprachen werden Laute kombiniert und so eine Vielheit erzeugt, eben Wörter.
    Diese werden dann zu realen Dingen abgebildet.
    Mit Zahlen ist es gleich. Ziffern werden kombiniert und dann zur Anzahl abgebildet.

Das Dezimalsystem (Zehnsersystem)
---------------------------------

- Für eine Anzahl unter zehn gibt es ein eigenes Zeichen: 1, 2, 3, 4, 5, 6, 7, 8, 9.
- Für "kein" gibt es die **0**. Zusammen mit der 0 gibt es im Zehnersystem 10 Zeichen.
- Für eine Anzahl Zehn und darüber machen wir Zehnerhäufchen und zählt diese separat.

Positionscodierung:

    Statt etwa 3 Zehner und 4 Einer zu schreiben, schreiben wir die 3 an eine Stelle für die Zehner
    und 4 an die Stelle für die Einer: 34.
    Das kann man Positionscodierung nennen: Über die Position identifiziert man, was man meint.

    302 heißt 3 Zehnerhäufchen von Zehnerhäufchen (Hundert), 0 (keine) Zehner und 2 Einer.

Wertigkeit:
    Die Wertigkeit der Stellen (=Positionen) ist von rechts nach links aufwärts: 

    ...  10³=1000 10²=100 10¹=10 10⁰=1

    Das sind alles Potenzen von 10. 
    10 ist die **Basis** des Dezimalsystems.

Brüche:
    So wie ein zehnfaches Häufchen eine Stelle hat, so wird auch dem zehnten Teil eine 
    Stelle nach dem Komma gegeben.

    ,1/10¹=1/10  1/10²=1/100  1/10³=1/1000 ...

Das Dualsystem (Binärsystem, Zweiersystem)
------------------------------------------

Im Dualsystem wird eine Anzahl von 2 zu einem eigenen Häufchen.

Zusammen mit der 0 gibt es im Binärsystem 2 Zeichen, die dann bedeuten: **Da oder Nicht Da**

Die Wertigkeit der Stellen ist von rechts nach links aufwärts: 

    ...  2⁴=16 2³=8 2²=4 2¹=2 2⁰=1 , `2^{-1}` `2^{-2}` ...

Beispiel: 

    1011₂ = 11₁₀

Das Dualsystem ist sehr wichtig, da es in Computern verwendet wird und weil 2 die kleinste Anzahl ist,
bei der man noch auswählen kann, d.h. Information codieren kann.

Das Hexadezimalsystem (Sechszehnersystem)
-----------------------------------------

Hier macht man jeweils 16 zu einem neuen Häufchen.

Zusammen mit der 0 gibt es im Hexadezimalsystem 16 unterschiedliche Zeichen: 

    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, A, B, C, D, E, F.

Dabei bedeuten A=10, B=11, C=12, D=13, E=14, F=15. 

Die Wertigkeit der Stellen sind von rechts aufwärts:

    ... 16⁴=65536 16³=4096 16²=256 16¹=16 16⁰=1 ,  `16^{-1}` `16^{-2}` ...

Da 2⁴=16 braucht man für eine Stelle im Hexadezimalsystem immer 4 Stellen im Dualsystem. 
Da das 2er System wichtig ist, macht diese Eigenschaft auch das Hexadezimalsystem und alle 
Zahlensystem, die Potenzen von 2 sind wichtig, 
z.B. Basis 8 (octal), 64 (base64), 128(ASCII) und 256 (ANSI).

Duodezimalsystem
-----------------

Zwölf hat viele Teiler: 2, 3, 4, 6
Das erlaubt eine einfache Darstellung von Brüchen mit diesem Nenner.

Aber wie beim Dezimalsystem (1/3 = 0.333...)
gibt es auch im Duodezimalsystem Brüche, die periodische sind (1/5 = 0.2497 2497...).

