.. raw:: html

    %path = "physics/circuits/thevenin"
    %kind = kinda["examples"]
    %level = 13 
    <!-- html -->

.. role:: asis(raw)
    :format: html latex


We will derive the gain of a band-stop filter using Thevenin's method.

Our starting circuit is the following from 
`Op Amps for EveryOne (5-10) <http://www.ti.com/lit/an/slod006b/slod006b.pdf>`_.


.. texfigure:: c1.tex
      :align: center

The input voltage is against the ground. We redraw the circuit to reflect this:

.. texfigure:: c2.tex
      :align: center

We want to find `G=\frac{V_o}{V_i}`.  
`V_o` is the voltage at the rightmost R. We will find the Thevenin equivalent there.


.. texfigure:: c3.tex
      :align: center

Next we find the currents using Kirchhoff's current law (KCL) and voltage law (KVL).
There are two loops where current flows. 
There is no current at the R at which we have made an open circuit

.. texfigure:: c4.tex
      :align: center

The resulting equations are

.. math:: \begin{array}{l l l}
    V_i - I_2 R - \frac{I_2}{iwC} - I_1 R & = 0\\
    V_i - \frac{I_1 - I_2}{iwC} - I_1 R & = 0
    \end{array}

We solve for `I_1` and `I_2`:

.. math:: \begin{array}{l l}
    I_1 &= \frac{\omega C V_i (-2 i+C R \omega)}{-1-3 C R i \omega+C^2 R^2 \omega^2}\\
    I_2 &= -\frac{i \omega C V_i}{-1-3 C R i \omega+C^2 R^2 \omega^2}
    \end{array}

The small loop at `V_{th}` with the now known currents can be used to calculate

.. math:: V_{th}=\frac{I_2}{iwC} + I_1 R

Next we will need the Thevenin impedance equivalent. For this we remove the source `V_i`
and calculate the impedance as seen from `V_{th}`.

.. texfigure:: c5.tex
      :align: center

We redraw to see a little better, what is parallel and what is serial

.. texfigure:: c6.tex
      :align: center

With this we get

.. math:: Z_{th}=\left(\frac{1}{i \omega C}+\frac{R \frac{1}{i \omega C}}{R+\frac{1}{i \omega C}}\right) || R = 
    \frac{R (1+2 i \omega C R)}{1+3 i \omega C R - C^2 R^2 \omega^2}

and

.. math:: V_o = \frac{R}{R + Z_{th}}

Then we finally have the **gain**:

.. math:: G = \frac{V_o}{V_i} = \frac{(-i+C R \omega)^2}{-2-5 i \omega C R+C^2 R^2 \omega^2}
    = \frac{(1+i \omega C R)^2}{2+5 i \omega C R-C^2 R^2 \omega^2}
    = \frac{(1+ s\tau)^2}{2+5 s\tau+(s\tau)^2}

We have replaced `\tau=R C` and `s=i \omega`, as is custom for filters.
The denominator can be solved for `s\tau` (-4.56,-0.44) and the product of the solutions is 2.
Therefore

.. math:: G = \frac{(1+ s\tau)^2}{2(1+\frac{s\tau}{0.44})(1+\frac{s\tau}{4.56})}

