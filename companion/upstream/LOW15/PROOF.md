# Complete maximum-degree-at-most15 exclusion

Le premesse precise del risultato locale e il loro ruolo sono indicati in [CURRENT_PREMISES.md](CURRENT_PREMISES.md).

## 1. Il dominio delle ancore da coprire è finito ed esatto

Su R={0,1,2,3} scriviamo una riga r=(p,t,s), con sei p_ij in ordine
lessicografico, quattro t_i che omettono i e quattro singleton s_i. Si ha

    k_i=1+Σ_(j≠i)p_ij+Σ_h t_h−t_i,
    d_i=k_i+s_i,
    |N[R]|=1+Σp+Σt+Σs.

Due generatori, con diversi ordini p/t e differenti controlli delle
identificazioni, ricostruiscono letteralmente lo stesso dominio cap15:

|Intorno|42|43|44|45|Totale|
|---|---:|---:|---:|---:|---:|
|Righe con gradi ordinati|5.594|1.319|151|10|7.074|

Espandendo tutte le24 permutazioni si ottengono29.043 righe distinte interamente
orientate. Le161 righe di intorno≥44 formano28 orbite sotto S4. Ogni riga alta
ha almeno un s_i≥8, come controllato sull'intera lista.

Ogni ancora reale può essere rinominata ordinando i gradi
e poi portando la sua riga al rappresentante dell'orbita. Si rinomina l'INTERA
famiglia, non si suppone che sia invariante per S4. Nessuna riga di intorno≥44
viene scartata sulla base di un modello numerico.

## 2. Il nucleo completo dei membri che incontrano R in almeno due punti

Definiamo

    C(R)={Q∈F:|Q∩R|≥2}.

Il nucleo contiene R, tutte le categorie p_ij e tutte le categorie t_i; ha
esattamente1+Σp+Σt membri. Le singleton di R e i membri disgiunti da R NON
appartengono al nucleo e possono usare punti esterni arbitrari.

### 2.1 Forme complete delle singole categorie

Dopo aver tolto la coppia ij, i p_ij membri diventano coppie esterne
DISTINTE e intersecanti. Due coppie disgiunte, insieme a R prima della rimozione,
darebbero un sunflower con nucleo ij. Per tre coppie, una stella a centro comune
è vietata perché le tre quadruple avrebbero un nucleo triplo. Pertanto:

|p_ij|Forma delle coppie esterne|
|---|---|
|0|Categoria vuota|
|1|Un arco, due punti|
|2|Un cammino di due archi, tre punti|
|3|Un triangolo, tre punti|

Per t_i=1 c'è un solo punto esterno aggiunto a R\{i}. I punti introdotti nelle
diverse categorie possono coincidere; non se ne presume la disgiunzione.

Se s_i≥8, la parte K_i del link di i che incontra R\{i} è
intersecante. Sono precisamente i membri del nucleo attraverso i, con i tolto.
Quindi due membri del nucleo non possono avere intersezione esattamente{i}.
Questa restrizione viene applicata SOLTANTO agli i con s_i≥8.

### 2.2 Perché la generazione non nasconde un cap sul supporto

Si aggiungono le categorie
una dopo l'altra. Per ogni vertice del loro arco/cammino/triangolo si considerano
tutte le assegnazioni iniettive ai punti esterni già introdotti oppure a punti
nuovi. Questi ultimi vengono rinominati consecutivamente nell'ordine di prima
comparsa. Qualunque nucleo reale determina una di tali scelte a ciascun passo.
Le sole potature sono: quadrupla duplicata, sunflower letterale fra tre membri,
oppure violazione dell'intersecanza K_i appena provata.

I controlli sono monotoni: aggiungere membri non ripara la violazione. NON si
impone un universo di7,8,9 o10 punti prima della ricerca. Il numero dei nuovi
punti è finito perché ogni categoria ha al massimo tre vertici esterni, e il
numero delle categorie è già fissato dalla riga. La canonicalizzazione finale
permette tutte le permutazioni dei punti esterni fissando R.

Il produttore enumera iniezioni dei modelli; il verificatore sceglie
sottoinsiemi di vertici e, per il cammino, il centro. Usano anche ordini diversi
delle categorie. Le liste COMPLETE dei nuclei canonici coincidono.

Undici delle28 orbite non ammettono alcun nucleo. Le altre17 danno35 record:

|Supporto effettivo del nucleo|7|8|9|10|Totale|
|---|---:|---:|---:|---:|---:|
|Record|15|1|11|8|35|

Non sono35 famiglie globali né35 classi d'isomorfismo globali. Ogni record fissa
una riga e un nucleo con quella riga. [data/HIGH_ANCHORS.json](data/HIGH_ANCHORS.json)
contiene tutte le28 orbite di ancore, mentre [data/CORES.json](data/CORES.json)
contiene i35 record di nuclei. L'`id` dell'ancora corrisponde al `row_id` del
record di nucleo: un'ancora senza record corrispondente ha zero nuclei.
[scripts/check_math.py](scripts/check_math.py) ricostruisce separatamente
l'intero censimento per ciascuna ancora e ne verifica l'uguaglianza con i
record distribuiti, comprese le undici orbite senza nucleo.

## 3. Trentatré nuclei sono incompatibili con un'altra loro ancora

Sia V l'unione dei punti di un nucleo C fissato. Per ogni membro aggiuntivo
Q∈F\C, la traccia U=Q∩V ha taglia al massimo4 e |U∩R|≤1. Quest'ultima condizione
discende dalla COMPLETEZZA di C(R), non dal divieto di una singola marcatura.

Una traccia nonvuota U è vietata se due membri A,B di C soddisfano

    U∩A=U∩B=A∩B.

Ogni estensione di U fuori da V conserverebbe quelle intersezioni, dando un
sunflower. Altrimenti il numero z_U di membri aggiuntivi con tale traccia ha box

    0≤z_U≤c_|U|−#{A∈C:U⊆A},     (c_1,c_2,c_3,c_4)=(15,6,2,1).

È un limite superiore, anche quando largo. La traccia vuota non è limitata né
rappresentata: i suoi membri sono disgiunti da ogni ancora del nucleo e non
contribuiscono ai gradi dei punti di V. Non influenzano alcuna equazione usata.

Scegliamo un membro effettivo A del nucleo. Per ogni traccia propria
nonvuota T⊂A, il contributo minimo è il numero dei membri di C con traccia T;
il massimo aggiunge TUTTE le capacità dei z_U con U∩A=T. È sicuro maggiorare
così anche estensioni non simultaneamente compatibili.

Il grado globale dei punti di R resta quello della riga iniziale; quello di
ogni altro punto dell'ancora è almeno il suo grado già fissato nel nucleo.
Una riga locale effettiva deve appartenere alle29.043 righe orientate e rispettare
questi intervalli. Si ammettono per le altre ancore tutti gli intorni≥42, non
si impone≥44.

Per33 dei35 record esiste una loro ancora A senza alcuna riga possibile.
`data/CORES.json` conserva A e tutti i14 intervalli; entrambi i ricostruttori
ricontrollano integralmente il dominio. Questo esclude tutti i completamenti
su qualunque numero di punti esterni, non soltanto le quadruple su V.

## 4. L'ultimo nucleo: una combinazione esatta di33 uguaglianze

I due record rimasti appartengono all'orbita7 e sono equivalenti. La riga è

    p=(0,3,3,3,3,1),  t=(0,0,0,0),  s=(8,8,7,7),  d=(15,15,15,15).

Uno dei nuclei, ID(7,7), è:

```text
0123
0245 0246 0256
0345 0346 0356
1278 1279 1289
1378 1379 1389
2345
```

Sono14 membri su10 punti, non una famiglia completa. Il secondo sostituisce
2345 con2378. La permutazione

    (0,1,2,3,4,5,6,7,8,9) ↦ (1,0,2,3,7,8,9,4,5,6)

trasporta i due nuclei, conserva la riga e dà una copertura esplicita.

### 4.1 Lo stesso z_U deve soddisfare tutte le ancore

Dopo le esclusioni di traccia del §3 ci sono87 z_U
nonvuoti. Per ogni ancora A del nucleo introduciamo una combinazione convessa
delle sue righe locali ammissibili. Per ciascuna delle14 tracce proprie nonvuote:

    contributo del nucleo + Σ_(U∩A=T) z_U
      = Σ_r λ_(A,r) conteggio_r(T),
    Σ_r λ_(A,r)=1,      0≤λ_(A,r)≤1.

TUTTE le ancore usano gli stessi87 conteggi, non un nuovo insieme per ogni A.
Il sistema conserva anche le capacità dei sottoinsiemi di V. Non si fissano
il numero totale dei membri, il numero dei punti esterni o H27. La traccia
vuota non interviene. Una famiglia reale sceglie un λ=1 per ogni ancora e induce
una soluzione integrale. La rilassazione frazionaria può essere più larga.

Il sistema completo ha486 variabili,210 uguaglianze e97 disequazioni.
I costruttori confrontano letteralmente ciascun coefficiente, membro destro,
box e identità della variabile. Il certificato `certificates/FINAL_CORE.json`
usa33 uguaglianze e NESSUNA delle97 disequazioni.

### 4.2 La verifica è fra interi, con tutti i box pagati

Per Az≤b, Ez=f e l≤z≤u, dati interi y≥0,η liberi, poniamo

    q=Aᵀy+Eᵀη,   H=y·b+η·f,
    L=Σ_j min(l_j q_j,u_j q_j).

Ogni soluzione soddisfa L≤q·z≤H. Un valore H<L è quindi una contraddizione.
Il certificato non ignora i coefficienti negativi e non usa tolleranze.

Nel sistema del nucleo:

    H=−435,    L=−89,    H−L=−346.

Si avrebbe

    −89≤−435,

impossibile. La scala1000 memorizzata serve a identificare la normalizzazione
di scoperta, non a decidere il segno. Il solver ha soltanto cercato η; il replay
non importa SciPy o NumPy.

### 4.3 Conclusione locale

Un'ancora reale di intorno≥44 determina una delle28 righe, un
nucleo compreso nella generazione e poi uno dei35 record. Undici righe non hanno
nuclei;33 record falliscono un'ancora; gli ultimi due sono confutati dal sistema
e dal trasporto. Non esiste alcun completamento. Dunque ogni ancora ha intorno≤43.

Il ponte finito→generale non extrapola un pattern: è la copertura dimostrata
della riga, delle identificazioni dei punti e di ogni completamento residuo.

## 5. Da questo lemma all'esclusione del cap15 di F69

Nikiforov, arXiv:1001.2070v1, §1, Theorem A, riporta il teorema di Jin:
per1≤k≤9, un grafo triangolo-libero di ordine n con δ>(k+1)n/(3k+2) è omomorfo
ad A_k. Il teorema di Jin è un risultato importato; la sua prova originale
non viene dimostrata né verificata dai checker qui distribuiti.

Non esiste un grafo G triangolo-libero
su69 vertici con α(G)≤27 e δ(G)≥26. Infatti26·11=286>276=4·69, quindi Jin con
k=3 dà G→A3. Rinominiamo A3 come Wagner W, con archi i~i±1,i+4 modulo8.
Siano a_i le cardinalità delle fibre, inizialmente anche zero, e

    b_i=a_(i−1)+a_(i+1)+a_(i+4)≤27.

I vicini di un indice W sono indipendenti, dunque la loro unione di fibre è
indipendente in G. Con δ_i=27−b_i si ha δ_i≥0 eΣδ_i=216−207=9. L'identità
W B=I+J, per B a salti0,±1, fornisce

    a_i=12−δ_(i−1)−δ_i−δ_(i+1)≥3.

Tutte le fibre sono nonvuote come CONSEGUENZA. Ogni vertice deve avere≥26 vicini
e li può trovare solo nelle fibre adiacenti, perciò b_i≥26. Ma allora

    208=8·26≤Σ_i b_i=3·69=207,

impossibile. Non si assume il blow-up completo né un matching di archi mancanti.

Se F69 avesse cap15, H27 darebbe μ≥42. Il teorema locale imporrebbe
|N[R]|≤43 su tutti i membri. Il grafo delle disgiunzioni, che ha per vertici i
MEMBRI di F69, sarebbe triangolo-libero, con α≤27 e grado minimo≥26. Contraddizione.
Il cap15 è quindi impossibile; con le altre esclusioni resta soltanto il massimo16.

Il checker verifica i64 coefficienti dell'identità, tutte le11.440 parole
nonnegative di somma9 e la rinominazione A3/W. Come controllo di bordo, i pesi
(8,8,8,9,9,9,9,9) danno un grafo di69 vertici con minimo25 e indipendenza26.
Non è una famiglia di quadruple. La prova del lemma è il conteggio sopra, non
una generalizzazione da quel controllo positivo.

