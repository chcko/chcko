.. raw:: html

    %path = "maths/functions/log"
    %kind = kinda["texts"]
    %level = 10
    <!-- html -->
    
Logarithm
---------

The power operation generates a result from the basis and the exponent.
So from the result there are two ways back: either to the basis or to the exponent.

- To get the basis one forms the power of the result with the reciprocal of the exponent,
  i.g. `(3^2)^{\frac{1}{2}} = 3`. This is also called root.

- To get the exponent there is the **logarithm**, e.g. `\log_{3}(3^2)=2`.

From the calculation rules of exponents with same basis, e.g. `2^32^2=2^{3+2}` 
and `\frac{2^3}{2^2}=2^{3-2}` follow the logarithm rules that make 
*plus* out of *multiply* and *minus* out of *divide*.

The repetition of multiplication (power) becomes repetition of addition (multiplication).

.. math::

    \begin{matrix}
    \log ab &= \log a + \log b \\
    \log \frac{a}{b} &= \log a - \log b \\
    \log b^c &= c\log b
    \end{matrix}


From the last rule it follows how to calculate any logarithm with just one logarithm.

.. math::

    b^x &= d \\
    x &= \frac{\log d}{\log b}


An exponential equation, i.e. an equation that has the unknown in the exponent,
is solved best by first trying to bring it into the form `b^x = d` and then
apply the logarithm on both sides.

The logarithm always refers to a basis. If the basis is not specified,
then `\log` is either with Basis 10 or with basis e=2.71828182846... (Euler number)

It is

.. math::

    \log_{10} 10 = \log 10 = \text{lg} 10 = 1\\
    \log_e e = \ln e = 1\\
    \log_2 2 = \text{lb} 2 = 1\\
    
