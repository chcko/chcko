.. raw:: html

    %path = "maths/numbers/C"
    %kind = kinda["texts"]
    %level = 10
    <!-- html -->

.. contents::

The complex numbers `\mathbb{C}`
--------------------------------

The real numbers (:lnk:`r.ci`) are more than just a count.

- There is also direction (`+` or `-`). Now we will extend this to all directions in a plane.

- In `\mathbb{R}`` we invert the direction with multiplication by `-1`. We extend this to rotation to any direction.

In `\mathbb{R}` `x^2` only assumes positive values. The equation `x^2+1=0` does not have a solution.

So we invent a "number" `i` that satisfies `i^2=-1`.

`i` is called **imaginary unit** and its multiples are called imaginary
numbers. `i` is like apple or orange. It has nothing to do with
the unit `1`. The imaginary numbers are orthogonal to `\mathbb{R}`,
which means you can choose from these two sets independently.
All combinations form a 2-dimensional space, 
i.e. a plane, the **complex plane**.

    `z = a + ib \in \mathbb{C}`

is also a two-dimensional vector: 2 orthogonal directions that can be added independently.

There are two representations

- `z = a+ib`, i.e. via the components or
- `z = r(\cos\varphi + i\sin\varphi)` via modulus `r` and artument `\varphi` (angle, phase) in radiants.

Now consider the following:

- `i\cdot 1 = i`, i.e. multiplication with `i` make 1 to `i`, which is orthogonal to 1,
  the **real unit**. This is a rotation by a right angle.
- `i\cdot i = -1`. Again a rotation by a right angle. 

Generally: Multiplication with `i` produces a rotation by the right angle.

Since two multiplications (`x^2`) are supposed to invert (rotate by `\pi`) 
one multiplication should rotate by half of it (`\pi/2`).

When multiplying exponentials, the exponent gets added.
This gives a hint that there could be a representation that has the angle in the exponent.

In trigonometric addition formulas (e.g. `\cos(\alpha+\beta)=\cos\alpha\cos\beta-sin\alpha\sin\beta`),
multiplication adds the angles.

Finally developing `\sin` and `\cos` into a Taylor series and comparing with the `e^x` series 
leads to the **Euler Formula**:

- :inl:`r.cy` 

`z=re^{i\varphi}` is a usual way to represent complex numbers.

About `\sin` and `\cos` we know that the period is `2\pi`, therefore this is
true for `e^{i\varphi}`.  The nth root divides the period up to `2n\pi` to
below `2\pi` and so we have `n` different roots.

.. math::

    z^{1/n}=r^{1/n}e^{i(\varphi/n+2k\pi/n)}

More generally: 

   In `\mathbb{C}` every polynomial of degree n has exactly n roots
   (**fundamental theorem of algebra**), if one counts the multiplicity 
   of roots. `\mathbb{C}` therefore is called **algebraically closed**.

This means that not only `x^2`, but every polynomial maps the whole
`\mathbb{C}` to the whole of `\mathbb{C}`.

.. admonition:: Note

    In function theory one learns that this can be extended to all functions
    that are infinitely often differentiable (analytic or holomorphic) in all of `\mathbb{C}` 
    (entire functions), because they can be developed into a Taylor series.

Further properties:

- a = Re(z) is the real part

- b = Im(z) is the imaginary part

- `\bar{z}=re^{-i\varphi}=a-ib` is the complex conjugate of z. `\bar{z^n}=\bar{z}^n`.

  `z_1\bar{z_2}` combines in itself dot product (`Re(z_1\bar{z_2})=r_1r_2\cos\Delta\varphi`) 
  and vector product (`Im(z_1\bar{z_2})=r_1r_2\sin\Delta\varphi`).

- `|z| = \sqrt{z\bar{z}} = \sqrt{a^2+b^2} = r` is the absolute value (modulus) of z.

  The square over the length of a complex number independent of direction 
  is given by `z\bar{z}` and not by `z^2`.

- `φ = arg(z)` is the argument (phase) of z. 

  - `arg(z_1z_2)=arg(z_1)+arg(z_2)`

  - `arg(\frac{z_1}{z_2})=arg(z_1)-arg(z_2)`

Application of `\mathbb{C}` 
...........................

Since `\mathbb{C}` is a extension of `\mathbb{R}`, 
one can do everything with `\mathbb{C}` that you can do with `\mathbb{R}`.
The essentially new is that `\mathbb{C}` includes all directions not just `+` and `-`.

What is a direction?

:inline:`r.ct`

The complex numbers are used in physics and technology in connection with vibrations and waves
and there are many of them:

- mechanics/solid state physics: water waves, acoustic waves, elastic waves, ... 

- Electricity: alternate current, alternate current circuits (resistance, capacity and inductance),...

- Electrodynamics: Electromagnetic waves (light, radio), ...

- Optics: Light, ...

- Quantum dynamics: particle waves, ....

Basically applications of complex numbers are due to 

- the fact that unrestricted calculation is possible in `\mathbb{C}` and 

- further results in function theory.

Many physical systems are described with differential equations.
These can be reduced to polynomial and then one gets complex numbers as roots.


