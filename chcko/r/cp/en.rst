.. raw:: html

    %path = "maths/maths+information"
    %kind = kinda["texts"]
    %level = 9
    <!-- html -->

Computer and Mathematics
------------------------

We humans process information and also have abstracted the rules 
by which this is done. The result is mathematics.

The computer processes information by applying these rules.
It can even be used to find new rules, new paths, new proofs.

The computer science in this sense is a part of mathematics,
now with many extensions which are specifically applicable 
to the computers of our times.

Since man has the computer now, we will not only let it calculate, but
successively use for all kinds of formalized thought processes.  Autonomous
learning, abstracting and synthesizing (creative tasks) can also take over by
computers, although that is still in its infancy.

The computer not only makes calculations unbelievably fast but has the
potential to take over most of the thought tasks, we humans are capable of.

Mathematics deals with information processing, but what is that?

Information
-----------

The communication between to humans, where information is exchanged,
can be broken down to an elementary process.

This process consists of

- a set, one can choose elements from (choice)
- the choosing process (decision, ...)

The selection is a repeated process.
All selections make up a **mapping**.
An element can be chosen exclusively only and every element gets it turn. 

.. admonition:: Note

    The smallest set one can still choose from has 2 elements.
    That is why the **bit** is the smallest unit of information.

The sender chooses concepts in his head, maps them to words,
maps them to phonetic combinations or sign combination and sents
them over a medium (air, paper) to the receiver.
The receiver processes in the opposite direction.

Phonemes, letters and digits are there to create a multitude (word, numbers)
to which concepts can be mapped (coding).

.. admonition:: Note
    
    With numbers one can choose everything one can choose everything 
    one can choose with words. One way is to put all concept into a
    sequence (array, row) and let the number choose the position 
    (lookup table). Words in our brain are used associatively,
    but that is possible with numbers, too.

Basically all dynamic system work with the above elementary selection process.
There are always sets and choices.
Examples:

- Biology: Variants via mutation and selection through the natural environment,
  i.e. the other individuals and the habitat.
- Economy: supply and demand
- Society: organizations and their success
- Politics: politicians and voters
- Science: theories and their usefulness to describe phenomena
- Ideas and their supporters
- random thoughts in our brain and checking via experience stored in the brain
- ...

Since quantum mechanics we know that randomness is an inherent principle of nature,
that not everything is predetermined, but that selection processes do really 
create new combinations, fleeting ones and staying ones.

Nature processes information by distributing states 
The universe can thus be compared with living systems like us.
We work with the same abstract principle of information processing.

Energy, Entropy
...............

:inline:`r.cv`

`\Delta Q=T\Delta S` from classical thermodynamics says
that the energy transport (heat transport) is proportional to the entropy
with temperature (in °K) as factor.

In a philosophical fuzziness these physical concepts can be interpreted in the following way:

- energy = number of states (cardinality of the set, information)
- entropy = distribution thereof = information
- selection = energy transport
  = information transport to increase entropy

Mathematics and Information
---------------------------

We have recognize the elementary process of information (transport) to
be the selection which consists of

- set
- choosing

Let's connect this better with mathematics?

Sets and Variables
..................

The set we find in the set theory, the foundation of mathematics.

To choose elements from a set one can reserve a bit for every element
and code a selection via 0 (not used) and 1 (used).
One can do with less bits, if one first finds out, which elements
exclude each other.

A set one can choose one element exclusively we call variable.
The element is the value.

.. admonition:: Variable

    Variablen bestehen aus Werten.

With variable we mean the real thing, not a placeholder for a number.
Only via a mapping, e.g. by comparing to a unit, the value is linked to a
number (coordinate).

Mathematics describes reality by finding variables and then dependencies
between them.

Strukture
.........

An important aspect of information processing is abstraction.  By comparing one
finds common patterns and these are used to build a smaller encoding
(description) and to recognize later.  In programming there is an important
guideline: Don't Repeat Yourself (DRY).  That's how mathematics does it as
well. Patterns that repeat are described abstractly and concrete objects become
examples of these structures (group, ring, field, ...).

This makes information exchange (communication) more effective. Instead of
repeatedly describe, e.g. the rules for `+` in `\mathbb{Z}` and `V` and so on
one can say `(\mathbb{Z},+)` and `(V,+)` and so on are groups.

Mathematics as science builds a structure as a whole by successively adding new
concepts and theorems.  New works build on these concepts, choose what to work
on, and thus extend the structure.

.. admonition:: Struktur

    This successive extension and sophistication of structure
    is a general developement of dynamic systems (evolution):
    biological evolution, economy, ... (see above).

    In order for complex and lasting structure to develop
    energy must be supplied in the right dosage.
    For the economy this is the money.
    

Algorithmics
............

To determine (choose) a value of a variable mathematics uses the **function**.
This is also the name in informatics, but with a slightly different meaning,
Other names are subprogram, subroutine, procedure, ...

:inline:`r.cw`

The value of one variable can depend on the values of more other variables.
Function therefore have more parameters. They are called **formal parameters**
in the definition of the function.  A first selection process there is already
when choosing the **actual parameters** to correspond to the formal ones when
calling the function. 

Functions in programming languages do not necessarily return the value of a
variable, but it is a good design to name variables and the elementary
dependencies via functions in order to clearly separate them from others. 

Functions consist of calls to other functions

- Successive calls are a **sequence**.
- Decisions, which calls to do under which conditions, are **branches**.
- Repeated execution of blocks of calls are a **loop** 

This algorithmics is hidden everywhere in mathematics behind numbers,
expression and symbols (polynomials, `\sqrt{}`, `\lim`, `\int`, ...) in
theorems and proofs.  The whole of mathematics can be regarded as a huge
program, but unfortunately still most of it in a language that the computer
does not understand.

.. admonition:: Representation

    A big challenge is to convert the representation of mathematics 
    into a language the computer can understand.
    There are many computer languages, some especially made for mathematics.

    Many different representations increase the effort
    and reduce the applicability.

    The same is true for human languages.

    
.. admonition:: Numbers

    When introducing the number systems algorithmic aspects are combined
    with the count (the natural number):

    - Count with + and -: Integers

    - Count with * and /: Rationals

    Then we can regards 

    - Numbers as elementary instruction (add 2, subtract 2, ...)

    - analytic expressions as programs/functions

    - term simplification as program simplification, profiling


.. admonition:: Equations

    The equation is a function that returns the result of a comparison.
    Equivalent transormations of an equation is a kind of profiling, too.

    Equations and inequalities are used to implicitly define sets.


