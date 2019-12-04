.. raw:: html

    %path = "maths/entropy"
    %kind = kinda["texts"]
    %level = 12
    <!-- html -->

To exclusively select an element v (value, state, point) of a variable V 
(cardinality `|V|=n`, n-set) we need `\log_bn` b-sets (normally `b=2`, bit).

.. math::

    I(V)=log\;n

`I(V)` is the code width of the variable, i.e. die information (in bits) needed
to select a value and it is the same for all values. `I` is a property of the variable.

.. admonition:: random variable, variate, variable

    A variate is a random variable.

    Often the distinction between random variable and variable is not 
    necessary. Both mean a real quantity, whose values can occur repeatedly.

If we consider every occurrence `c \in C` of values of `V`,
then there is another way to refer to values of `V`. 
We first choose an occurrence of any value with  `I(c)=\log |C|`
and subtract the information to select occurrences of `v\in V` (`I(c_v)=\log |C_v|`).
`\frac{|C|}{|C_v|}` is the number of `|C_v|` sized subsets of `C`.  
So to select such a `v` occurrences subset we need

.. math:: 

    I(v)=\log\frac{|C|}{|C_v|}=-\log\;p(v)

This is different for all `v\in V` and represents the optimal code length for every value
(entropy code, Huffman code).

The average code width is

.. math::
    H(V)=-\sum_vp(v)\log\;p(v) 
    
`H(V)` is the **entropy** of the variable `V` (note: not of a value of `V`).

The information in a variable depends on the probability distribution 
of value occurrences (= random event).

