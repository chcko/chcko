.. raw:: html

    %path = "maths/functions"
    %kind = kinda["texts"]
    %level = 9
    <!-- html -->

A **function (= mapping)** can be seen as set of value pairs `(x,y)` with
`x\in X` (**domain**, **preimage**) and `y\in Y` (**codomain**, **image**, **range**). 
Important is the **uniqueness** of the image: for any `x` there is exactly one `y`.  
`x` can be freely chosen. `x` is **independent value, preimage, argument or position**.  
`y` is determined by `x`. No new information is needed to select `y`. 
This is why functions are important. 
`y` is called **(dependent or function) value or image**.

If the uniqueness is not satisfied, then it is called a **relation**.

A function `f` as a direction from the set of all `x` (`X`) to the set 
of all `y` (`Y`). This is notated as `f:X\rightarrow Y`.

The value pairs normally cannot be written down because too many or infinite.
Therefore one describes the function via an **analytic expression**, i.e.
`y=x^2+1`. This basically is an algorithm, a program.

.. admonition:: Basic Concepts: 

    - domain
    - codomain
    - mapping

If we do not want to have a separate letter `f` for the mapping,
we can write: `y(x)`, i.e. the parentheses say that 
`y` follow from `x`, i.e. is function of `x`.
Sometimes `f` can mean both the mapping or the function value.
    
If we concentrate only on the mapping, instead of `g(f(x))` 
we can write `g\circ f` meaning: first we map via `f`, then via `g`,
i.e. the ordering is the same in both writings.

There can be more `x` with the same `y` and it is still a function.
If there is only one preimage `x` for a `y`, then the function
is **injective**, i.e. it keeps the distinction or does not loose information.  
If in addition every element of `Y` is reached (**surjective**),
then the function is **bijektive**. 
In this case by choosing `y` we also choose `x` (`x(y)`, **inverse function**).

If the images of elements that are close together are also close together,
then the function is **continuous**. Close is intuitive, but still needs
a formal definition. This is done via a **metric** `d` (`d(x,y)\ge 0`,
`d(x,y)=d(y,x)` and `d(x,z)\le d(x,y)+d(y,z)`, e.g. `d(x,y)=|y-x|`) 
(or in a more abstract way in topology via sets of nested open sets).

.. admonition:: Continuity at `x`

   For every `\varepsilon > 0` there is a `\delta`, such that
   for all `y` with `d(x,y)<\delta` we have `d(f(x),f(y))<\varepsilon`. 

   For every `\varepsilon`-neighbourhood there is a `\delta`-neighbourhood.
    
A function does not presuppose order of domain and codomain. But if it is given,
then a function is said **(strictly) monotonically increasing**,
if `x\le y` (`x<y`) makes `f(x)\le f(y)` (`f(x)<f(y)`).
Analogously one defines **(strictly) monotonically decreasing**.

Morphisms are related to functions (see :lnk:`r.cs`).

Regarding graphical representation of a function in a **coordinate system**: 

- First values of variables `X` and `Y` are mapped via units to numbers
- A unit for the graph is chosen (e.g. cm).
  The ratio of unit in graph to unit in reality (kg, km, m/s,...) is the **scale**.
- For a value of the independent variable `X` one goes the number
  of graph units to the left (`x`-coordinate, abscissa).
- For a value of the dependent variable `Y` one goes the number of 
  graph units upward (`y`-coordinate, ordinate).
- This one repeats for a few pairs of values. 
  These `(x,y)`-pairs can also be written into a table as a intermediate step
  (**value table**).
- Since usually it will be a continuous function,
  one can connect the points with a continuous line.
  If the line is linear then it is called a **linearen function**.

Examples of graphs for fundamental types of functions of one variable 
can be found here: :lnk:`r.cf`.

