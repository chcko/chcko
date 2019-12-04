.. raw:: html

    %path = "maths/sequences and series"
    %kind = kinda["texts"]
    %level = 10
    <!-- html -->


Sequences and Series
--------------------

A **Sequence** is a function of natural numbers (positive integers).

The natural number is used to refer to the position of an element (term) of the sequence.
It is called index.

- `a_1` is the first element of the sequence
- `a_2` is the second element 
- ...
- `a_n` is the n-th element

If we sum up the first n elements of a sequence,
then we get the n-th element of the sum sequence or **series**.

The use of *function* says:
If I know which position, then I know the number at that position.

Many sequences have a regularity that allows to descibe them in a much shorter way
(short description = low complexity). Here are the most important ones

Arithmetic Sequence
...................

In the arithmetic sequence one element follows from the previous one by adding a contant

`a_{n+1} = a_n + d`.

This is called **recursive** description of the arithmetic sequence.

To get to the n-ten element from the first one, we repeat adding with d for n-1 times:

`a_n = a_1 + (n-1) d`

This is the **term description**:

.. admonition:: note

    In many programming languages one starts with 0, because then you can do
    `nd` instead of `(n-1)d`.

To recognize a sequence to be arithmetic you check whether the differences
between successive numbers stay the same.

Arithmetic Series
.................

If you look at the sum of the first n elements, you can see a regularity,
which is always used to make calculations simpler.

In the above term description you can notice, that starting from the beginning
each element is larger by d, and starting from the end (nth) backward each element
is smaller by d. These operations cancel and therefore we can calculate Count/2 times
sum of first plus nth element.

`\sum_{k=1}^{n} a_k = \frac{n(a_1+a_n)}{2}`

Specifically we have `1+2+...n=\frac{(n+1)n}{2}`.

Geometric Sequence
..................

In the geometric sequence one element follows from the previous one by 
multiplying a constant

`a_{n+1} = a_n \cdot q`.

This is the **recursive** description of the geometric sequence.

To get to the nth element starting from the first one, we repeat multiplying by q for n-1 times:

`a_n = a_1 q^{n-1}`

This is the **term description** of the geometric Sequence.

To recognize a given sequence as geometric, you check whether the quotient of successive elements
stays the same.

Geometric Series
................

In

.. math::

    \begin{matrix}
    1+&q+q^2+...+q^{n-1}&=&S_n\\
      &q+q^2+...+q^n&=&q S_n\\
    \end{matrix}

you see many equal terms. By subtraction you get

`\sum_{k=1}^{n} q^{k-1} = 1 + q + ... + q^{n-1} = \frac{q^n-1}{q-1}=\frac{1-q^n}{1-q}` 

