.. raw:: html

    %path = "Mathematik/Finanz/Zinsen"
    %kind = kinda["Texte"]
    %level = 10
    <!-- html -->
    

`K` Kapital

    Ein Geldbetrag.

`i` Zinssatz

    Die Zu- oder Abnahme von `K` wird in %=1/100 angegeben. 

    - Zinswert: `3\% K = 0.03 K`. 
    - Zunahme: `K + 3\% K = (1+3\%) K = 1.03 K`.
    - Abnahme: `K - 3\% K = (1-3\%) K = 0.97 K`.

`n` Perioden (Jahre/Quartale/Monate/Tage)

    Zum Zinsatz `i` gehört immer auch ein Zeitraum, in dem die Zunahme oder Abnahme stattfindet.

    - `i` meint ein Jahr (Jahreszinssatz, Effektivzinssatz)
    - `i_{12}` meint ein Monat
    - `i_4` meint ein Quartal

    Nach diesem Zeitraum ist K um den `iK` größer, also `K_{n=1} = K_0 (1+i) = K_0 q` (q = 1+i).

Zinseszinsen


    Am Anfang eingelegtes Kapital ist nach einer Periode
    (n=1) `K_{n=1} = K_0 (1+i) = K_0 q` wert, nach n=2 Perioden `K_0 q^2`, nach n=3 Perioden `K_0 q^3`...

    Nach n Perioden:

    - `K_n = K_0 q^n`

    - Aufzinsen: Ein Kapital wird mit `q^n` multipliziert, um den Wert `n` Perioden später zu erhalten.
    - Abzinsen: Ein Kapital wird mit `q^{-n}` multipliziert, um den Wert `n` Perioden früher zu erhalten.

Rente

    Eine Rente ist eine Zahlung (Rate `r`) in regelmäßigen Zeitabständen (Perioden).
    Die Periodenzahl für jede Rate ist anders.
    Die Endwerte aller Raten aufsummiert ergibt die Rentenformel:

    `R_n = \sum_{m=0}^{n-1} r_m = \sum_{m=0}^{n-1} r q^m = r \frac{q^n - 1}{q-1}`

    Diese Formel kann man anwenden, um den Endwert `R_n` der Rente zu berechnen,
    wenn die Rente am Ende jeder Periode gezahlt wurde (nachschüssig).

    - Nachschüssige Rente: `R_n = r \frac{q^n - 1}{q-1}`

    - Vorschüssige Rente: `R_n^v = q R_n`

    **Barwert** der Rente ergibt sich durch Abzinsen des **Endwertes** `B_n = R_n q^{-n}`.

Unterjährige Rente

    Um den unterjährigen Zinsatz mit dem Jahreszinssatz vergleichen zu können, muss man umrechnen.

    Lineare Umrechnung, wenn in den Monaten oder Quartalen keine Verzinsung stattfindet: 

    - `i_{12} = i/12`
    - `i_4 = i/4`

    Konforme (äquivalente) Umrechnung bei unterjähriger Verzinsung:

    - `i = (i_{12} + 1)^{12} - 1`
    - `i = (i_4 + 1)^4 - 1`

    Wenn ein Jahreszinssatz gegeben ist und eine monatliche Rente zu berechnen ist,
    dann muss zuerst **auf den monatlichen Zinssatz umgerechnet** werden.

Rentenrest

    Um zu beantworten, wieviel Kapital zu einem Zeitpunkt 
    während der Rentenlaufzeit noch übrig ist, zählt man den Rentenwert 
    bis zu diesem Zeitpunkt vom Kapitalwert an diesem Zeitpunkt ab.

Umrechnung einer Rente in eine andere

    - Man ermittelt zuerst den Endwert der einen Rente `R_n`. 
    - Dieses `R_n` muss man dann zum Endwert der anderen Rente auf- oder abzinsen.
    - Durch Verwendung der Rentenformel kann man dann die gesuchte Größe (`n`, `q`, `r`) der neuen Rente ausrechnen.

Kapitalvergleich, Angebotsvergleich

    Um Gelder vergleichen zu können muss man sie auf den gleichen Zeitpunkt (etwa jetzt, also Barwert)
    umrechnen. Umrechnen geht über Auf- oder Abzinsen oder unter Verwendung der Rentenformel.


