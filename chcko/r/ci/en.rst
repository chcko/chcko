.. raw:: html

    %path = "maths/numbers/NZQR long"
    %kind = kinda["texts"]
    %level = 9
    <!-- html -->

.. contents::

This is not a first introduction to number,
but a discussion and interpretation with links to further resources
and an emphasis on algorithmic aspects (:lnk:`r.cp`).

Natural Numbers (`\mathbb{N}`)
------------------------------

The natural numbers are the real numbers in the sense that they represent a
count. All other sets of numbers have additional information or are quite
different altogether

The **count** is a real variable, which specifies the **cardinality** of a set. 
A value of this variable, like three, means three things.
Further properties are not considered, they are abstracted away.
That is why every natural number can be seen as **equivalence class** (:lnk:`r.co`).

.. admonition:: Note

    In mathematics one makes a further distinction: **cardinal numbers** as above
    and **ordinal numbers** to specify the order.

The intuitive idea of `\mathbb{N}` is formalized with the
`Peano Axioms <http://de.wikipedia.org/wiki/Peano-Axiome>`_.

.. admonition:: Note

    Essentially `\mathbb{N}` is a construction 
    of an ordered multitude (0 with successors), 
    to address values of other variables (like count),
    just like words address concepts.

Zero 
....

Zero was a great invention for the number representation, which the roman
system did not yet have. In general one can now include variables, even if they
are not there every time. This often helps to generalize description. As an
example in 103 the position coded tens variable is there, even if there is no
ten grouping in the number (:lnk:`r.cn`). Another example are vectors
(:lnk:`r.cg`).

The Integers `\mathbb{Z}` and the Addition
------------------------------------------

`\mathbb{Z}` is more than the count.

As motivation for the integers one can add to every element of `\mathbb{N}`
a process or a direction. 2 is then not only the count 2,
but has the additional information to add the 2 things (`2 = {2,+} = +2`).

If you understand `\mathbb{N}` already associated with a process
or direction, then it is a good idea to extend this to include
the same values but the undoing process or counter direction
to get back to the original situation. This way one intuitively comes
to the integers `\mathbb{Z}`.

`+` means to add and `-` means to subtract, but that can change. 
The `+` is often dropped, but it must be implicitly assumed, 
because an integer is not the same thing as a natural number.
It has additionally the reversible process or direction.

If you understand only count with `\mathbb{N}`, 
then `\mathbb{Z}=\mathbb{N}\times\{+,-\}`. 
Then `\mathbb{N}` is not a subset of `\mathbb{Z}`, but an
`isomorph <http://en.wikipedia.org/wiki/Homomorphism>`_
`embedding <http://en.wikipedia.org/wiki/Embedding>`_.

.. admonition:: Note

    An formal introduction of `\mathbb{Z}`, starting from `\mathbb{N}` with as few new concepts
    as possible (no `+` und `-`), is via **equivalence classes** (:lnk:`r.co`) 
    of number pairs `(n,m)` from `\mathbb{N}` with the equivalence relation: 
    `(n_1,m_1)\sim(n_2,m_2)\equiv n_1+m_2=n_2+m_1`.
    In the canonical representation one number is 0. `+2 = (2,0)` und `-2 = (0,2)`.

With `+` and `-` as opposite processes one has encoded this process in the number.
The `Addition` itself is then algorithmically a sequential execution or **sequence**:
`+2+(-2)` means: add 2 then(=+) subtract 2.
If you swap the numbers `((-2)+(+2))` you get the same result (**commutative law**).
With more numbers you can choose freely which to calculate first
`(-2)+((+2)+(+3))=((-2)+(+2))+(+3)` (**associative law**).

.. admonition:: Note

    The subtraction 2-2 is an abbreviation for +2+(-2).

The result of +2+(-2)= 0, the **neutral element** of addition.
+2 is the **opposite number (additive inverse)** of -2 and vice versa.
`(\mathbb{Z},+)` is an **abelean Group** (:lnk:`r.cl`).

.. admonition:: Note

    `+` as part of the number and `+` as binary operation are not the same.
    Similarly for `-`. `-` in addition can be a unary operation that returns the 
    opposite number (additive inverse).

The Integers `\mathbb{Z}` and Multiplication
--------------------------------------------

A process can be repeated and multiplication says how often
addition (+2) or subtraction (-2) is repeated.  Algorithmically multiplication 
is a loop:

    `3\cdot(-2) = (-2)+(-2)+(-2)`

Multiplication with 1 means the thing itself.
1 is the **neutral element** of the multiplication.

The multiplication with -1 means: revert the process,
i.e. make plus (+) to minus (-).

    `(-1)\cdot(-2) = +2`

    `(-1)\cdot(-1)\cdot(-2) = -2`

With this one can multiply every integer with every other integer and one gets
an integer again.`(\mathbb{Z},\cdot)` is **closed** and the **assoziative law**
holds.  This makes `(\mathbb{Z},+,\cdot)` to an **integrity ring**
(:lnk:`r.cm`).  `(\mathbb{N},+,\cdot)` alone is only a **semiring**
(:lnk:`r.cm`) .


Multiplication und die Rationalen Numbers (`\mathbb{Q}`) 
--------------------------------------------------------

Analogous to `\mathbb{Z}=\mathbb{N}\times\{+,-\}` one can 
think the repeating process united with the number and it is a good 
idea to include the inverse process (dividing).

Which subtraction do I need to repeat 3 times in order to get a (-6) subtraction?

    (-6)/3 = -2

Analogous to `\mathbb{Z}=\mathbb{N}\times\{+,-\}` one can unite
`\mathbb{N}\times\{\cdot,\div\}` with the count multiplication and division.

The binary operations `\cdot` and `+` must be handled separately,
only the **distributive law** ties them together.

    `a\cdot(b+c) = a\cdot b + a\cdot c`

    e.g. `2\cdot(3+4)=2\cdot 3+2\cdot 4=14`

If you look for the part that repeated (multiplied)
yields no change, i.e. 1, then we get to the **reciprocal**,
which is the **inverse element of multiplication**.

While with (-6)/3 we still get a whole number, i.e. a multiple of 1,
this is not the case for the reciprocal in general.

Therefore the set is extended by these reciprocals to make it closed.
This is analogous to the extension from `\mathbb{N}` to `\mathbb{Z}`.

- There the process "add" was united to form a tuple (count,add).
  "add" has a reverse process "away".
  One has extended by (count, away).

- With `\mathbb{Q}` one extends (count,repeat) with the *reciprocal* (count,divide).

.. admonition:: Note

    In analogy to `\mathbb{N}\times\{+,-\}`
    one could write `\mathbb{Q}`-elements as:

    - `\cdot 2` corresponds to +2
    - `\div 2` corresponds to -2

    The binary operation `\cdot` then is only a successive processing and can be dropped.

    `(\cdot 2)\cdot(\div 2) = \cdot 2\div 2 = 1`

    But actually we write

    - `2\cdot 2^{-1} = 1` or
    - `2\cdot \frac{1}{2} = 1`

    the first is because one can add the exponent for the same basis
    and so we have `2\cdot 2^{-1}=2^1\cdot 2^{-1}=2^{1-1}=2⁰=1`.


`(\mathbb{Q},\cdot)` is a **abelean Group** with neutral element 1.

Because the multiplication in `(\mathbb{Q},\cdot)` shall yield an element of 
`(\mathbb{Q},\cdot)` again (closure), one takes all fractions
`p/q=pq^{-1}` into `(\mathbb{Q},\cdot)`.  
3/2 means to first do `\cdot 3` and then `\div 2` (reciprocal of 2).

    `\frac{3}{2}=3\cdot 2^{-1}=3\frac{1}{2}=\frac{1}{2}\cdot 3=2^{-1}\cdot 3`

`pq^{-1}` means to copy/repeat p times then divided q times.
To additionally multiply r times and undo that by dividing r times, 
one doesn't change a thing.

    `pq^{-1}=rr^{-1}pq^{-1}=rp(rq)^{-1}=\frac{rp}{rq}`

All such pairs of numbers are equivalent and the canonical representation is 
with p and q without common divisor.

.. admonition:: Hinweis

    `\mathbb{Q}` formally is introduced as set of equivalence classes
    of such equivalent number pairs:
    `(n_1,n_2)\sim(n_2,m_2)\equiv n_1m_2=n_2m_1`.


`\mathbb{R}` as extension with the irrational numbers `\mathbb{I}`
------------------------------------------------------------------

Count (`\mathbb{N}`) with addition (+) and subtraction (-) is `\mathbb{Z}`.
`\mathbb{Z}` with repetition (`\cdot`) and division (`\div`) is `\mathbb{Q}`.
If we stay with `+,-,\cdot,\div`, then we can do with `\mathbb{Q}`.

But if we want the power operation to be reversible, then we must extend again.
There is for example no `p/q` in `\mathbb{Q}`, for which `p^2/q^2=2`. 
(Proof: p/q shall have no common divisor. If `p^2` is even, so is p (p=2n).
`p^2=4n^2=2q^2` means that q is even, but that is a contradiction).

There are though **algorithms** that make rationale Numbers (**sequences**),
whose square gets arbitrarily close to 2. All such algorithms are 
combined into a equivalence class and this is then the new number `\sqrt{2}`

The irrational numbers `\mathbb{I}` are equivalence classes of number
sequences.  By naming the algorithm, and `\sqrt{}` refers to such an algorithm,
the irrational number is determined. One cannot write an irrational number as
decimal number. One can also not run the algorithm to an end, because it 
does not terminate. So the irrational number is really the algorithm itself.

The irrational numbers get further classified as **algebraische** irrationals,
which are those that are roots of polynomials, and the **transcendental**
irrationals.  The latter exist, because there are functions beyond finite
polynomials, like Sin, Cos, ... most of which can be expressed with infinite
polynomials (series), though. `\pi` and `e` are transcendental.

New operations/functions lead to new numbers. But the definition 
**equivalence classes of sequences** is so general that it 
includes algebraic and transcendental numbers and `\mathbb{Q}` itself.

This is `\mathbb{R}`:

    `\mathbb{R} = \mathbb{Q} \cup \mathbb{I}`

Another very useful and exciting extension are the complex numbers `\mathbb{C}`(:lnk:`r.di`).

.. admonition:: Note
    
    Since `\mathbb{R}` includes all never ending number sequences, one could
    include `\infty` and `-\infty`, which are also never ending sequences of
    numbers, if it weren't for `\infty+1=\infty` and the like. 
    Still in complex analysis (function theory) the complex number set is 
    extended with `\infty` fruitfully.



