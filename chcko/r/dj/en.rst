.. raw:: html

    %path = "maths/trigonometry"
    %kind = kinda["texts"]
    %level = 11
    <!-- html -->

.. role:: asis(raw)
    :format: html latex

.. contents::

In the following drawing we have a circle with radius 1.
The length of the arc on such a circle is a measure for the **angle**.
It is called **radian** and the unit is ``rad``. The right angle (90°) is `\pi/2`.
In general 

.. math::

    \frac{\pi}{180}\alpha[°] = \alpha[rad]

By changing this angle one also changes the lengths labeled with `\sin\alpha`,
`\cos\alpha` and `\tan\alpha`. These lengths are determined by the angle,
which is equivalent to say that the lengths are **functions of the angle**.

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


.. admonition:: Similarity = affine mapping

    One can scale this diagram to an actual rectangular triangle and completely
    determine it by knowing one sharp angle and one side.

The graphs of the above **trigonometric functions** are as follows


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

Some values of the functions can be found via calculations on the equal sided triangle 
(`\pi/3`, `\pi/6`) or on a square with side length 1 (`\pi/4`).

`\cos` is symmetric: `\cos(-\alpha)=\cos\alpha` 

`\sin` is antisymmetric: `\sin(-\alpha)=-\sin\alpha`.

All trigonometric functions have a period of `2\pi`: `sin|cos|tan(\alpha+2\pi)=sin|cos|tan(\alpha)`.

Because the sharp angles of the rectangular triangle add to `\pi/2`, we have 

.. math::
    \sin(\pi/2 - \alpha)=\cos\alpha\\
    \cos(\pi/2 - \alpha)=\sin\alpha

