.. raw:: html

    %path = "maths/functions/exponential"
    %kind = kinda["texts"]
    %level = 11
    <!-- html -->

.. role:: asis(raw)
    :format: html latex

Basics
------

In the **exponential function**

.. math::

    y = a^x

- `x` is the **exponent**
- `a` is the **basis**
- `y` is the **exponential function** of `x` on the basis `a`

The **exponent** tells how often *multiplication* with `a` is repeated.
`a` must be a positive real number: `a\in\mathbb{R}`.

.. admonition:: Multiplication

    Multiplication is an operation happening in the real world and we
    encode it with a number.  In the number set `\mathbb{Q}` the operation is
    part of the number: `2` means `\cdot 2`, and `1/2` mean `/2`.  `\cdot`
    stands for the multiplication operation and `/` stands for the 
    *inverse operation*, the division. But the inverse operation is made part 
    of the number by the inclusion of the fractions in `\mathbb{Q}`.
    So we only speak of *multiplication* and mean the application 
    of the operation of `\mathbb{Q}\subset\mathbb{R}`.


If `a` is bigger than `1`, then `y` will increase (grow) with `x` *strictly monotonically*: `x_1<x_2 \Rightarrow y_1<y_2`.

.. tikz:: \begin{axis}[grid=both,axis lines=middle,xmin=-3,xmax=3,ymin=0,ymax=8, samples=50]
     \addplot[green]  {pow(2,x)} node[above]{$y=2^x$};
    \end{axis}

If `a` is smaller than `1`, then `y` will decrease (diminish) with `x` *strictly monotonically*: `x_1<x_2 \Rightarrow y_1>y_2`.

.. tikz:: \begin{axis}[grid=both,axis lines=middle,xmin=-3,xmax=3,ymin=0,ymax=8, samples=50]
     \addplot[green]  {pow(1/2,x)} node[above]{$y=(\frac{1}{2})^x$};
    \end{axis}


Discussion
----------
    
Let's compare the number of combinations of n bits:

.. math::
    
    2^n

with the growing processes, like with accruing of capital with annual compounding

.. math::

    (1+\frac{i}{100})^n

or the especially interesting natural growing

.. math::

    e^x = \lim_{n->\infty}(1+\frac{1}{n})^{nx} 
      = \lim_{m->\infty}(1+\frac{x}{m})^m = (1+\frac{x}{\infty})^\infty

`e` is `Euler's Number <https://en.wikipedia.org/wiki/E_(mathematical_constant)>`_
whose importance is founded on the given relation.

The key to compare them is to understand **information** in the shape of bits as a growing process.
Every bit increases the size by `1` times what is there already. 
Let's denote this aspect of the bit by `(1+1)` to emphasize that an additional `1`
is added to the one there already. The parentheses make this an operator, an element of the number set `\mathbb Q`.
`n` repeated applications of `(1+1)` produces a multitude of size 

.. math::

    (1+1)^n = 2^n

Every new bit is *compounded* to the existing combinations.

The information measure for a real variable of size `C` is the
number of bits `n=\log_2 C` needed to grow `C` combinations.

.. admonition:: Which other variable to compare to?

   Instead of bits we could as well use the considered variable itself because
   that is there physically. But combinations are also physically there and the
   selection of values, which ultimately gives birth to variables, is physical,
   and the number of involved variables plays a role.  First this means that
   information is physical and secondly, considering quantum mechanics, the
   physical number of involved variables is huge and their individual
   contributions are tiny.

If we start from a *number of variables*, the *exponential function*
gives the *number of value combinations*.  If we start from a *number of
values*, the *logarithm* gives the *number of variables* needed to represent
it.

For **interest calculation** we look at an amount of money (the `1`), which is
deposited in the bank with interest `i`.  After `n` years the `1` has grown to 

.. math::

    (1+i/100)^n = q^n
    
The *growth factor* `q` is not `2`, normally just a little above `1`.  The corresponding
"information" measure in this financial context would be the
number of years.

The essential difference with respect to bit information is that, what is added,
is a *fraction* of what is there. But then, fraction is actually just a matter
of units.

The units of living organisms are cells and the ultimate units in the real
world are the quantum particles.  Both of them are small compared to the things
around us. And with such small units one can also *compound* arbitrarily
(infinitely) often:

.. math::

    \lim_{m->\infty}(1+\frac{x}{m})^m = \lim_{n->\infty}(1+\frac{1}{n})^{nx} = e^x

In the first equality we see that, given a certain growth, varying the
*compounding steps* amounts to varying the *growth factor*. Due to the 
importance of `e^x` one often moves the *growth factor* `q` in `y=q^x`
to the exponent of `e` (`y=e^{kx}`). `k=\ln q` is called the *gowth constant*.

.. admonition:: Natural compounding in the finantial world

  Actually in the financial world the real compounding takes place in very
  small steps, just that the bank forwards them to the customer in larger units
  of time.

`x` is the information in the **natural information** unit 
`nat <https://en.wikipedia.org/wiki/Nat_(unit)>`_.  Basically we split up the size
of the variable to infinitely many infinitely small variables, such that 
the growth factor per step is almost `1`.

