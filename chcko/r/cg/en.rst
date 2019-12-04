.. raw:: html

    %path = "maths/vectors/transformation and inverse"
    %kind = kinda["texts"]
    %level = 11
    <!-- html -->


Coordinate Transformation and Inverse Matrix
============================================

Though convenient it is not a necessity that the basis vectors are independent, 
i.e. orthogonal. 

As an example think of ingredients of cakes as a vector space (*ingedient vector space*).
Then every cake is a vector, an independent choice from more variables, 
which in this case are the quantities for each ingredient (0 for not used at all).

The ingredients can be regarded orthogonal to each other. The context does not 
ask for a detailed comparison. *The dot product is 0.*

Let's compare the cakes in detail though via their ingredients.
Cake A and cake B surely have ingredients in common.
So the unit vectors in the *cake vector space* are not orthogonal to each other
with this comparison. *The scalar product is not 0.*

A vector in the cake vector space (How many of each type of cake?) can be transformed
to the ingredient vector space by multiplying with a matrix. 
Every column in the matrix is the recipe of one cake.

In a matrix and vector written as a set of numbers, every number means
something.  What it means is coded by the position the number takes.  This is
called position coding. The same we do with our number system where the units,
the tens, the hundreds,... have their own position.

In this example the cake space and ingredient space do not necessarily need to 
have the same number of variables (number of variables = dimension). 
We can have 10 ingredients and
3 types of cakes. Then the transformation matrix is 10x3 (10 rows, 3 columns).
Such a `m\times n` matrix with `m\not = n` cannot be inverted, 
i.e. one cannot infer from the ingredients how many of each type of cake are baked. 
Said differently: Not for every combination of ingredients there
is a combination of cakes (linear combination), which needs exactly that amount of ingredients.

If we fix a number for each cake in a smaller assortment of cakes 
we use less information, i.e. we make fewer decisions,
than in the bigger space of ingredients.

.. admontition:: Pseudoinverse

    A non-square matrix can be pseudo-inverted, though: Moore-Penrose Pseudoinverse. 
    For this example multiplying an ingredient vector with the pseudo-inverse 
    would produce a cake vector, which minimizes unused quantities of ingredients
    (Method of Least Squares) or makes best use of the ingredients (Maximum Entropy Method).

If we change from one vector space to another with same dimensions, 
then we can get back to the starting one by multiplying with the *inverse matrix*. 

In order for the inverse to exist, in addition to being square, the
columns/rows of the matrix must be *linearly independent*.  If not, then that
is like effectively being in a smaller matrix (*rank of matrix*). For the
cake example this means that every type of cake must have a different combination of
ingredients, which is some extra information that distinguishes it from the
others and that can be used to code something.

.. admonition:: Linear Independence

    A square matrix can be inverted, if columns (rows) cannot be expressed as
    linear combination of the others, i.e. the rank of the matrix is equal to
    its dimension.

One can calculate the inverse of a square Matrix by:

- leaving out the `ij` cross and calculate the determinant = Minor `M_{ij}`
- change the sign, if `i+j` is odd
- transpose, i.e. mirror at the main diagonal 
  (compare below: `ij` for `A` and `ji` for `M`)
- divide everything by the determinant

Short:

.. math::

    (A^{-1})_{ij} = \frac{1}{det(A)}(-1)^{i+j} M_{ji}


Normally we write `\frac{1}{det(A)}` in front of the matrix, 
but it can be multiplied with every number of the matrix.

For a *2x2 Matrix* `M_{ij}` is the diagonally opposite number.  Because of the
transposing the numbers left bottom and right top (secondary diagonal) stay
where they are, but the sign changes.  At the main diagonal the numbers get
swapped, but since `i+j` is even the sign does not change.

- Main diagonal `\rightarrow` sign stays
- Secondary diagonal `\rightarrow` position stays

