# Universal pair/singleton and shared-extension lemmas

The statements below are local geometric arguments. Their high-link classification premise is the universal R16 classification and maximality proved in the paper.

## 2. Le tracce pair consumano anche la capacità delle singleton

Fissiamo y∈S. Un residuo con traccia pair ha forma {y,j}∪E, con E coppia esterna.
Nel caso C5 prendiamo tutti tali residui; nel caso P5 prendiamo alternativamente
quelli che non hanno j=a o quelli che non hanno j=b, dove {a,b} è l'unica
2-copertura del cammino.

Nella sottofamiglia scelta le coppie esterne E si incontrano a due a due. Se
sono disgiunte, un cono che contiene y e evita j,k produce un sunflower con
nucleo y; quando j=k si usa un cono attraverso quella coppia. Ogni residuo
singleton {y}∪H deve incontrare ogni E, usando un arco della stella che evita j.
Una stessa coppia E compare al massimo due volte, per il cap2 della tripla y∪E.

Siano b il numero dei residui pair della sottofamiglia e h=n_{y}. Le coppie
intersecanti hanno un punto comune oppure sono lati di un triangolo. Nel primo
caso il cap6 della coppia fra y e il centro dà b≤6; nel secondo si hanno tre
lati con molteplicità al massimo2, ancora b≤6. Nel triangolo ogni H contiene
almeno due vertici e la somma delle tre capacità di tripla dà b+h≤6.

Nel caso stella con almeno due foglie, al massimo due H evitano il centro;
le altre sono al massimo6−b. Con b=5 o6 ci sono almeno tre foglie e al massimo
una H evita il centro. Il caso di un solo lato si limita sommando le due
codegree. Ne segue la tabella NECESSARIA

|b|0|1|2|3|4|5|6|
|---|---:|---:|---:|---:|---:|---:|---:|
|h≤|10|10|8|5|4|2|1|

Il valore10 a b=0 usa il cap universale per una famiglia intersecante di triple.
La foresta usa invece20 a b=0, più largo e ancora valido. In particolare

    b≤6,                     5h+9b≤59.                         (P)

Questi limiti non richiedono interni vuoti, H27, μ42, cardinalità69 o
un numero massimo di punti esterni. Nel P5 vanno applicati alle due sottofamiglie
indicate, NON automaticamente alla famiglia pair intera.


## 5. Identità delle estensioni, non soltanto margini

Una traccia tripla U rappresenta U∪{z}, con z punto esterno effettivo.
Due occorrenze della stessa U hanno estensioni distinte, per semplicità.

Un cono prescritto xT può obbligare z ad appartenere a OGNI membro
di una categoria singleton o pair: altrimenti il cono, U∪{z} e quel membro
formano un sunflower. Analogamente può obbligare le estensioni di due occorrenze
triple a coincidere. Il checker trova questi testimoni tramite le tre
intersezioni letterali, non mediante una lista di regole nominali.

Se due estensioni forzano una singleton di almeno tre membri, coincidono:
due punti distinti insieme al punto singleton formerebbero una tripla di
codegree almeno3. Se forzano una categoria pair di almeno due membri, coincidono:
due punti distinti riempirebbero le sue due posizioni esterne e darebbero una
sola quadrupla, non due. Si prende la chiusura transitiva delle uguaglianze.

Per una classe C di occorrenze triple con lo stesso punto esterno z,
S_C e P_C sono gli INSIEMI delle categorie singleton e pair forzate. Allora

    d_F(z)≥|C|+Σ_(y∈S_C)n_y+Σ_(V∈P_C)n_V,
    d_F(y,z)≥#{U∈C:y∈U}+[y∈S_C]n_y+Σ_(V∈P_C,y∈V)n_V.

Le categorie hanno tracce di taglia3,1,2, quindi sono disgiunte. Una categoria
forzata da più occorrenze si conta una sola volta. Classi diverse non sono
presunte distinte: ulteriori coincidenze possono soltanto aumentare le capacità
richieste. Una duplicazione della stessa U nella stessa classe è impossibile;
si contraddice inoltre il cap18 sul grado esterno o il cap6 sulle coppie.

Se n_U=2, le due estensioni z,w sono distinte. Ogni categoria forzata
da U contiene entrambi; la loro somma non può superare d_F(z,w)≤6. Anche questo
limite è verificato sulle categorie reali, senza raddoppiare i contributi.


## 2. Un lemma sulle famiglie esterne

Siano Y={0,…,5}, U={x}∪Y e P la famiglia

```
012 015 023 034 045 124 134 135 235 245.
```

Supponiamo che F contenga il cono x+M, con M=P oppure P meno un blocco.
Per ogni y∈Y definiamo la **famiglia esterna completa**

\[
H_y=\{T:T\cap U=\varnothing,\ \{y\}\cup T\in F\}.
\]

**(a) Intersezione fra famiglie diverse.** Per y≠z esiste A∈M che
evita entrambi: in P ce ne sono 10−5−5+2=2, e una sola omissione ne
lascia almeno una. Se T∈H_y e S∈H_z fossero disgiunte, i membri
y+T, z+S e x+A sarebbero tre quadruple disgiunte. Dunque T∩S≠∅.

**(b) Una tripla può appartenere ad al più due H_y.** Tre occorrenze
su tre punti distinti y,z,w darebbero un sunflower a nucleo T.

**(c) Capacità se una famiglia esterna è P10 o P9.** Se H_y è
esattamente una P10 su un supporto V di sei punti, ogni membro delle
altre H_z è una trasversale di tre punti di questa P10. Non ci sono
trasversali di due punti, e le trasversali di tre punti sono esattamente
i dieci blocchi di P10. Quindi tutte le H_z sono contenute in questi
dieci blocchi, inclusa H_y; per (b),

\[
\sum_{z\in Y}|H_z|\le20. \tag{E10}
\]

Se H_y è esattamente P9, non vi sono ancora trasversali di due punti.
Le trasversali triple sono gli stessi dieci blocchi della sua estensione
P10 più il complemento del blocco omesso, in tutto undici. Quindi

\[
\sum_{z\in Y}|H_z|\le22. \tag{E9}
\]

Per controllare questi conteggi: una tripla S⊂V incontra tutti i membri
di M se e solo se V∖S non appartiene a M. P10 contiene precisamente
una tripla di ogni coppia complementare. Una trasversale con punti fuori
da V darebbe una trasversale di taglia al più due in V, impossibile.
Questo è un argomento sul supporto arbitrario, non un limite supposto.

## 3. Quando una singleton fornisce una famiglia esterna

Nelle ancore x+A, A∈M, le triple del link di y provenienti dal cono
contengono x e hanno supporto U∖{y}. I loro link grafici sono C5 o P5.

Se s_y è 9 o 10, la classificazione e l'isolamento P9/P10 del dossier
obbligano la parte vicina a evitare il suo supporto; gli eventuali blocchi
mancanti, essendo disgiunti dall'ancora, apparterrebbero alla singleton.
Poiché il cono della parte vicina copre U∖{y}, la singleton è interamente
esterna a U. Ogni altra tripla del link incontra l'ancora e quindi U:
questa singleton coincide **esattamente** con H_y.

Se s_y=8, per P8 lo stesso argomento fornisce otto triple esterne. Per
Q8 il nucleo di cinque punti è esterno, ma le sue due foglie possono
essere in U. Sono sempre esterne almeno le sei triple sul nucleo.
Pertanto il limite uniforme utilizzabile è

\[
|H_y|\ge\ell(s_y),\quad
\ell(10)=10,\ \ell(9)=9,\ \ell(8)=6,
\quad\ell(s)=0\text{ per }s\le7. \tag{L}
\]

Non si sostituisce sei con otto nel caso Q8 senza un ulteriore argomento.
Se d(y)≥17, E17/E18/C1 separano invece l'intero link in componenti su
supporti disgiunti; la componente che contiene x contiene il cono, e
l'altra è esterna. La singleton esterna resta quindi la stessa in tutte
le ancore centrali che contengono y.

