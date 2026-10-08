# Complete degree17 local exclusion

Read [CURRENT_PREMISES.md](CURRENT_PREMISES.md) for the precise premises and their locations. The proof below gives the local reduction, symmetry, complete domain and pruning arguments.

## 1. Il modello su una sola componente: tutti gli interni rimangono ammessi

Su S={0,…,5} poniamo

    P10 = 012 015 023 034 045 124 134 135 235 245;
    P9  = P10 senza012.

Il centro ha etichetta6 e grado17. Gli altri membri del link, disgiunti da S,
sono sette per P10 e otto per P9. Non se ne fissano altre caratteristiche.
Sia I=F∩C(S,4) l'intero interno, comprese tutte le assenze. Per ogni ∅≠U⊆S,
|U|≤3, n_U conta i membri che evitano il centro e hanno traccia esattamente U.
Sono41 coordinate (6+15+20). I membri con traccia vuota e il numero dei punti
esterni non hanno una variabile di cap nel nucleo.

I box nonvuoti derivano dalle capacità17/6/2 meno i membri già prescritti
contenenti U. Una traccia è esclusa se un suo membro, con due coni/interni fissati,
forma un sunflower: il test dipende solo dalla traccia, poiché i due membri fissi
sono sul core S∪{6}. La scelta della loro estensione esterna non ripara il divieto.

Per y∈S sia I_y il numero degli interni contenenti y.
Se y ha stella C5, cancellare tali interni dal suo link dà

    d_F(y)−I_y≤15.

Per un P5 al grado17, E17 richiede I_y≥1: una componente intersecante di almeno
sette triple deve completare le quattro triple del cammino; soltanto due aggiunte
possono estendere all'esterno la sua unica copertura di due punti. I7 non viene
identificata con P8 o Q8.

Se s_y≥8 o la classificazione di un grado17 rende controllata la
parte K_y, si applica il confinamento importato: tutti i membri prescritti del
link di y stanno in K_y e devono essere intersecanti. Un'aggiunta che evita il
centro copre la stella. Nel C5 è interna; nel P5 può usare la sua unica coppia
di copertura, al massimo due volte. Quando |K_y|≥8, la classificazione la confina
ai sei punti già occupati. Non si impone intersecanza quando queste premesse mancano.

Ogni punto ha UN selettore del suo grado; ogni ancora
sceglie una riga completa di quattordici tracce. Le ancore condividono gli STESSI
n_U e gli STESSI gradi. Presenze e assenze interne sono assegnate nel singolo caso,
non inferite preventivamente. Ogni famiglia effettiva dà una soluzione integrale;
permettere combinazioni convesse allarga il dominio. Il modello non asserisce il
converso. Gli interni dell'altra componente non sono limitati.

Per un C5 consideriamo tutti i pair
attraverso y. Per un P5 escludiamo alternativamente una delle due categorie
associate alla sua unica copertura di due punti. Se b è il numero dei pair della
sottofamiglia ed h=n_{y}, sono necessari

    b≤6;   h≤(10,10,8,5,4,2,1)[b];   5h+9b≤59.

La prova distingue una stella di coppie esterne e un triangolo, con molteplicità
al massimo2 e codegree6 del punto/centro. Questi sono vincoli sulle quadruple,
non capacità assunte per una famiglia arbitraria di coppie. La foresta usa20
invece di10 quando b=0: è un rilassamento più largo, ancora sicuro.

## 2. P10⊔I7: dodici certificati nuovi e un raccordo esatto

### 2.1 Interni nonvuoti

Tutte le2^15 scelte interne danno292 interni compatibili con i dieci coni,
con distribuzione1,15,75,135,60,6 per taglia0,…,5. I60 automorfismi li dividono
in13 orbite. Un secondo enumeratore prova tutte le maschere e tutte le720
permutazioni; la copertura completa coincide.

Undici tipi nonvuoti hanno un'ancora senza righe (0=1). Il solo restante
I={0123} dà531 variabili,422 uguaglianze e12 disuguaglianze. Due disuguaglianze
pair e dodici uguaglianze hanno una combinazione che impone−8 a un'espressione
con minimo0 sui box. Contraddizione0≤−8; il gap normalizzato è−2/25.
Quindi tutti i dodici tipi nonvuoti sono esclusi. Il trasporto rinomina l'intera
famiglia e non le impone un gruppo di simmetria.

### 2.2 La soglia nuova produce le stesse dieci righe elementari, non una copia di μ43

Con interno vuoto i sei vicini hanno grado≤15. Su un'ancora x∪{a,b,c}
poniamo e=n_{abc}, w le tre tracce pair ed s le tre singleton dei vicini. Si ha

    e∈{0,1}, 0≤w≤3, k_i=5+e+w_ij+w_ik,
    d_F(i)=k_i+s_i≤15,
    |N[R]|=17+e+Σw+Σs≥42.

R42.7/N42.7 impone s_i≤8. Se s_i=8, B4 e il C5 vuoto impongono k_i=5.
Il nuovo controllo enumera questi intervalli con17 e42, indipendentemente dal
predicato. Sono dieci righe; tutte le cento righe delle dieci ancore del modello
completo coincidono con esse. La disuguaglianza residua è e+Σw+Σs≥25: è ESATTAMENTE
la stessa del vecchio nucleo18/43. Questo raccordo riguarda le coordinate dei
vicini e non afferma che una F69 possa essere trasformata in una F70.

I tre profili sui sei punti sono tutti15, un14/cinque15 oppure
un13/cinque15. L'ultimo è impossibile: se0 ha grado13, l'ancora012 impone al
margine residuo m_12 il valore3, mentre124, tutta di grado15, impone m_12≤2.
Rimangono due profili.

### 2.3 Il nucleo finito ereditato viene rigiocato integralmente

Il produttore combina righe di ancore; il verificatore enumera maschere
dei margini pair e completa le triple in ordine inverso. Le intere liste di41
coordinate coincidono:

|Profilo|Pattern dei margini|Proiezioni|
|---|---:|---:|
|tutti15|332|17.303|
|un14/cinque15|11|946|
|Totale||18.249|

Le regole sono universali: cap6 dei pair attraverso un C5, uguaglianze
fra estensioni forzate dai coni, unicità di una quadrupla, cap20 dei gradi esterni
e cap6 delle codegree. Il cap20 è più largo del cap17 corrente. Ogni proiezione
ha un testimone verificato di violazione; zero aperte.

I due file di testimoni sono conservati IDENTICI, con il loro header
storico μ43/centro18. Non sono stati rinominati per simularne una nuova scoperta.
`check_p10_bridge.py` ricostruisce PRIMA il dominio17/42 e ne prova l'identità
combinatoria; poi rigioca i testimoni e le due generazioni complete. La nuova
conclusione mantiene C5 e R42, non importa R43. Il sottoramo P10⊔I7 è escluso,
qualunque sia I7 e senza un cap sul supporto esterno.

## 3. P9⊔I8: settantacinque interni refutati e quattro residui esatti

Per P9 sono373 gli interni compatibili, in79 orbite sotto6 automorfismi.
Il nuovo modello del centro17 con otto membri esterni nel link ne esclude75:
71 con un'ancora vuota e4 mediante combinazioni aritmetiche. Tutti i sistemi
sono ricostruiti da due programmi e confrontati letteralmente.

Restano esattamente

    P9_000: ∅;
    P9_002: {0134};
    P9_003: {0135};
    P9_004: {0345}.

Le loro orbite interne hanno taglie1,3,6,3. Non si assumono dunque gli interni
vuoti: gli ultimi tre casi vengono mantenuti per intero nella ricerca seguente.

## 4. I punti esterni devono essere gli stessi attraverso tutte le ancore

Per ogni tripla U una sua occorrenza rappresenta U∪{z}. Due occorrenze
della stessa U hanno estensioni distinte, per semplicità. Le nuove foreste
mantengono le estensioni anche in presenza dell'interno singleton assegnato.

Per un cono o interno fissato C e una categoria singleton/pair/tripla,
si controllano le tre intersezioni letterali. Se evitare z formerebbe un
sunflower con C e U∪{z}, ogni membro di quella categoria deve contenere z.
I coni sono soltanto i nove blocchi presenti: il blocco omesso012 non viene
reintrodotto. Gli interni prescritti possono dare ulteriori obblighi validi.

Una singleton con almeno tre membri obbligata da due estensioni forza la loro
uguaglianza, altrimenti la tripla che le unisce al punto singleton avrebbe
codegree≥3. Una categoria pair con almeno due membri forza la stessa uguaglianza:
due valori esterni distinti riempirebbero entrambe le posizioni, dando una sola
quadrupla. Le relazioni dirette fra due triple danno altre uguaglianze.

Si prende la chiusura transitiva. Per una classe C di occorrenze che
rappresentano il medesimo punto esterno, si contano l'INSIEME delle categorie
singleton e pair obbligate, una sola volta ciascuna. Sono limiti inferiori per
il suo grado e le sue codegree. Una duplicazione della stessa tripla nella classe
è impossibile; un grado esterno>17 o una codegree>6 è impossibile. Classi non
unite non vengono presunte distinte: ulteriori coincidenze non eliminano il
sovraccarico già forzato da una singola classe.

Se n_U=2, i due esterni sono distinti e tutte le categorie obbligate da U
contengono entrambi: la somma di tali categorie non può superare6. Questo è
un ulteriore rifiuto, non l'assunzione di una separazione arbitraria degli esterni.

## 5. Dominio completo e foreste delle quattro P9

### 5.1 Il raccordo con gli interni è esatto

Sia f_y il numero di membri prescritti (coni più interni) attraverso y.
Il margine m_ij conta soltanto residui NON interni contenenti ij. Per T in P9,
la riga dell'ancora fornisce

    n_T=t_0−#{Q∈I:T⊆Q},
    m_ij=p_ij+t_0−#{Q∈I:ij⊆Q}.

Il contributo degli interni non viene sottratto due volte. Dopo le triple,
le altre coordinate sono determinate:

    n_ij=m_ij−Σ_(U⊇ij,|U|=3)n_U,
    n_y=d_F(y)−f_y−Σ_(j≠y)m_yj+Σ_(U∋y,|U|=3)n_U.

Tutti i gradi, i margini e le triple assegnate devono accordarsi fra le nove
ancore. Le11 triple non prescritte sono visitate su TUTTI i valori interi
consentiti dai box universali e dalla capacità residua delle tre coppie.

I domini completi sono:

|Interno|Righe sulle nove ancore|Profili etichettati, con interno fissato|Profili canonici|
|---|---:|---:|---:|
|∅|1.392|520|122|
|{0134}|1.057|218|118|
|{0135}|1.263|258|258|
|{0345}|1.694|671|372|
|Totale|5.406|1.667|870|

Per gli interni nonvuoti si usa il loro STABILIZZATORE, non l'intero gruppo P9.
Questi conteggi riguardano profili interni e gradi, non famiglie o classi di
isomorfismo delle famiglie. La rinominazione non identifica punti distinti.

### 5.2 Una foglia anticipata deve escludere tutti i completamenti

Per ogni prefisso, ciascuna tripla ancora libera è maggiorata dalla
capacità residua minima delle sue tre coppie e dal suo box. Sottrarre tutte
queste capacità dà un limite INFERIORE sulle categorie pair. Le identità di
incidenza danno limiti inferiori e superiori sulle singleton. I rifiuti usano
soltanto condizioni necessarie monotone: singleton certamente negative, capacità
pair/singleton o box superati, coppia di estensioni sovraccarica, duplicazione,
grado esterno>17, codegree>6.

Il verificatore ricostruisce tutte le alternative del raccordo e ogni figlio
intero del prefisso. Non accetta byte mancanti, aggiunti, un codice OPEN o una
ragione falsa. Il vecchio codice opzionale H8 è DISABILITATO: nessuna delle
prove consegnate lo usa. Il cap27 sul pool è pure non portante e non viene
usato nelle foreste.

Tutte le quattro foreste sono esaurite, senza cutoff nei run negativi:

|Interno|Raccordi delle ancore|Pattern dei margini|Nodi di prefisso|Foglie|
|---|---:|---:|---:|---:|
|∅|919.446|567.693|13.672.861|7.280.909|
|{0134}|23.992|13.081|20.065|15.156|
|{0135}|112.533|49.349|104.818|68.474|
|{0345}|482.457|240.980|582.379|350.104|
|Totale|1.538.428|871.103|14.380.123|7.714.643|

C++ genera i byte della foresta; Python usa componenti di un grafo e
intersezioni di insiemi per verificare le ragioni, e ricalcola il dominio con
il costruttore a partizioni/t-prima-di-p. La rigenerazione C++ deve produrre
byte identici. Non sono due censimenti umani indipendenti, né una prova formale.

Ogni famiglia ipotetica induce un interno fra i79, e poi uno dei
profili e un percorso coperto. Settantacinque interni sono refutati linearmente;
nei quattro rimanenti ogni percorso termina in una contraddizione verificata.
Nessuna P9 isolata può comparire nel link del centro17 nelle ipotesi della nota.
Insieme al §2 ed E17, questo dimostra il teorema locale: il massimo17 è escluso.


## 7. Natura aritmetica dei certificati

Per Az≤b, Ez=f, l≤z≤u, con moltiplicatori interi y≥0,η liberi, si calcolano
q=Aᵀy+Eᵀη, H=y·b+η·f e L=Σ_j min(l_jq_j,u_jq_j). H<L è una contraddizione perché
una soluzione dovrebbe soddisfare L≤q·z≤H. Ogni box è pagato esattamente. La scala
positiva è metadato di normalizzazione e nessuna tolleranza decide la verifica.
Il solver serve soltanto a proporre combinazioni.

Gli87 certificati nuovi sono12 P10 e75 P9;82 hanno un'ancora senza righe
e5 usano combinazioni nontriviali. La tabella completa riporta dimensioni e gap.
I file di P10 vuota sono due certificati finiti ereditati, rigiocati dopo il nuovo
raccordo; le870 prove P9 sono nuove foreste al cap17, non i vecchi certificati
al cap18 ri-etichettati.

