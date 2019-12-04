.. raw:: html

    %path = "maths/numbers/representation"
    %kind = kinda["texts"]
    %level = 9
    <!-- html -->

The numbers are their own concepts independent from their representations.

The `wikipedia article <http://en.wikipedia.org/wiki/Numeral_system>`_ 
gives a great overview beyond the 
`positional system <http://en.wikipedia.org/wiki/Positional_notation>`_ 
described here.

Positional System 
=================

It is not possible to give every number its own sign.  Instead we use signs
up to a certain count and then one makes heaps (groups) of that count and
starts counting these heaps.

.. admonition:: Note

    One can compare the numeral system with letters or phonetic systems.
    In a language one combines phonemes to produce a multitude, i.e. the words.
    These are associated/mapped to concepts.
    With Numbers digit signs are combined and then mapped to a count and beyond.

The Decimal System
------------------

- For a count below ten there are signs: 1, 2, 3, 4, 5, 6, 7, 8, 9.
- For "none" there is **0**. Together these are 10 signs.
- For a count ten and above one makes heaps of ten and counts these separately.

Position coding:

    Instead of writing 3 tens and 4 ones we write 3 at a position for the tens
    and 4 for the position for the ones: 34.
    This can be called position coding: Via the position we identify what we mean.

    302 means 3 heaps of tens of tens (hundred), 0 (no) tens and 2 ones.

Position value:
    The value of the position increases from right to left

    ...  10³=1000 10²=100 10¹=10 10⁰=1

    These are powers of 10. 
    10 is the **base** of the decimal system.

    Fractions:

    As heaps of 10 get a position also fractions in 10th get a position to the right
    of the dot (.)

    ,1/10¹=1/10  1/10²=1/100  1/10³=1/1000 ...

The Binary System
-----------------

In the dual system two things make their own heap.

Together with the 0 the binary system has 2 signs, which mean: **there or not there**

The position values of the positions are these

    ...  2⁴=16 2³=8 2²=4 2¹=2 2⁰=1 . `2^{-1}` `2^{-2}` ...

Example

    1011₂ = 11₁₀

The binary system is important, because computers use it and because 2 is the
smallest quantity one can still choose from.

The Hexadecimal System 
----------------------

Here we make heaps of 16.

Together with the 0 we have 16 signs:

    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, A, B, C, D, E, F.

The new ones are A=10, B=11, C=12, D=13, E=14, F=15. 

The position values are:

    ... 16⁴=65536 16³=4096 16²=256 16¹=16 16⁰=1 .  `16^{-1}` `16^{-2}` ...

Because of 2⁴=16, one needs 4 binary digits for one hexadecimal digit.
Since the binary system is important, the hexadecimal is important, too,
and so are other systems with base power of 2,
like. Base 8 (octal), 64 (base64), 128(ASCII) and 256 (ANSI).

Duodecimal System
-----------------

Twelve has many divisors: 2, 3, 4, 6
This allows an easy representation of fractions with these denominators.

But as with the decimal system (1/3 = 0.333...)
the duodecimal system has easy fractions that are periodic (1/5 = 0.2497 2497...).



