.. raw:: html

    %path = "maths/morphisms"
    %kind = kinda["texts"]
    %level = 10
    <!-- html -->

The concept of a function from set theory that maps uniquely elements of one set 
(domain) to elements of another set (codomain),
is tweaked/generalized with the concept of morphism in category theory
in the sense that it puts the whole mapping in the center and combines 
all objects whether domain or codomain into a set of objects O.
Domain and codomain in the set of objects are determined or part of a
morphism (`D_f` is domain of f, `C_f` is codomain of f, both do not need to be sets). 
More morphisms in the set of morphisms M can share the 
same pair (domain, codomain). (O,M,id) is a category. id is the identity morphism.

An important aspect of a morphism is that it maintains the structure in the objects
(order structure, algebraic structure, topological structure) and
depending on the structure the morphisms have special names (`f\circ g (D_g) = f(g(D_g))`):

- Monomorphism: `f\circ g=f\circ h \implies g=h` (left cancellation of `f`) 
  or `f` injective for set objects 
  (`proof <http://www.proofwiki.org/wiki/Injection_iff_Monomorphism_in_Category_of_Sets>`_)

- Epimorphism: `g\circ f=h \circ f \implies g=h` (right cancellation) 
  or `f` surjective for set objects 
  (`proof <http://www.proofwiki.org/wiki/Surjection_iff_Epimorphism_in_Category_of_Sets>`_)
  
- Isomorphism: `f` has `g` such that `f\circ g=id_{D_g}` and `g \circ f = id_{D_f}`
  (left inverse = right inverse) or `f` bijektive for set objects 

- Endomorphism: `X\rightarrow X`

- Automorphism: `X\rightarrow X` + isomorphism

- Homomorphism (Algebra): `f(a+b)=f(a)+f(b)` (different `+` possible)

- Homeomorphism (Topology): `f` and `f^{-1}` continuous

- Diffeomorphism (Differential geometry): bijektive, `f` and `f^{-1}` continuously differentiable



