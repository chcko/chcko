.. raw:: html

    %path = "maths/functions/integral of 1÷z"
    %kind = kinda["texts"]
    %level = 12
    <!-- html -->

From real calculus we know, that
`\frac{dy}{dx}=\frac{d\,e^x}{dx}=e^x=y`, and therefore for the inverse `\ln`
`\frac{dx}{dy}=\frac{d\,\ln y}{dy}=\frac{1}{y}` for `y>0`.  For the antiderivative
of `\frac{1}{y}` we can include negative `y`, if we take the absolute value: 
`\int\frac{1}{y}dy=ln|y|+C`.  This follows from the symmetry of `\frac{1}{y}`. 
At 0 there is a singularity, i.e. one cannot integrate over it.

In `\mathbb{C}` we have `e^z=e^{x+iy}=e^xe^{iy}`,
i.e. the real part becomes the absolute value `e^x` and the imaginary part becomes the argument.
That is the reason for the period `2\pi i` along the imaginary axis.
The antiderivative of `\frac{1}{z}` is the inverse of `e^z`,
which means that the absolute value becomes the real part `ln|z|` and the argument
becomes the imaginary part.

`\int \frac{1}{z}dz=ln|z|+i\arg(z)+C`

In `\mathbb{C}` one can integrate around the singularity: 

.. math::

    \oint_{|z|=1}\frac{1}{z}dz = 
    (\ln|z| + i\arg z)\bigr|_{\arg z=0,\,|z|=1}^{\arg z=2\pi,\,|z|=1} = 2\pi i

This is the precursor of the residue theorem.

