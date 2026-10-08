# Complete closed-neighbourhood45 exclusion

Read [CURRENT_PREMISES.md](CURRENT_PREMISES.md) for the precise premises and their locations. The proof below gives the local reduction, symmetry, complete domain and pruning arguments.

## 1. Tutte le ancore45 e i loro nuclei completi

Una riga r=(p,t,s) ha sei tracce esatte pair p_ij, quattro triple t_i
che omettono il punto i dell'ancora, e quattro singleton s_i. Poniamo

    k_i=1+Σ_(j≠i)p_ij+Σ_h t_h−t_i,
    d_i=k_i+s_i,
    |N[R]|=1+Σp+Σt+Σs.

`check_cores.py` ricostruisce l'intero dominio sia con `local43.py`
sia con `audit43.py`, chiamati esplicitamente con μ=42,r10=r9=7,cap16. Sono
24.002 righe con gradi ordinati; espandendo le permutazioni si hanno147.619 righe
orientate. Le157 righe di N45 formano36 orbite sotto le24 permutazioni dell'ancora.
Si rinomina l'INTERA famiglia; non si assume un completamento simmetrico.

Per R={0,1,2,3}, C(R) contiene tutti e soltanto i membri con |Q∩R|≥2.
La sua taglia è1+Σp+Σt. Le singleton e i membri disgiunti da R non vi appartengono.

Le parti esterne di una categoria pair sono coppie distinte e
intersecanti. Con uno,due,tre membri esse sono rispettivamente un arco, un cammino
di due archi, un triangolo. Una stella di tre archi darebbe un nucleo triplo.
Ogni traccia tripla ha un solo punto esterno. I punti esterni delle categorie
possono coincidere: tutte le identificazioni sono enumerate.

Se s_i≥8, B4 rende intersecante il complemento K_i nel link del punto i. Due
membri di C(R) non possono quindi incontrarsi esattamente in{i}. Questo divieto
si applica soltanto alle coordinate grandi, non a quelle con singleton7.

### 1.1 Generazione senza un cap artificiale sul supporto

Le categorie vengono aggiunte una per volta. Tutte le
iniezioni dei loro due o tre vertici esterni sui vertici già presenti e su vertici
nuovi sono provate. Le nuove etichette si normalizzano nell'ordine di prima
comparsa. Una famiglia reale determina una delle scelte. Le sole potature sono
quadrupla duplicata, sunflower letterale o violazione di B4.

La canonicalizzazione riguarda SOLO i punti esterni; R rimane fissata punto per
punto. Il nucleo diventa un grafo sui punti esterni: ogni arco ha come colore
l'insieme delle categorie pair che lo usano; i vertici registrano le categorie
triple. Si canonizzano separatamente le componenti connesse. All'interno di una
componente, la raffinazione dei colori usa invarianti; vengono provate tutte le
permutazioni residue delle classi. Le componenti vengono ordinate per la loro
rappresentazione canonica. Un isomorfismo conserva questi invarianti e manda
componenti in componenti, quindi la normalizzazione non perde identificazioni.

Il secondo ordine di generazione sceglie prima sottoinsiemi di vertici e poi
le loro disposizioni, con un diverso ordinamento delle categorie dove rilevante.
Le due procedure condividono questa canonicalizzazione esatta: non sono due
implementazioni totalmente indipendenti di ogni dipendenza.

Tutte le liste finali coincidono. Venti delle36 righe non ammettono un
nucleo. Le altre sedici producono2.335 record; il vecchio profilo35, prima parziale,
è ora esaurito con2.210 record. I supporti effettivamente comparsi sono:

|Punti del nucleo|7|8|9|10|11|12|13|
|---|---:|---:|---:|---:|---:|---:|---:|
|Record|3|4|162|1.063|737|319|47|

Non sono famiglie globali né classi d'isomorfismo globali. Le singleton possono
ancora usare punti fuori dal nucleo, senza un limite prescelto. I record dei
profili0–34 coincidono, dopo normalizzazione, con le liste storiche; il replay
ricostruisce comunque TUTTI i36, non assume completi i vecchi log.

## 2. Cambiare ancora esclude2.330 nuclei

Sia V=supp C(R). Un membro aggiuntivo Q ha traccia U=Q∩V con |U|≤4 e
|U∩R|≤1, perché C(R) è completo. Se per due membri A,B del nucleo

    U∩A=U∩B=A∩B,

ogni estensione di U è vietata. Questo test non dipende dalle etichette esterne.
Altrimenti il conteggio z_U ha il box necessario

    0≤z_U≤c_|U|−#{A∈C(R):U⊆A},    (c1,c2,c3,c4)=(16,6,2,1).

La traccia vuota non contribuisce ad alcuna ancora del nucleo ed è inizialmente
omessa, non limitata arbitrariamente.

Per un membro A effettivo del nucleo, il minimo di ogni traccia su A è quello già
prescritto. Il massimo aggiunge TUTTI i box compatibili, anche se non simultaneamente
realizzabili: è una maggiorazione sicura. I gradi dei punti originali di R sono
fissati dalla riga; gli altri hanno grado almeno8 e almeno il loro grado nel nucleo.
Ogni loro riga deve appartenere all'intero dominio orientato μ42, compreso N45.

Per2.330 record esiste un'ancora senza alcuna riga possibile. Il checker
ricostruisce, con insiemi, tutte le tracce ammesse, i14 intervalli e il dominio.
`data/ANCHOR_SCREEN.json` salva un testimone per ogni record, non un semplice stato.
Restano cinque nuclei: due nella riga5 e tre nella riga8.

## 3. Cinque sistemi condivisi con refutazioni intere

Tutte le ancore del nucleo usano gli STESSI z_U.
Ogni ancora sceglie una combinazione convessa delle righe ancora ammesse. Le sue
quattordici tracce sono legate agli z_U con contributi del nucleo sottratti una sola
volta. Una famiglia reale sceglie una riga sola e dà una soluzione integrale.
Consentire frazioni allarga il problema; la fattibilità non costruirebbe una famiglia.

Nei due nuclei della riga5 questo sistema è già incompatibile. Nei tre della riga8
si aggiungono selettori condivisi dell'intera distribuzione del grado di ogni punto,
non soltanto l'uguaglianza dei gradi medi attraverso le ancore.

Ciascuno dei tre nuclei contiene una coppia di membri DISGIUNTI. Un membro
con traccia vuota sarebbe disgiunto da entrambi e formerebbe un sunflower vuoto.
Quindi z_vuoto=0. In F69, i13 membri del nucleo lasciano esattamente56 altri membri:

    Σ_(U≠∅) z_U=56.

Non è lecito imporre questa equazione senza la coppia disgiunta. Il checker ne
ricostruisce una in ogni sistema che usa il conteggio totale. Due dei tre sistemi
sono ora incompatibili; rimane l'ultimo nucleo.

### 3.1 H27 su unioni di categorie realmente intersecanti

Due classi di traccia U,V sono sicuramente
cross-intersecanti se U∩V≠∅. Lo sono anche quando un membro A del nucleo evita
U∪V: due loro membri disgiunti, insieme ad A, darebbero un sunflower vuoto.
Una singola categoria U nonvuota è intersecante con se stessa.

Si sceglie una collezione di categorie a due a due compatibili in questo senso,
più eventualmente alcuni membri del nucleo. Questi ultimi devono incontrarsi
fra loro e incontrare ogni traccia selezionata. L'UNIONE delle famiglie effettive
è intersecante, dunque sotto H27:

    Σ_(U selezionato) z_U ≤27−numero dei membri del nucleo selezionati.

Categorie diverse sono disgiunte come insiemi di quadruple. Un membro aggiuntivo
non coincide con un membro del nucleo perché incontra R in≤1 punto.

Sono state prodotte sette disuguaglianze di questo tipo. Il verificatore
controlla ogni coppia di categorie e ogni membro fissato della collezione mediante
intersezioni letterali. Non assume che un qualunque insieme di tracce sia
intersecante. I sette limiti chiudono il quinto sistema. Il solver ha cercato
collezioni e moltiplicatori; la validità dei limiti non dipende dal solver.

### 3.2 I cinque certificati

I costruttori a maschere e a insiemi confrontano letteralmente variabili,
intervalli, coefficienti e membri destri. Con Az≤b, Ez=f, l≤z≤u e moltiplicatori
interi y≥0,η liberi, si calcolano

    q=Aᵀy+Eᵀη, H=y·b+η·f,
    L=Σ_j min(l_jq_j,u_jq_j).

Ogni soluzione deve soddisfare L≤q·z≤H. Un gap H−L<0 è una contraddizione esatta.
Tutti i coefficienti negativi sono pagati sui loro intervalli.

|Nucleo/certificato|Variabili|Uguaglianze|Disequazioni|H|L|H−L|
|---|---:|---:|---:|---:|---:|---:|
|C5_6|1.962|225|141|−1.500|−415|−1.085|
|C5_8|1.006|225|129|−27|−15|−12|
|G8_0_0|1.201|416|39|−37|−33|−4|
|G8_1_0|1.235|417|61|−368|−354|−14|
|H27_CORE_8_2|1.292|418|99|−26.703|−25.964|−739|

Le etichette C5_6/C5_8 indicano la RIGA5 e l'indice del nucleo; NON il lemma
geometrico C5 importato. I valori nella tabella sono interi alla normalizzazione
del singolo certificato, non cardinalità negative e non confronti fra tolleranze.

Ogni ancora45 di F69 produce una delle36 righe, uno dei2.335
nuclei, e una delle2.330 ancore impossibili oppure una soluzione di uno dei cinque
sistemi. Tutti sono esclusi. Quindi |N[R]|≤44 per OGNI membro della candidata. □

