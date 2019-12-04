.. raw:: html

    %path = "maths/operations"
    %kind = kinda["texts"]
    %level = 9
    <!-- html -->

A very basic operation is the **addition**.
Addition can be seen as cardinality of the union of two disjoint sets.

    `|M\cup N|=|M|+|N|` if `M\cap N = \emptyset`

This abstract view can be applied to concrete cases, if we identify the unit of
a resource (length, mass, ...) with an element and there is no overlapping,
because the resource can be dispatched only once.

In the application one must take the physical system into account though.
For example elastic rods inserted vertically into a tube might not add their
lengths due to their elasticity and weights.
Volumes of liquids when mixed might not add, because the molecules can 
use the space more efficiently in the mixture.

**Multiplication** one first encounters when calculating the area of a rectangle.
One either can add all unit squares (Addition) or 
one repeats (multiplication) the rows or the columns (commutativity of `\cdot`)
If we address every unit square with coordinates `(i,j)`, then multiplication 
counts all combinations of `0 <= i <= a` and `0 <= j <= b`, which yields `a\cdot b`.

In a square of side length `a` one has `a\cdot a` unit squares, in a cube of
side length `a` one has `a^3` unit cubes ...  Here we count combinations of a
set `M` `n` times with itself.  `|M\times \dots \times M| = |M|^n`.  Thus we
have come to the **power** operation. 

- Multiplication is a shorthand for addition. 
  So multiplication is a second level operation.

- Power is a shorthand for multiplication.
  Power therefore is a third level operation.

**Operation** is another name for **function** (:lnk:`r.cr`), if certain rules
like **assoziative law** or **commutative law** apply.  An **operation** can
easily be made to a new set by combining it with a value {(value,operation)}.
(see Zahlen: :lnk:`r.ci` and `lambda calculus <http://en.wikipedia.org/wiki/Lambda_calculus>`_).  
These are then sets of instructions or **operators**, which can be applied to
other values of other variables, e.g. 3m = (3,times) m, i.e. 3 = (3,times).

