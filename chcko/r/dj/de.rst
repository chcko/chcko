.. raw:: html

    %path = "Mathematik/Trogonometrie"
    %kind = kinda["Texte"]
    %level = 11
    <!-- html -->

.. role:: asis(raw)
    :format: html latex

.. contents::

Im folgenden Diagramm hat der Kreis den Radius 1.
Die Länge des Bogens diese Einheitskreises ist ein Maß für den **Winkel**,
das **Bogenmaß** genannt wird und die Einheit ``rad`` (Radiant) besitzt.
Der rechte Winkel (90°) ist `\pi/2`.
Im Allgemeinen:

.. math::

    \frac{\pi}{180}\alpha[°] = \alpha[rad]

Wenn man den Winkel ändert, dann ändern sich auch die Längen, die mit
`\sin\alpha`, `\cos\alpha` und `\tan\alpha` beschriftet sind. 
Diese Längen sind durch den Winkel bestimmt.
Anders gesagt: Diese Längen sind **Funktionen des Winkels**.

.. tikz:: \coordinate (O) at (0,0);
        \coordinate (C) at ({2*cos(60)},{2*sin(60)});
        \coordinate (P) at ({2*cos(60)},0);
        \coordinate (D) at (2,{2*tan(60)});
        \draw[black, very thin] (O) circle [radius=2];
        \draw[red,thick] (2,0) arc [radius=2, start angle=0, end angle=60] node[midway,above]{\tiny $\alpha$};
        \draw[blue,thick] (O) -- (C) node[midway,above]{\tiny $1$};
        \draw[blue,thick] (P) -- (C) node[midway,right]{\tiny $\sin\alpha$};
        \draw[blue,thick] (O) -- (P) node[midway,below]{\tiny $\cos\alpha$};
        \draw[green,thick] (P) -- (2,0);
        \draw[green,thick] (2,0) -- (D) node[midway,right]{\tiny $\tan\alpha$};
        \draw[green,thick] (C) -- (D);
        \draw[xshift=-1.1cm,yshift=-1cm] node[right,text width=2.2cm]
        { \tiny $\tan\alpha=\frac{\sin\alpha}{\cos\alpha}$\\$\sin^2\alpha+\cos^2\alpha=1$ };


.. admonition:: Ähnlichkeit = Affine Abbildung

    Man kann dieses Diagramm auf die Größe eines tatsächlichen rechtwinkligen
    Dreiecks skalieren und dieses Dreieck vollständig bestimmen, wenn man eine
    Seitenlänge und einen Winkel desselben weiß.

Die Graphen der obigen **trigonometrischen Funktionen** sind die folgenden


.. tikz:: \begin{axis}
        [
        ymin=-1,ymax=1,
        xmin=0,xmax=2*pi,
        xtick=\empty,
        ytick={-1,0,1},
        extra x ticks={1.5708,3.1416,4.712,6.2832},
        extra x tick labels={$\frac{\pi}{2}$, $\pi$, $\frac{3\pi}{2}$, $2\pi$},
        every extra x tick/.style={
                xticklabel style={anchor=north west},
                grid=major,
                major grid style={thick,dashed,red}
        },
        axis lines = center,
        xlabel=$x$,ylabel=$y$,
        enlargelimits=0.2,
        domain=0:2*pi,
        samples=100,
        axis equal,
        ]
        \addplot [green,thick] {tan(deg(x))} node [midway,left]{tan};
        \addplot [red,thick] {sin(deg(x))} node [above]{sin};
        \addplot [blue,thick] {cos(deg(x))} node [above]{cos};
    \end{axis}

Einige Werte der Funktionen ergeben sich durch Berechnungen am gleichseitigen Dreieck
(`\pi/3`, `\pi/6`) oder am Quadrates der Seitenlänge 1 (`\pi/4`).

`\cos` ist symmetrisch: `\cos(-\alpha)=\cos\alpha` 

`\sin` ist antisymmetrisch: `\sin(-\alpha)=-\sin\alpha`.

Alle trigonometrischen Funktionen haben eine Periode von `2\pi`: `sin|cos|tan(\alpha+2\pi)=sin|cos|tan(\alpha)`.

Weil die spitzen Winkel eines rechtwinkligen Dreiecks sich zu `\pi/2` addieren, gilt

.. math::
    \sin(\pi/2 - \alpha)=\cos\alpha\\
    \cos(\pi/2 - \alpha)=\sin\alpha

