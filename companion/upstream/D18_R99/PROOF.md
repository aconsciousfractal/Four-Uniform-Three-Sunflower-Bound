# Degree eighteen with two P9 components

Lavoriamo con una famiglia finita semplice di quadruple senza tre-sunflower, compreso il nucleo vuoto. Scriviamo N[R] per il vicinato chiuso di un membro e mu per il minimo di |N[R]|. Le premesse sono la classificazione universale R16 e la sua massimalità per i link alti, l'ostruzione C5 separata e le precedenti riduzioni di bootstrap e di grado, nell'ordine aciclico descritto dal paper. H27 si applica soltanto a famiglie intersecanti. Le premesse e i rispettivi testi sono indicati nella [mappa delle dipendenze](../../../proof/DEPENDENCIES.md), alla voce «Ordinary premises and source replacements».

## 1. Le due componenti e i conteggi condivisi

Fissiamo Y={0,…,5}, Z={6,…,11}, x=22. L'etichetta22 non dichiara
che esistano soltanto23 punti. Siano

    P10 = 012 015 023 034 045 124 134 135 235 245,
    P9 = P10 senza012.

Il link contiene la P9 suY e la sua traslazione suZ:18 coni x∪T. Scriviamo
S=Y∪Z. Nell'argomento per assurdo |F|≥69, il numero r dei residui è almeno51.
Tutte le refutazioni di maggiorazione sono confrontate con51; non richiedono
l'equazione r=51.

### 1.1 Perché si possono dimenticare le etichette esterne

Per ogni T⊆S, |T|≤4, introduciamo

    z_T = #{Q∈F : x∉Q, Q∩S=T}.

Ci sono Σ_(j=0)^4 C(12,j)=794 tipi di traccia. Non è una scelta di794
quadruple rappresentative: ciascun z_T CONTA tutte le sue estensioni.
Quando |T|=1,2,3, il numero è limitato rispettivamente dalla capacità18,6,2,
meno i coni già contenentiT. Se |T|=4, semplicità dà z_T≤1.
Le assenze certificate o un sunflower con due membri prescritti danno z_T=0.

Il solo tipo che non avrebbe un box universale immediato è T=∅. Ma in OGNI
ramo dei50 certificati è fissata una coppia di membri disgiunti, interamente
sul core insieme a x. Un residuo con traccia vuota sarebbe disgiunto da
entrambi, dunque vietato. Quindi z_∅=0.

Per un interno presente, prendiamo quell'interno e un cono dell'altra P9.
Per una marcatura con quattro punti diS, una componente contiene al massimo
due punti marcati e la P9 ha un blocco che li evita. Per una marcatura con
traccia mista di tre punti e un esterno a, prendiamo un cono che evita la
marcatura; il core viene ampliato includendo a. Il verificatore ricostruisce
una coppia prescritta disgiunta in tutti i50 casi.

Per quest'ultimo stadio rinominiamo il punto esterno marcato come12.
Il core C=S∪{12} ha13 punti, e si usano Σ_(j=0)^4 C(13,j)=1.093 conteggi di
traccia. Gli ALTRI punti esterni rimangono arbitrari. Il punto12 è reale,
appartiene al marcatore e ha un unico selettore di grado4,…,18.

I box nonvuoti sono esattamente0 oppure i cap universali appena descritti.
Il modello verificato omette le disuguaglianze che maggiorano le incidenze
mediante il NUMERO di etichette esterne:79 righe per i modelli a core12 e92
per quelli a core13. Le combinazioni certificate non usano quelle righe:
assegnare loro moltiplicatore zero conserva esattamente lo stesso valore
aritmetico. Il modello usa i box universali e z_∅=0, senza un limite al
numero dei punti esterni.

### 1.2 Legare le due P9 agli stessi z_T

Ogni componente conserva il modello locale precedente:41 conteggi
n_U per ∅≠U⊆Y (oZ), |U|≤3, sei gradi condivisi e una configurazione completa
per ognuna delle nove ancore. Per ogni U imponiamo

    n_U = Σ_(T : T∩Y=U) z_T,

oppure la corrispondente equazione suZ. Il centro locale di etichetta6 delle routine viene trasportato nel centro
globale22: NON è il punto6 della seconda P9. Si legano soltanto le41 tracce
sui sei punti della componente e i relativi gradi. I membri interni con quattro punti
sono conteggiati separatamente nelle righe della componente e sono fra le
z_T globali. Non si sottraggono due volte. Le due componenti non possono più
scegliere indipendentemente estensioni incompatibili della stessa quadrupla.

Si conservano i cap18/6/2 sui sottoinsiemi del core, H27 sui membri prescritti
o marcati e H27-pool su ciascuna componente:

    Σ_(T:|T∩Y|=1) z_T≤27,       Σ_(T:|T∩Z|=1) z_T≤27.

Per il pool, due membri di categorie distinte disgiunti, con un cono che
evita i loro due punti nella componente, formerebbero un sunflower vuoto.
Quindi l'unione delle categorie è intersecante. Non si presume la stessa
proprietà per altri insiemi di categorie senza prova.

Una famiglia effettiva produce interi z_T e
selettori0/1. Il modello ammette anche valori frazionari; questo allarga il
dominio e non elimina una famiglia. Non si richiede il converso. Le ancore
centrali usano le stesse coordinate di grado attraverso tutti i membri.
Nessun punto esterno è identificato con un altro per presumere simmetria.

## 2. Venti certificati escludono tutte le coppie interne nonvuote

La ricostruzione dei373 interni P9 in79 orbite e il replay dei73
certificati ereditati lasciano esattamente:

    I0=∅, I1={0123}, I2={0134}, I3={0135}, I4={0345}, I5={0135,1234}.

Le dimensioni delle sei orbite sono1,3,3,6,3,3:19 interni etichettati.
Aut(P9) ha6 elementi. Il prodotto dei due gruppi e lo scambio delle componenti
coprono361 coppie etichettate in21 orbite.

Si assegnano tutte le presenze e assenze interne su ENTRAMBI i lati.
Si conservano il completamento C5 d(y)−I_y≤15, il distinto completamento P5
(I_y≥1 a17 e≥4 a18) e il confinamento dei complementi intersecanti quando
s_y≥8 o quando la decomposizione del link alto lo giustifica. Gli interni
restano possibili fino alla loro assegnazione nel singolo caso.

Tutte le20 coppie nonvuote sono escluse:19 maggiorazioni strettamente
inferiori a51 e un'incompatibilità. La maggiore delle MAGGIORAZIONI CERTIFICATE
è253/5=50,6. La coppia I5/I5 ha gap−41/2000. I valori sono quelli dopo la
correzione esatta dei box, non gli obiettivi in virgola mobile del solver.
I venti casi di coppie interne sono i record con `problem.stage` uguale a
`interior_pair` in [data/CASES.json](data/CASES.json). Lo stesso catalogo contiene
i22 casi misti da quattro punti e gli otto casi misti da tre punti; ogni record
indica il proprio certificato esatto. [scripts/check_catalogues.py](scripts/check_catalogues.py)
controlla la copertura completa delle orbite; [scripts/check_models.py](scripts/check_models.py)
ricostruisce tutti i50 modelli e verifica le disuguaglianze esatte dei certificati.

Ogni famiglia con almeno un interno si rinomina in uno dei20
casi coperti. Non si impone che sia simmetrica. Pertanto, nell'ipotetico caso
r≥51, entrambi gli interni sono vuoti. I punti C5 hanno grado≤15; quelli P5≤16.
Non si eliminano i punti17 o18 esterni alle due componenti.

## 3. Prima tutte le quadruple sul core, poi le tracce miste di tre punti

### 3.1 Ventidue marcature sul core12

Con gli interni vuoti restano465 quadruple diS distribuite su entrambe
le componenti. Formano22 orbite. Ogni marcatore M viene imposto con z_M=1,
si eliminano soltanto le tracce che danno un sunflower con M e un cono e si
aggiunge H27 sull'ancora M. Non viene aggiunta una scelta arbitraria delle
altre quadruple.

I22 certificati maggiorano r strettamente sotto51. Il massimo accettato è
2537/50=50,74. Le orbite disgiunte coprono tutte le465 quadruple; assieme ai30
interni già esclusi, nessun residuo può stare interamente inS.

### 3.2 Otto marcature con tre punti misti e un esterno

Soltanto DOPO il §3.1 si pongono assenti tutte le tracce di quattro
punti diS. Per un marcatore misto di tre punti si distingue il suo quarto
punto12 e si usano i1.093 conteggi sul core ampliato. Il marcatore è un membro
effettivo, la sua variabile è1, il suo punto12 ha un solo grado globale.
Non è sufficiente marcare soltanto una numerosità della tripla: l'identità
del quarto punto è conservata in ogni intersezione e in ogni capacità.

Gli otto marcatori sono

    016·12, 036·12, 046·12, 0·9·10·12,
    019·12, 039·12, 049·12, 3·4·9·12.

La notazione con punti separa le etichette a due cifre; i file usano liste
esplicite. Le dimensioni sul precedente universo di dieci esterni sono
180,360,180,180,180,360,180,180, in totale1.800. Per esterni arbitrari la stessa
copertura segue rinominando il quarto punto del marcatore come12.

Tutti gli otto sistemi danno un limite esatto sotto51; il maggiore è
2011/40=50,275. NON occorre enumerare le14 tracce di un'ulteriore ancora
marcata: le18 ancore centrali, collegate al punto esterno effettivo, bastano.

Ogni residuo ha adesso al massimo due punti inS, oppure tre
punti TUTTI nella stessa P9. Non si dichiarano assenti le triple pure.
L'ordine dei due stadi è essenziale: le refutazioni di §3.2 usano quelle di§3.1.

## 4. La copertura con eccezioni esclude le coppie miste

Supponiamo presente un residuo
M={y,z,a,b}, con y∈Y,z∈Z,a,b esterni. Un altro residuo Q deve contenere la
coppia{y,z}, oppurea, oppureb, salvo al massimo due estensioni eccezionali
per ciascuno dei due punti marcati che sia di tipoP5.

Se Q evitaa,b e non contiene entrambi y,z, la sua intersezione conM è vuota
o singleton. Nel caso vuoto, una componente contiene al massimo un punto
diQ (anche quandoQ contiene tre punti puri), e ha un blocco che evita quel
punto e il punto marcato. Il cono eM,Q sono tre membri disgiunti.

Se l'intersezione è{y}, cerchiamo un blocco attraversoy evitando gli altri
punti diQ nella componente. L'unica possibile eccezione è una tripla pura
yuv in cui{u,v} copre l'intera stellaP5. Un C5 non ha una tale copertura di
due punti; il P5 ne ha esattamente una. Nella P9 che omette012, le triple
sono035,145,234, rispettivamente pery=0,1,2. Ciascuna ammette al massimo due
estensioni, per la codegree della tripla. Il caso{z} è simmetrico.

Le tre categorie principali hanno taglia≤6,18,18. M appartiene a tutte e
tre: si sottraggono almeno due copie. Con al massimo quattro eccezioni:

    r≤6+18+18−2+4=44.

Questo contraddice r≥51. Nessun residuo ha esattamente un punto
per componente e due esterni. Il termine+4 NON è eliminato per comodità.
Il checker tratta15.696 tracce della radiceP9⊔P9 e conserva tutte le
36 eccezioni canonicheP5. La prova generale dipende dalle tracce, non da un
limite al numero delle etichette esterne.

## 5. Le triple complementari: il risparmio decisivo di quattro unità

### 5.1 Non basta sommare le capacità separate

Una P9 su sei punti ha11 trasversali triple. Nove sono i suoi
blocchi prescritti; le due ulteriori sono precisamente012 e345. Sono
complementari. Si può verificare sulle20 triple del supporto; una dimostrazione
è che P10 contiene un elemento di ogni coppia di triple complementari e,
rimuovendo012, si aggiunge come trasversale soltanto il suo complemento345.
Il blocco012 rimane anch'esso trasversale perchéP10 era intersecante.

Una tripla prescritta ha già il cono attraverso x, dunque al massimo UNA
estensione residua. Ciascuna delle due eccezioni ha separatamente capacità2.
Il conto ingenuo permetterebbe9+2+2=13 per lato, totale26: NON basta contro
il deficit necessario24. Non viene presentato il falso limite18.

### 5.2 Capacità congiunta delle due eccezioni

Siano U=012,V=345 e

    A={a esterno : U∪{a}∈F},   B={b esterno : V∪{b}∈F}.

Dopo il §3 tutti gli esterni di questi residui stanno fuoriS∪{x}: un quarto
punto dell'altra componente darebbe una quadrupla interamente inS, già esclusa.
Se esistonoa∈A,b∈B cona≠b, U∪{a} eV∪{b} sono disgiunti. Un qualsiasi cono
sull'ALTRA P9 è disgiunto da entrambi. Sono tre membri distinti disgiunti:
un sunflower vuoto.

Quindi, se A eB sono entrambi nonvuoti, tutti i loro elementi devono essere
lo stesso punto. Semplicità impone |A|=|B|=1. Se uno dei due è vuoto,
l'altro ha taglia≤2 per il cap sulla codegree della tripla. In ogni caso

    |A|+|B|≤2.                                             (COMP)

La prova è identica sull'altra componente. Il limite2 è raggiunto dai
controlli positivi locali: uno stesso esterno per le due triple, oppure
due esterni di una sola tripla. Non se ne deduce che il deficit globale22
sia raggiungibile.

### 5.3 Deficit≤22 e contraddizione488≤486

Per un residuoQ, siaκ(Q) il numero dei18 coni disgiunti daQ.
Dopo le esclusioni sono possibili solo: una coppia nella stessa componente
più due esterni; un punto inS più tre esterni; quattro esterni; oppure una
tripla pura più un esterno.

Una coppia nella stessa P9 incontra al massimo otto dei suoi nove blocchi,
quindiκ≥10. Un singolo punto incontra al massimo cinque coni, quindiκ≥13.
Un residuo tutto esterno haκ=18. La tripla pura haκ=9 precisamente quando
è una delle11 trasversali della relativa P9; altrimentiκ≥10.

Per le nove trasversali prescritte, le estensioni residue sono al massimo9;
per le due eccezioni, (COMP) dà un totale≤2. Ciascuna componente contribuisce
al deficit al massimo11. Dunque

    D=Σ_(Q residuo) max(0,10−κ(Q))≤22.

Da r≥51 segue

    Σ_Q κ(Q)≥10r−22≥488.

H27, applicata separatamente ai membri disgiunti da ciascuno dei18 coni, dà
invece

    Σ_Q κ(Q)≤18·27=486.

La contraddizione è488≤486. R99 è esclusa e il teorema è dimostrato.

`data/TERMINAL.json` è un certificato intero piccolo: si sommano le18
righeH27, le18 capacità residue1 delle triple prescritte e le due capacità2
congiunte delle coppie complementari. Ogni colonna terminale riceve coefficiente
almeno10 e il membro destro è486+18+4=508. Quindi10r≤508, impossibile perr≥51.
Nel controllo su23 etichette sono classificate tutte le7.315
quadruple in30 interne,465 miste da4,1.800 miste da3,1.620 miste da2 e3.400
terminali. Il loro istogrammaκ è:

|κ|9|10|11|13|14|18|
|---|---:|---:|---:|---:|---:|---:|
|Colonne|220|450|1.080|720|720|210|

Questo censimento corrobora il conto; il lemma e la prova generale non dipendono
da dieci esterni. Le3.400 colonne non sono una famiglia simultaneamente realizzata.

## 6. Certificazione esatta, coperture e indipendenza algoritmica

Ogni sistema è Az≤b,Ez=f,l≤z≤u, con interi. I certificati hanno
moltiplicatori interi y≥0,η liberi e scalat>0. Posto q=Aᵀy+Eᵀη,H=y·b+η·f,
per incompatibilità si verifica H−Σ_j min(l_jq_j,u_jq_j)<0. Per maggiorare
c·z si pone r=tc−q e si verifica

    H+Σ_j max(l_jr_j,u_jr_j)<51t.

Ogni box è pagato: nessuna tolleranza numerica decide un rifiuto. Il solver
serve soltanto a cercare i moltiplicatori. Le disuguaglianze di§5 non richiedono
un solver. Ogni punto e ogni membro marcato rimangono effettivi; la simmetria
rinomina l'intera famiglia e non ne impone l'invarianza.

I50 certificati sono20 interni,22 per tracce miste di quattro punti,
otto per tracce miste di tre. Sono49 maggiorazioni e un'incompatibilità.
Il sistema maggiore ha10.262 variabili. Le due ricostruzioni confrontano
coefficienti, RHS, box, obiettivi e tipi di traccia integralmente. L'auditor
locale usa il predicato a partizioni e l'ordine t-prima-di-p; il produttore
usa l'altro predicato e l'ordine p-prima-di-t.

Sono verificati anche i73 certificatiP9 ereditati e la copertura373/79.
I73 più50 danno123 certificati aritmetici controllati per modalità. I test
negativi modificano dieci oggetti per ciascuno dei50 certificati, quattro
coperture, quattro dati del conto terminale e sei controlli di ambito:
514 alterazioni respinte per modalità. Sono controlli negativi LIMITATI,
non una prova di assenza di ogni bug.

I checker `check_catalogues`, `check_models`, `check_geometry`, `check_next_domain`
e `check_scope`, elencati nella [mappa delle dipendenze](../../../proof/DEPENDENCIES.md)
alla voce «D18_R99: Degree eighteen with two P9 components», verificano i73
certificati P9 selezionati e la copertura373/79, i50 sistemi, il conto terminale
con capacità congiunta2, il dominio successivo17/42 e i controcontrolli.
P10, C5, R16 e bootstrap42 sono blocchi separati; H27 resta un risultato
matematico importato, non dimostrato dall'esecuzione dei checker.
