.. raw:: html

    %path = "Mathematik/Morphismen"
    %kind = kinda["Texte"]
    %level = 10
    <!-- html -->

Der Begriff der Funktion aus der Mengenlehre, Elemente einer Menge
(Definitionsbereich) in eine andere Menge (Wertebereich) eindeutig abzubilden,
wird mit dem Begriff des Morphismus in der Kategorientheorie in der Hinsicht
abgeändert/verallgemeinert, dass man die ganze Abbildung ins Zentrum rückt und
Objekte unabhängig ob Quelle (domain) oder Ziel (codomain) zu einer Menge von Objekten O
zusammenfasst. Quelle und Ziel in der Menge der Objekte sind durch den
Morphismus bestimmt, bzw. Teil davon 
(`D_f` ist Quelle von f, `C_f` ist Ziel von f, beide müssen nicht Mengen sein). 
Mehrere Morphismen in der Menge der Morphismen M können sich ein Paar
(Quelle,Ziel) teilen.  (O,M,id) ist eine Kategorie. id ist der identische
Morphismus.

Ein wichtiger Aspekt bezüglich Morphismen ist, dass eine Struktur erhalten bleibt
(Ordnungsstruktur, Algebraische Struktur, topologische Struktur) und
je nach betrachteter Struktur gibt es Unterbegriffe (`f\circ g (D_g) = f(g(D_g))`): 

- Monomorphismus: `f\circ g=f\circ h \implies g=h` (linkskürzbares `f`) 
  oder `f` injektiv für Mengen als Objekte
  (`Beweis <http://www.proofwiki.org/wiki/Injection_iff_Monomorphism_in_Category_of_Sets>`_)

- Epimorphismus: `g\circ f=h \circ f \implies g=h` (rightkürzbar es `f`) 
  oder `f` surjektiv für Mengen als Objekte
  (`Beweis <http://www.proofwiki.org/wiki/Surjection_iff_Epimorphism_in_Category_of_Sets>`_)
  
- Isomorphismus: `f` hat ein `g` für das `f\circ g=id_{D_g}` und `g \circ f = id_{D_f}`
  (Linksinverse = Rechtsinverse) oder `f` bijektiv für Mengen als Objekte

- Endomorphismus: `X\rightarrow X`

- Automorphismus: `X\rightarrow X` + Isomorphismus

- Homomorphismus (Algebra): `f(a+b)=f(a)+f(b)` (`+` möglicherweise unterschiedlich)

- Homöomorphismus (Topologie): `f` und `f^{-1}` stetig

- Diffeomorphismus (Differentialgeometrie): bijektiv, `f` und `f^{-1}` stetig differenzierbar



