# Degree eighteen with an isolated P10 component

Work with a finite simple four-uniform family containing no three-sunflower, including empty core. Write N[R] for its closed member neighbourhood and mu for the minimum of |N[R]|. The applicable universal R16 classification, maximality, separate C5 obstruction and bootstrap/degree premises are specified in the acyclic [mathematical dependency map](../../../proof/DEPENDENCIES.md). H27 is applied only to intersecting families. The proof below gives the exact trace, point-identification, symmetry, coverage and pruning arguments.

## 1. Componenti, interni completi e modello necessario

Su S={0,…,5} fissiamo

```text
P10 = 012 015 023 034 045 124 134 135 235 245.
P9  =     015 023 034 045 124 134 135 235 245.
```

Nel modello locale l'etichetta del centro è6; il suo GRADO è18. Per P10 gli
altri otto membri del link evitano S, per P9 sono nove. Le loro altre
caratteristiche e il numero dei punti che usano non sono fissati.

Assegniamo l'intero interno I=F∩C(S,4), comprese le
assenze. I membri prescritti sono tutti i coni x∪T, T∈P10/P9, e tutti i Q∈I.
Per ogni ∅≠U⊆S, |U|≤3, poniamo

    n_U = #{Q∈F : x∉Q, Q∩S=U}.

Sono 41 conteggi: sei singleton, quindici coppie, venti triple. I membri interni
sono contabilizzati separatamente. Non compare n_vuoto né una variabile che
limiti il numero dei punti esterni. Per ciascuna coordinata vale il box

    0≤n_U≤c_|U|−#{Q prescritto: U⊆Q},     (c_1,c_2,c_3)=(18,6,2).

È un box necessario, talora largo. Se una quadrupla con traccia U forma un
sunflower con due membri prescritti, n_U=0. Il rifiuto dipende soltanto dalla
traccia, perché i due membri prescritti stanno in S∪{x}.

Scriviamo I_y=#{Q∈I:y∈Q}. Per un vicino C5 si ha

    d_F(y)−I_y≤15.

Togliere dal suo link le I_y triple interne lascia intatta la stella C5 del
centro e soltanto i cinque coni sui sei punti pertinenti. Sedici triple residue
contraddirebbero il risultato universale importato. Per un vicino P5, E17/E18
impongono I_y≥1 al grado17 e I_y≥4 al grado18. Non si identifica una I7 arbitraria
con P8 o Q8.

Se la singleton di un vicino in un'ancora centrale è almeno8,
B4 rende intersecante la parte complementare K_y. La separazione dei link alti
fornisce anche il controllo quando d_F(y)≥17. Il confinamento importato mantiene
i coni e gli interni prescritti nella medesima parte. K_y deve quindi contenerli
tutti e questi devono essere intersecanti. Un'aggiunta che evita x copre il
C5/P5 prescritto. Nel C5 ogni aggiunta è interna, quindi già assegnata. Nel P5
possono esserci al massimo due aggiunte esterne sulla sua unica copertura di
due punti; se |K_y|≥8 la classificazione la confina nuovamente ai sei punti.
Il programma ricostruisce le coperture e controlla anche la compatibilità con I.
Non si impone intersecanza a una parte che non ricade in tali ipotesi.

Le nove/dieci ancore centrali scelgono una riga completa delle quattordici
tracce, tutte alla soglia42. Le sette tracce che evitano x sono somme degli STESSI
n_U; il grado del medesimo punto è collegato agli STESSI selettori in tutte le
ancore. Gli interni assegnati forniscono contributi costanti. Una famiglia vera
produce selettori interi. Il rilassamento convesso può essere più largo, non è
richiesto che ogni sua soluzione sia realizzabile da una famiglia.

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

## 3. Tutti i dodici interni P10 nonvuoti sono refutati

Le 2^15 scelte interne, controllate con i coni, lasciano292 famiglie,
con distribuzione per taglia0,…,5 pari a1,15,75,135,60,6. I60 automorfismi P10
le dividono in13 orbite. Un enumeratore per augmentazione e uno per maschere
complete confrontano l'intera copertura, non soltanto il numero finale.

Per undici orbite nonvuote almeno un'ancora non ha alcuna riga: la
sua equazione di scelta è0=1. La sola eccezione è I={0123}:

    1.641 variabili; 422 uguaglianze; 12 disequazioni (P).

Un certificato usa soltanto le disequazioni b_0≤6, b_2≤6 e quattordici uguaglianze.
I suoi moltiplicatori interi hanno membro destro−37; il minimo del medesimo
membro sinistro su tutti i box è0. Dividendo tutti i moltiplicatori per37,
si legge **0≤−1**. L'affine 5h+9b≤59 è nel modello ma non serve a questa
particolare combinazione. Il certificato originale ha scala1000 e gap−37.

Una famiglia con interno nonvuoto può essere rinominata, insieme
a TUTTI i propri punti e membri, in una delle dodici orbite. Non viene imposta
simmetria al completamento. Nessuna può esistere: l'interno P10 è dunque vuoto.
Questo non esclude ancora la configurazione vuota, trattata di seguito.

## 4. Il dominio intero completo della P10 vuota

Ora i sei vicini hanno grado≤15. Per T={a,b,c}∈P10, R={x,a,b,c},
le tracce contenenti x sono fissate. La singleton del centro è8. Poniamo

    e_T=n_T,
    m_ij=Σ_(U⊇{i,j}) n_U,
    w_ij(T)=m_ij−n_T.

Si hanno d_F(y)=5+Σ_(U∋y)n_U. Per una tripla T della P10, n_T≤1 perché esiste
già il cono xT; per le dieci triple non prescritte, n_T≤2. Non sono dichiarate
assenti quelle triple.

Ogni ancora ammette97 righe complete, 970 in totale. Il raccordo dei
sei gradi produce263 profili etichettati, in18 orbite sotto Aut(P10). Le liste
complete vengono ricostruite dal checker e confrontate con il produttore.

Per ciascun profilo si sceglie una riga per ogni ancora,
accordando TUTTI i m_ij e le n_T già assegnate. Per le dieci triple non prescritte
si visitano tutti gli interi da0 alla capacità residua delle loro tre coppie,
al più2. Completate le triple, le altre coordinate sono determinate:

    n_ij=m_ij−Σ_(U⊇ij, |U|=3)n_U,
    n_y=d_F(y)−5−Σ_(j≠y)m_yj+Σ_(U∋y, |U|=3)n_U.               (T)

Un valore negativo è impossibile. Ogni famiglia effettiva produce una di
queste scelte. Non si fissa il numero dei residui a traccia vuota.

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

## 6. Un I8 limita a36 la somma delle sei famiglie esterne

Scriviamo H_y={H:{y}∪H∈F,
H∩(S∪{x})=∅}. Ogni H_y è intersecante: un cono che passa per y renderebbe
sunflower due parti esterne disgiunte. Le famiglie H_y,H_z sono cross-intersecanti:
un blocco P10/P9 evita y,z, quindi due loro parti esterne disgiunte produrrebbero
con il cono tre quadruple disgiunte. Una stessa tripla esterna può appartenere
ad al massimo due categorie, per il cap di codegree2.

Se una H_y ha almeno8 membri, ne scegliamo otto. Sono P8 oppure Q8. Ogni tripla
di tutte le H_z è una trasversale di questo I8. Nel supporto dell'I8 ci sono
12 trasversali triple per P8 e11 per Q8. Fuori da quel supporto una trasversale
tripla deve usare una 2-copertura interna; non esistono 1-coperture e la
2-copertura è al massimo una. Ogni H_z contiene al massimo due triple che
estendono quella coppia, per il cap2 della tripla formata dalla coppia e z.
Ne segue, uniformemente,

    Σ_y |H_y|≤2·12+6·2=36.                                    (H8)

Per P8 priva di 2-copertura il limite è24; per Q8 è34. Si usa il più largo36.
Analogamente, una H_y di taglia≥9 dà il limite22 e una di taglia10 il limite20,
per le undici/dieci trasversali triple di P9/P10 e l'assenza di 2-coperture.

Il checker esamina tutte le45 coppie di blocchi omessi P10 e il Q8:
12 trasversali triple in ogni P8,11 nel Q8; al massimo una2-copertura. Questo
censimento piccolo si combina con la classificazione completa I8 importata.
Non si sta classificando una I8 nuova su un supporto arbitrariamente scelto.

Il profilo d(y)=13 per tutti i sei vicini ha un solo raccordo
dei margini: tutti m_ij=0, quindi tutte le pair/triple sono assenti e n_y=8
per ogni y. Richiede48 occorrenze esterne, mentre(H8) ne permette al massimo36:

    48≤36,

impossibile. Non serve H27 per questo passo. I profili diversi sono coperti
dagli altri rifiuti della foresta.

## 7. Certificato a prefissi: copertura completa della P10 vuota

Per un prefisso di assegnazione delle triple, ogni tripla libera ha
capacità al più min(2, capacità delle sue tre coppie). Sottrarre tutte queste
capacità dà un limite INFERIORE per ciascuna n_ij; la formula(T), con le triple
ancora libere nonnegative, dà un limite inferiore per n_y. Aggiungerne tutte le
capacità dà anche un limite superiore per n_y. Tali stime possono essere larghe
ma valgono per ogni completamento.

Le regole dei §§2,5,6 sono monotone rispetto ai limiti inferiori impiegati:
un sovraccarico, un'uguaglianza forzata o una duplicazione non si riparano
aggiungendo membri. La tabella pair/singleton è non crescente. Il checker
ricalcola il dominio, i figli e il motivo di ogni foglia. Rifiuta byte mancanti,
aggiunti, ragioni false e foglie OPEN. Un ramo dell'accordo iniziale delle
ancore può terminare senza byte soltanto quando nessuna riga accorda i margini.

Il certificato completo ha:

|Oggetto|Conteggio|
|---|---:|
|Profili canonici / etichettati|18 / 263|
|Righe locali complete|970|
|Nodi di raccordo delle ancore|1.370.900|
|Pattern di margini|620.591|
|Nodi di prefisso|4.024.631|
|Foglie di refutazione|2.099.936|
|Foglie aperte|0|

|Ragione della foglia|Numero|
|---|---:|
|Limite pair/singleton|390.028|
|Coppia esterna di due estensioni sovraccaricata|71.331|
|Quadrupla duplicata|531|
|Punto esterno di grado>18|926.924|
|Coppia di codegree>6|711.121|
|Somma delle famiglie esterne, profilo tutti13|1|

Una famiglia ipotetica produce un interno. Se nonvuoto, ricade
in una delle dodici refutazioni del §3. Se vuoto, produce un profilo e un
percorso della foresta; la sua foglia viola una condizione necessaria. Questo
è il ponte finito/generale: non un'estensione da un campione o da uno status
numerico. La configurazione P10 al centro18 è impossibile. Con E18 e H27,
le tre radici P10 di F69 sono quindi chiuse. □

## 8. R99: riduzione degli interni e due strumenti ulteriori

### 8.1 Settantatré tipi esclusi, sei esplicitamente aperti

Il medesimo modello a μ42/cap18, ora su P9 e con nove membri esterni
nel link del centro, tratta tutti i373 interni in79 orbite. Con(P) vengono
refutati73 tipi:62 hanno un'ancora senza righe,11 richiedono combinazioni
aritmetiche. Restano:

|ID|Interno rappresentativo|Orbita etichettata|
|---|---|---:|
|P9_000|vuoto|1|
|P9_001|{0123}|3|
|P9_002|{0134}|3|
|P9_003|{0135}|6|
|P9_004|{0345}|3|
|P9_019|{0135,1234}|3|

Sono19 interni etichettati per componente. Il prodotto dei due
gruppi Aut(P9) e lo scambio delle componenti dividono le361 coppie in21 orbite,
una per coppia non ordinata dei sei tipi. La copertura è ricostruita in
`check_catalogues.py`. TUTTE le21 sono OPEN; gli interni NON sono dichiarati
vuoti. Le 85 refutazioni lineari della consegna sono12 P10 più73 P9, tutte
incompatibilità, di cui73 immediate e12 nontriviali.

### 8.2 H27 sulle categorie pure, non soltanto sui coni

Tutte le quadruple che incontrano S in un solo punto formano
insieme una famiglia intersecante. Con lo stesso punto condividono quel punto;
con punti distinti y,z, due membri disgiunti insieme a un cono che evita y,z
formerebbero un sunflower vuoto. Pertanto

    Σ_y n_y≤27.                                                (H27-pool)

Il lemma non richiede interni vuoti. H27-pool è disponibile per le prossime
ricerche R99, ma NON viene usato nella foresta P10 del §7. La prova di quella
foresta usa il diverso limite(H8), senza H27.

### 8.3 Due posizioni esterne non possono contenere tre punti distinti

Un residuo con traccia pair V⊂S ha soltanto due punti
fuori S. Se tre occorrenze triple forzano tutte la categoria V, le loro
estensioni devono assumere al massimo due valori distinti. Se ogni possibile
fusione di due valori viola già un cap di grado/codegree o forza un duplicato,
la categoria V non può essere presente. Non si può inferire la distinzione
semplicemente dal fatto che due classi di uguaglianza non siano ancora unite:
la loro fusione deve essere realmente esclusa.

`controls/R99_TWO_SLOT.json`
fornisce un vettore intero delle41 tracce con gradi(14,15,15,15,15,15), compatibile
con tutte le nove ancore e non respinto dalle vecchie regole unarie. La categoria
01 ha taglia1 e deve contenere le estensioni delle triple012,023,124. Le tre
possibili fusioni a coppie forzano gradi esterni almeno19,20,21, tutti>18.
Servirebbero quindi tre punti distinti nelle due posizioni esterne della
quadrupla. Il checker ricostruisce esattamente questa contraddizione.

È esclusa questa specifica proiezione, NON tutta la P9 né alcuna
delle21 coppie globali. La conclusione riguarda soltanto la proiezione specificata; la copertura completa R99 è stabilita nel blocco D18_R99.

## 9. Certificati aritmetici, controlli e limite della verifica

Per Az≤b, Ez=f e l≤z≤u, un certificato contiene interi y≥0 ed η liberi.
Si calcolano q=Aᵀy+Eᵀη, H=y·b+η·f, L=Σ_j min(l_jq_j,u_jq_j). Se H−L<0,
qualunque soluzione imporrebbe L≤q·z≤H<L. Tutti i box sono pagati esattamente.
La scala positiva normalizza i moltiplicatori; nessuna tolleranza numerica
interviene nella decisione. Il solver serve soltanto a cercare moltiplicatori.

Il produttore `projection.py` e l'auditor `audit_projection.py` hanno
ordini di generazione e rappresentazioni diversi. Il confronto tratta tutte
le righe, i coefficienti, i box e le colonne di ogni sistema. Il checker Python
della foresta non importa il C++: ricostruisce le intersezioni con insiemi e
le classi di uguaglianza come componenti di un grafo. L'opzione `--cpp` rigenera
le18 prove e confronta ciascun byte decompresso. Normalmente e con−O i controlli
usano eccezioni esplicite, non assert disattivabili.

I controcontrolli comprendono tutte le24.804 terne del testimone54,
due famiglie effettive di25 e26 quadruple con16 membri nelle categorie pure
(2.300 e2.600 terne), il conteggio delle trasversali P8/Q8, l'esempio a due
posizioni esterne e mutazioni di certificati, domini e stati. Nessuno di tali
esempi viene presentato come una candidata nel dominio μ42.

Le ricevute della verifica completa sono prodotte dall’unico ingresso `scripts/verify.py` nella radice del companion, secondo `SUITE_PLAN.json`. Per questo ramo i controlli `check_catalogues`, `check_linear`, `check_forest`, `check_geometry` e `check_scope` verificano le coperture292/13 e373/79, gli85 certificati esatti, tutti i18 profili di foresta e2099936 foglie chiuse, la geometria e le mutazioni dichiarate. Le altre premesse finite sono controllate nei loro blocchi separati della suite completa; H27 resta un import matematico esplicito. Non vengono lette ZIP baseline o eseguiti produttori C++.

Un esaurimento parziale non copre profili mancanti: il controllo della foresta richiede tutti i profili, tutti i figli e tutte le foglie, con zero foglie aperte. La suite non enumera famiglie effettive F69; verifica il dominio necessario e i certificati della refutazione. I controcontrolli limitati non sono una prova che il software sia privo di ogni difetto.
