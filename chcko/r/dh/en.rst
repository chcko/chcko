.. raw:: html

    %path = "physics/mechanics/forces"
    %kind = kinda["examples"]
    %level = 10 #in school years
    <!-- html -->

.. role:: asis(raw)
    :format: html latex

Structure Analysis Problem solved with Python
=============================================

This pin jointed truss is the initial example take from `akabaila`_

.. _akabaila: http://akabaila.pcug.org.au/StructuralAnalysis.pdf

.. tikz:: \coordinate (A) at (0,0) (A) node [below]{0};
   \coordinate (B) at (0,3) (B) node [above]{1};
   \coordinate (C) at (4,0) (C) node [below]{2};
   \coordinate (D) at (4,3) (D) node [above]{3};
   \coordinate (E) at (8,0) (E) node [below]{4};
   \coordinate (F) at (8,3) (F) node [above]{5};
   \coordinate (G) at (12,0) (G) node [below]{6};
   \coordinate (H) at (12,3) (H) node [above]{7};
   \tikzset{-};
   \draw[black,very thick] (A) -- (B) node [midway,left]{0};
   \draw[black,very thick] (A) -- (C) node [midway,below]{3};
   \draw[black,very thick] (B) -- (C) node [midway,left,below]{2};
   \draw[black,very thick] (B) -- (D) node [midway,below]{1};
   \draw[black,very thick] (C) -- (D) node [midway,left]{4};
   \draw[black,very thick] (C) -- (E) node [midway,below]{7};
   \draw[black,very thick] (D) -- (E) node [midway,left,below]{6};
   \draw[black,very thick] (D) -- (F) node [midway,below]{5};
   \draw[black,very thick] (E) -- (F) node [midway,left]{8};
   \draw[black,very thick] (E) -- (G) node [midway,below]{10};
   \draw[black,very thick] (E) -- (H) node [midway,right,below]{11};
   \draw[black,very thick] (F) -- (H) node [midway,below]{9};
   \draw[black,very thick]  (G) -- (H) node [midway,right]{12};
   \draw[black,thin]  (0,0) -- (1,-1) -- (-1,-1) -- (0,0);
   \draw[black,thin]  (12,0) -- (13,-1) -- (11,-1) -- (12,0);
   \tikzset{->};
   \draw[black,thin]  (4,-1) -- (4,-2) node [midway,right]{100kN};
   \draw[black,thin]  (8,-1) -- (8,-2) node [midway,right]{150kN};
   \tikzset{<->};
   \draw[black,very thin]  (0,4) -- (12,4) node [midway,above]{3x8m};
   \draw[black,very thin]  (13,0) -- (13,3) node [midway,right]{6m};

It can be analysed using force and moment vectors,
because resulting linear equations are neither underdetermined
nor overdetermined, but determined. 
The truss is said to be *statically determinate*.

**We want to find the forces along the members.**

To find all the forces along the members we use:

- no revolution: all moments must be matched by reacting moments
- no translation: all forces in all nodes add to zero.

We will solve this here using ``Python`` with ``numpy`` and ``scipy``
and more precisely we will do with these functions:

.. code-block:: python
    :linenos:

    from numpy import dot, cross, array, allclose, transpose, finfo, double;
    from scipy.linalg import norm, solve;
    unit = lambda v: v/norm(v)
    R90 = array([[0, 1], [-1, 0]]) # rotate 90 degrees
    V = array
    eps = finfo(double).eps

First we need to describe the problem world, i.e. we need to find
the variables. By variable I mean the real thing here. A variable consists of values.
When using a value of a variable, then we do this via reference,
more precisely via index into the list of values representing the variable.

The following describes the system. I use captial letters for variables and
small letters for references to values of the variables. The names are short,
one letter if possible. I take the first letter of the english word. N is Nodes,
E is Edges, F is Forces, S is Support nodes. n, e, f and s reference values of these
variables. A value of Nodes consists of x and y, which reference the external variables
X and Y (the values of). By external I mean that they are not specified in the code.

.. code-block:: python
    :linenos:

    #nodes = x, y
    N = [V((a*8,b*6)) for a,b in [(0,0),(0,1),(1,0),(1,1),(2,0),(2,1),(3,0),(3,1)]];
    #edge = (n1,n2), n_i = indix into N
    E = [(0, 1), (1, 3), (1, 2), (0, 2), (2, 3), (3, 5), (3, 4), 
            (2, 4), (4, 5), (5,7), (4, 6), (4, 7), (6, 7)]
    #external forces = index into N for node of application, vector
    F = [(2,V((0,-100))), (4,V((0,-150)))]
    #support points = indices into N 
    S = [0,6];

Now let's find the forces along the edges.

1. No revolution.

   We need to make the moment created around one support point zero by constructing a force
   at the other support point. If there were more than one other support point for an axis, 
   the system would be overdetermined, which we don't handle here.

.. code-block:: python
    :linenos:

    def react_to_mp_at_q(mp,q):
        """p != q are any nodes.
        m stands for moment. mp is the moment around node p.
        """
        dp=N[q]-N[mp[0]]
        norm_dp = norm(dp)
        if norm_dp == 0:
            return V((0,0))
        ndp = dp/norm_dp
        fq = mp[1]*dot(R90,ndp)/norm_dp
        return -fq

2. No translation

   We distribute the forces to a node to those edges not having a
   force associated yet.  In our 2D case we need two such edges. One is OK, if the
   force is exactly in that direction. 

   .. admonition:: shortcoming 
       For more other edges, I take one edge, if it is in the direction of the
       force and ignore the others.  This is physically not correct, but the
       method applied here is not for overdetermined systems.

   The force placed on an edge via this distribution will be forwarded to the
   other node, but there the direction must be changed: An edge under tension will
   pull from both nodes and a contracted edge will push into both nodes.

.. code-block:: python
    :linenos:

    def distribute(f,es,q):#f = sum of forces on edges es to node q
        ies = [i for i in range(len(E)) if q in E[i]]
        mat = []
        eo = []#edge, other node
        for e in ies:
            if e not in es:
                #E[e]
                t = [tt for tt in E[e] if tt==q][0]#this
                o = [tt for tt in E[e] if tt!=q][0]#other
                d0 = unit(N[o]-N[t])
                mat.append(d0)
                eo.append((e,o))
        A = transpose(array(mat))
        dim = len(f)
        if len(eo)==dim:
            r = solve(A,f)
            for i in range(len(r)):
                ff = r[i]*mat[i]
                yield ff, eo[i]#even if ff==0
        elif len(eo) > dim:
            for i,v in enumerate(mat):
                angle = dot(v,f)/norm(v)/norm(f)
                if abs(angle) < eps or abs(angle+1) < 4 * eps: #same direction
                    yield f,eo[i]
                    return
            raise ValueError('node %i overdetermined'%q)
        else:
            if allclose(unit(f),mat[0]):
                yield f, eo[0]
            else:
                raise ValueError('node %i underdetermined'%q)

The above ``distribute`` needs the edges along which forces come into the node.
We keep track of the edges with forces in a ``{node, [(edge,force)..]}`` dictionary.
Initially this is empty.  We add the external forces and the forces due to the moments.
Then we distribute forces in unbalanced nodes. 

.. code-block:: python
    :linenos:

    def no_revolution():
        EF = dict([(p,[]) for p in range(len(N))])
        for p,ff in F:
            EF[p].append(([],ff))
        for i in range(len(S)):
            for j in range(len(S)):
                if j != i:
                    p = S[i]
                    q = S[j]
                    mp = (p,sum([cross(ff[1],(N[ff[0]]-N[p])) for ff in F]))
                    fq = react_to_mp_at_q(mp,q)
                    EF[q].append(([],fq))
        return EF

    def no_translation(EF):
        _sum = lambda tt: [reduce(lambda x,y:x+y,t) for t in zip(*tt)]
        unbalanced = lambda:[(i,v) for i,v in [(i,_sum(EF[i])) for i in EF] 
                        if v and not allclose(norm(v[1]),0)]
        u = unbalanced()
        while len(u)>0: 
            q,(es,f) = u[0]
            dist=list(distribute(f,es,q))
            for ff,eo in dist:
                EF[q].append(([eo[0]],-ff)) #q is this node of edge eo[0]
                EF[eo[1]].append(([eo[0]],ff)) #eo[1] is the other node of edge eo[0]
            u = unbalanced()
        return EF

    def format_ef(EF):
        from itertools import chain
        from pprint import pformat
        e_f = list(chain.from_iterable([[(tuple(e),norm(f)) for e,f in EF[i]] for i in EF]))
        e_f = list([(e[0],round(f,2)) for e,f in set(e_f) if e])
        e_f.sort()
        return pformat(e_f)

    EF = no_revolution()
    EF = no_translation(EF)
    format_ef(EF)


Here are the resulting forces along the edges:

+--------+--------+--------+-----+-------+--------+-------+--------+-----+--------+-----+--------+--------+
| 0      | 1      | 2      | 3   | 4     | 5      | 6     | 7      | 8   | 9      | 10  | 11     | 12     |
+========+========+========+=====+=======+========+=======+========+=====+========+=====+========+========+
| 116.67 | 155.56 | 194.44 | 0.0 | 16.67 | 177.78 | 27.78 | 155.56 | 0.0 | 177.78 | 0.0 | 222.22 | 133.33 |
+--------+--------+--------+-----+-------+--------+-------+--------+-----+--------+-----+--------+--------+




