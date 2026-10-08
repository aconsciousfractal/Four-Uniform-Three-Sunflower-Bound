# Exact trace identifications, margins and high-point rigidity

These ordinary arguments apply to a finite simple SF4 family, with no three-sunflower including empty core. An anchor is an actual member. A large index means singleton trace size at least eight; a high point means global degree at least nineteen. No neighbourhood threshold or support cutoff is assumed.

The paper supplies the universal SF2 capacities (lemma `lem:sf2`), the intersecting I8/I9/I10 classification (proposition `prop:i810`), isolation (`lem:isolation`), separation B4 (`lem:b4`), the SF3 bound20 (`cor:triple20`) and the current high-link decompositions (`lem:r16maximal`, derived from `thm:r16class`). The labels A1/B4/B5/C1 used below refer to these statements. The P10 model is denoted P or mathcal P below; P9 is P10 with one block removed, and Q is Q8.

A fact used below is that an intersecting SF3 family with more than six triples has no point of degree six. Indeed the complete link of a degree-six point is the SF2 maximum graph 2K3. A triple avoiding that point would have to meet every edge in both disjoint triangles, requiring at least two points in each triangle. A three-element set cannot do that. Thus every triple would contain the degree-six point and the family would have exactly six members. This uses only the SF2 maximum and actual pairwise intersection.

The rooted finite signatures at size eight or greater are the complete rooted forms of the universal I8/I9/I10 models. The following arguments keep both equality and distinction of extension points, rather than replacing them by counts.

## D. Exact traces, identifications and margins

For a family \(\mathcal F\) of quadruples and \(R\in\mathcal F\),
\(s_x,p_{xy},t_m\) count the members whose traces on R are respectively
\(\{x\},\{x,y\},R\setminus\{m\}\). Set
\[
S=\sum s_x,\quad P=\sum p_{xy},\quad T=\sum t_m,\quad
r_x=\sum_{y\ne x}p_{xy},\quad h=S+P+T=|N[R]|-1.
\]
The number P is distinct from the family \(\mathcal P\).
The complete link
\(\mathcal L_x=\{B\setminus\{x\}:x\in B\in\mathcal F\}\)
is sunflower-free. Its part \(\mathcal H_x\) disjoint from the anchor
\(R\setminus\{x\}\) has size \(s_x\); the remaining part
\(\mathcal K_x\) has size
\[
k_x=1+r_x+T-t_x,\qquad d(x)=s_x+k_x.
\]
The residual sets of each nonempty proper exact trace on R are intersecting
and sunflower-free: two disjoint residual sets, together with R before the
trace is removed, would give a sunflower. Hence
\[
s_x\le10,\quad p_{xy}\le3,\quad t_m\in\{0,1\},\quad d(x)\le20.
\]
For p we use the bound three for intersecting sunflower-free graphs;
for t, two distinct singleton residual sets would be disjoint.
The last bound is the paper's universal SF3 bound20.

An index is **large** if \(s_x\ge8\), and small otherwise.
For a large index, the paper's separation lemma B4 ensures that \(\mathcal K_x\)
is intersecting and \(k_x\le10\). The following consequences retain
identifications of exterior points, in addition to their counts.

### D.1 Compatibility

#### D.1.1 For every large index, \(r_x\le6\)

If all three \(p_{xy}\) are at most 2, this is immediate. Otherwise a class
of three pair residual sets forms a triangle: a three-edge star is forbidden.

Let \(V\) be the support of this triangle, in the class \(\{x,y\}\).
For \(z\ne x,y\), every residual set in the class \(\{x,z\}\) must meet
all three triangle edges, because the corresponding members of \(\mathcal K_x\)
must intersect. An edge covering a triangle is a pair of vertices in \(V\).
Thus all \(r_x\) residual sets are among the three pairs in \(V\).
Each pair occurs at most twice in \(\mathcal K_x\), since otherwise it would
be the core of a sunflower. It follows that
\[
r_x\le6\qquad(s_x\ge8).
\tag{D6}
\]

#### D.1.2 When \(k_x\ge9\)

The paper's universal I9/I10 classification identifies \(\mathcal K_x\) with
\(\mathcal P\) or one of its nine-member subfamilies. Relative to its member
\(R\setminus\{x\}\), the family \(\mathcal P\) has exactly two blocks
meeting the anchor at each individual point. Therefore
\[
p_{xy}\le2\quad\text{per ogni }y\ne x
\quad\text{se }s_x\ge8,\ k_x\ge9.
\tag{D7}
\]

If \(k_x=10\), all these values are 2 and all \(t_m\), \(m\ne x\),
are 1. To justify the count, every point of the design has degree 5:
besides the anchor, it belongs to two blocks meeting the anchor in two
points and to the two remaining blocks meeting it only at that point.

#### D.1.3 Forced identifications of exterior points

When \(t_m=1\), write the unique member of the corresponding class as
\[
T_m=(R\setminus\{m\})\cup\{z_m\},\qquad z_m\notin R.
\]

If \(x\) is large and \(t_y=1\), every residual edge in the class
\(\{x,y\}\) must contain \(z_y\). Indeed, in the link of \(x\), the
member \(T_y\setminus\{x\}\) must meet every member \(\{y\}\cup E\)
of that class, and the only possible point is \(z_y\). Hence
\[
s_x\ge8,\ t_y=1\ \Longrightarrow\ p_{xy}\le2.
\tag{D8}
\]

If \(x,y\) are both large, \(t_x=t_y=1\) and \(p_{xy}=2\), the two
distinct edges must contain both \(z_x\) and \(z_y\). Consequently
\[
z_x=z_y.
\tag{D9}
\]

There is also an opposite condition. If \(x\) is large and \(k_x\ge9\),
the points \(z_m\) with \(m\ne x\) and \(t_m=1\) must be **pairwise distinct**.
In the design \(\mathcal P\), two blocks meeting an anchor in two points
cannot have the same exterior point: otherwise, in the link of the common
point of their two anchor pairs, those blocks and the anchor would form a
triangle, whereas that link is \(C_5\). This property passes to
\(\mathcal P\) with one block removed.

The conflict between (D9) and this distinction of exterior points is the
essential obstruction.

### D.2 Two small structures

An intersecting triple family containing all triples on four points W has
no further members: a new member would have to use at least two points of W,
but that pair already has codegree 2. An intersecting family with more than
six triples has no degree-6 point, by the SF2 argument given in the introduction.

If an intersecting family of eight triples has a three-member singleton
class, it is \(\mathcal Q\): the six anchors of type uab have singleton
profile \((2,1,1)\) and three pair traces; the two of type uvd have profile
\((3,3,0)\) and one pair trace omitting the point of weight zero.
These are all the anchors. The profile \((2,2,2;1)\) is therefore
\(\mathcal P\) with two pair traces removed. Its three singleton classes
are complete stars on the same set of three exterior points, centred at the
exterior points of the complementary pairs.
This structure holds at every anchor of \(\mathcal P\): every pair has
codegree 2, and the three substitutions of the anchor have distinct exterior
points; intersection with the substitution of the complementary pair forces
the centre of each star.

### D.3 Margin with four large indices

**Lemma D3.** If all four indices are large, \(P+T\le12\).

We have \(P\le12\). Suppose \(P+T\ge13\), so \(T\ge1\).

**If \(T=4\)**, all weights are at most 2 and \(P\ge9\).
At least three pairs have weight 2; the graph of these pairs on four indices
has a component with at least three vertices. Three exterior points coincide.
The \(\mathcal K_x\) of the fourth index contains all triples on four points
and additional members, since \(r_x\ge P-6\ge3\): impossible.

**If \(T=3\)**, again all weights are at most 2, and \(P\ge10\).
On the three occupied indices, if the weight-2 graph is connected, their
three exterior points coincide and give the same obstruction in the link of
the unoccupied index. If it is disconnected, the total deficit from 12 is at
most 2: exactly two occupied pairs have weight 1 and all other pairs have
weight 2. The \(\mathcal K_x\) of the unoccupied index has size 10 and
requires three distinct exterior points; the remaining occupied weight-2
pair requires two of them to coincide.

**If \(T=2\)**, let \(a,b\) be occupied and \(c,d\) unoccupied;
\(P\ge11\). The five pairs incident to \(a\) or \(b\) have weight at
most 2. For \(P=12\), all \(r_x\) are 6, so all six weights are 2.
Then \(z_a=z_b\), but \(k_c=9\) requires them to be distinct.

For \(P=11\), even \(cd\) cannot have weight 3: if it did, writing
\(L\) for the sum of the four cross-pair weights, we would have
\(6+L=r_c+r_d\le12\) and \(11=p_{ab}+3+L\), with \(p_{ab}\le2\).
Thus \(p_{ab}=2,L=6,r_c=r_d=6,k_c=k_d=9\), which excludes weight 3.

Hence all weights are 2 except one of weight 1. If that pair is a cross
pair, the other unoccupied index has \(k=9\) and contradicts \(z_a=z_b\).
If it is \(cd\), the common point \(z_a=z_b=q\) belongs to six members
of \(\mathcal K_c\), which has eight: two pair traces and four singleton
members. This is excluded by the degree bound five for a point in an
intersecting family of size greater than six.

If the weight-1 pair is \(ab\), then \(\mathcal K_c,\mathcal K_d\) have
size 9 and \(z_a\ne z_b\). The residual set \(\{z_a,z_b\}\) occurs
in class \(ab\), since both points are required. The complete stars in the
two \(\mathcal P\) models also force it into classes \(ac,ad\).
The three quadruples have common core \(\{a,z_a,z_b\}\): a sunflower.

**If \(T=1\)**, necessarily \(P=12\). Denote the occupied index by
\(a\); its three incident weights are 2 and all \(r_x=6\). The weights
on the remaining triangle are also 2. For every \(x\ne a\),
\(\mathcal K_x\) has eight members and rooted profile \((2,2,2;1)\).
Section D.2 and the paper's universal I8 classification force the model
\(\mathcal P\) with two pair traces removed.

The shared classes of two residual sets identify the same exterior set of
three points in all three links, and the same centre for each shared pair.
The centre of class \(xa\) is always \(z_a\). The three pairs on the
triangle of the other indices would therefore have to be coloured with the
two remaining exterior points, using distinct colours at each vertex.
A triangle cannot be properly edge-coloured with two colours.
All cases are excluded. \(\square\)

### D.4 Margin with three large indices

**Lemma D4.** If there is exactly one small index, \(P+T\le14\).

Let v be the small index and G the set of the three large indices.
We have \(2P=\sum_{x\in G}(r_x+p_{xv})\le27\), hence P≤13.
Suppose \(P+T\ge15\). The remaining cases are T=2,3,4.

If \(T=2\), we need \(P=13\). An unoccupied large index has
\(r_x+p_{xv}\le8\): if \(r_x=6\), then \(k_x=9\) and
\(p_{xv}\le2\); otherwise use \(r_x\le5,p_{xv}\le3\).
Every other summand in the preceding sum is at most 9. To obtain 26 we need
exactly two occupied large indices \(a,b\), with summands 9, and the third
large index \(w\), with summand 8. In particular \(r_a=r_b=6\) and
\(p_{av}=p_{bv}=3\).

Now \(k_a=8\). By D.2 its three weights are \((3,3,0)\).
Since \(t_b=1\), we have \(p_{ab}\le2\); thus \(p_{ab}=0,p_{aw}=3\).
Likewise \(p_{bw}=3\). It follows that \(r_w=6,p_{wv}=0\),
contradicting the required summand 8.

If \(T=3\), each summand in the preceding sum is at most 8:
when \(r_x=6\), we have \(k_x\ge9,p_{xv}\le2\); when
\(r_x\le5\), the bound 3 suffices. Hence \(P\le12\);
since \(P+T\ge15\) is required, all summands are 8.
The possibilities are \((r_x,p_{xv})=(6,2)\) or \((5,3)\).
The latter is impossible: \(k_x\) is 8 or 9; size 9 excludes weight 3,
whereas at size 8, D.2 would force \(r_x=6\).

Thus all three large indices have \(r_x=6,k_x\ge9,p_{xv}=2\), and all
six pairs have weight 2. Among the three occupied indices, at least two,
\(a,b\), are large; \(p_{ab}=2\) forces \(z_a=z_b\).
The \(\mathcal K_x\) of the third large index has at least nine members
and requires them to be distinct: a contradiction.

If \(T=4\), all six weights are at most 2 and \(P\ge11\).
Thus all are 2, with at most one of weight 1. On the triangle of large
indices, at least two pairs have weight 2, and their three exterior points
coincide. Every large index has \(r_x\ge5,k_x\ge9\) and requires the
other two exterior points to be distinct: a contradiction.

All cases are excluded; Lemma D4 follows.

### D.5 The five margins

If q is the number of small indices,
\[
\begin{array}{c|ccccc}q&0&1&2&3&4\\\hline P+T\le&12&14&17&19&22.\end{array}
\]
The first two cases are Lemmas D3–D4.
For q=2, with large indices c,d and small indices a,b,
\(P=r_c+r_d-p_{cd}+p_{ab}\le15-p_{cd}\).
If P+T≥18, then T=3 requires P=15, \(p_{cd}=0\),
\(r_c=r_d=6\). But \(k_c\ge9\) forces the other two weights of c
to be at most 2, contradicting r=6. For T=4 the five weights incident to
large indices are at most 2 and the sixth is at most 3, so P≤13.
T≤2 does not suffice. Therefore P+T≤17.
For q=3 use P≤6+9=15; for q=4 use P≤18; T≤4 completes the proof.

## E. High points and rigidity of the design

A point is **high** if \(d(x)\ge19\), and low otherwise.
The universal SF3 bound20 and the paper's maximality/high-link decomposition
lemma give a high point two components
\(\mathcal P/\mathcal P_9\) on disjoint six-point supports,
and for every anchor containing it,
\[
(s_x,k_x)\in\{(9,10),(10,9),(10,10)\}.
\]
Every pair in each component is covered.

**E1. At most two high points in a quadruple.** Suppose R contains
three high points a,b,c. For each, \(k_x\ge9,r_x\le6\), so
\(T-t_x\ge2\). T≤1 is impossible; for T=2 all three would be
unoccupied, leaving only one index for two occupied traces.
Thus T=3 or 4. All weights are at most 2, because every pair meets a high point.
For T=3, two occupied high points a,b have distinct exterior points by the
model of the third, so \(p_{ab}\le1\) and \(r_a\le5\),
contradicting \(k_a=r_a+3\ge9\).
For T=4, all pairs among the three high points have weight at most 1,
using the model of the third; hence \(r_a\le4\), contradicting
\(k_a=r_a+4\ge9\). No assumption on \(\mu\) was used.

**E2. No exactly-one transversal.** If a subset X meets each block of
\(\mathcal P\) in exactly one point, then \(5|X|=10\) implies |X|=2.
That pair is contained in two blocks, a contradiction.

**E3. Confinement of a \(C_5\) star.** An intersecting triple family
containing the centre x added to the edges of \(C_5\) on V is supported
on \(\{x\}\cup V\). A member avoiding x must cover the cycle with three
points of V. A new edge in the link of x meeting V would raise a degree to
three; one avoiding V would form a three-edge matching with two cycle edges.
