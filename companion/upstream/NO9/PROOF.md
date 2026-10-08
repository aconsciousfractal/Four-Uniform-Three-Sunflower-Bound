# Complete singleton9 exclusion at degree16

Read [CURRENT_PREMISES.md](CURRENT_PREMISES.md) for the precise premises and their locations. The proof below gives the local reduction, symmetry, complete domain and pruning arguments.

## 1. Le due componenti residue vengono trattate con i loro interni effettivi

S={0,…,5}, x=6 nel nucleo locale. Si fissa

    P9 = 015 023 034 045 124 134 135 235 245.

Il centro x ha grado16 e gli altri sette membri del link evitano S. Il loro
numero di punti e le loro etichette non sono limitati. L'interno è
I=F∩C(S,4), assegnato con presenze E assenze.

Le373 scelte interne compatibili formano79 orbite sotto
i6 automorfismi della P9. Due generatori ricostruiscono l'intero catalogo. Sono
rigiocati77 certificati ereditati,75 immediati e2 nontriviali. I soli casi rimasti
prima della chiusura mediante le foreste sono I=∅ e I={0345}, con orbite rispettivamente1 e3.
I due punti razionali dei precedenti rilassamenti sono verificati ancora: restano
fattibili come punti dei modelli LINEARI, non come famiglie effettive.

### 1.1 Il dominio mantiene le stesse41 tracce in tutte le ancore

Per ∅≠U⊆S, |U|≤3, n_U conta i membri che evitano x
con intersezione esattamente U su S. Sono6 singleton,15 coppie e20 triple.
Gli interni sono contabilizzati separatamente. I membri con traccia vuota e il
numero dei punti esterni NON sono limitati.

I box sono16/6/2 meno i coni e gli interni contenenti U. Un tipo è vietato solo
quando una sua qualsiasi estensione forma un sunflower con due membri fissati:
le tre intersezioni dipendono allora soltanto dalla traccia.
Ogni vicino ha UN grado globale condiviso. C5 impone d(y)−I_y≤15. Quando B4
rende intersecante K_y, si conservano il confinamento e le eventuali due
aggiunte esterne del P5. Non si presume K_y intersecante quando la sua ipotesi manca.

I due costruttori confrontano letteralmente tutte le righe, le equazioni,
i box e le identità delle variabili. La nuova copertura dà:

|Interno|Righe sulle9 ancore|Profili etichettati|Profili canonici|Stabilizzatore|
|---|---:|---:|---:|---:|
|∅|261|30|11|6|
|{0345}|483|82|49|2|

Il gruppo del secondo caso è lo stabilizzatore dell'interno, non l'intero
Aut(P9). Questi60 casi sono profili di gradi e tracce, non60 famiglie.
Il tentativo iniziale di aggiungere uno alla sola singleton del centro e usare
il vecchio dominio D17 NON era valido per tutte le righe: rimanevano6 occorrenze
di righe nel caso vuoto e2 nell'altro. Tutte sono mantenute nel nuovo censimento.

### 1.2 Copertura intera dei margini

Sia f_y il grado già prescritto dai coni e dall'interno. Si accordano
tra le nove ancore gli stessi gradi d_y, margini m_ij delle coppie e n_T dei
blocchi T della P9. I contributi interni vengono sottratti una sola volta.
Per le11 triple non prescritte si provano tutti gli interi consentiti dai box
e dalla capacità residua delle loro tre coppie. Poi

    n_ij = m_ij − Σ_(U⊇ij, |U|=3) n_U,
    n_y  = d_y − f_y − Σ_(j≠y)m_yj + Σ_(U∋y, |U|=3)n_U.

Ogni famiglia reale determina uno di questi percorsi. I punti distinti con
uguali dati numerici non vengono identificati.

## 2. Le estensioni sono punti della stessa famiglia

Un'occorrenza tripla U rappresenta U∪{z}. Se un cono o interno fissato,
questo membro e un membro di una categoria singleton/pair formerebbero un
sunflower quando z viene evitato, OGNI membro di quella categoria contiene z.
Analogamente si ricavano uguaglianze dirette di estensioni da due triple.
I testimoni usano soltanto coni realmente presenti:012 non viene reintrodotto.

Due estensioni che forzano una singleton di almeno3 membri devono coincidere,
per il cap2 di una tripla. Se forzano una categoria pair di almeno2 membri,
devono coincidere per semplicità: due esterni distinti riempirebbero le due
posizioni esterne e darebbero una sola quadrupla.

Per una classe C di occorrenze con il medesimo esterno z, si prendono gli INSIEMI
di categorie singleton e pair obbligate, contandole una sola volta. Esse danno
limiti inferiori al grado di z e alle codegree d(y,z). Le categorie delle tre
cardinalità di traccia sono disgiunte. Si respinge una quadrupla duplicata,
un grado oltre16 o una codegree oltre6. Classi non unite non sono presunte
distinte: un'ulteriore coincidenza non ripara un sovraccarico già presente.

Due estensioni della STESSA tripla devono invece essere distinte. Tutte le
categorie da essa obbligate contengono entrambi gli esterni e la loro somma
non può superare la codegree6 della coppia esterna.

Se b conta i pair attraverso un vicino C5 e h la
sua singleton, si hanno b≤6 e

    h≤(20,10,8,5,4,2,1)[b].

A b=0 la foresta usa20, più largo del cap10 effettivo. Nel P5 si applica la
regola alle due sottofamiglie che escludono alternativamente uno dei due
vertici della sua unica copertura di due punti. Non si applica il caso C5
all'intera famiglia pair del P5.

### 2.1 Un rifiuto anticipato riguarda tutti i completamenti

In un prefisso, ogni tripla libera viene maggiorata dal suo box e
dalle tre capacità residue pair. Sottrarre tutte queste capacità dà limiti
INFERIORI ai pair ancora necessari. Le identità sopra danno limiti inferiori
e superiori alle singleton. Si impiegano soltanto condizioni necessarie
monotone: un sovraccarico, un'uguaglianza forzata, una duplicazione o una
singleton certamente negativa non si riparano aggiungendo membri.

Il checker ricostruisce tutti i figli e la ragione di ogni foglia. I codici
OPEN, il vecchio taglio H8, byte mancanti o aggiunti sono rifiutati. La nuova
foresta non usa H27-pool, H8, un cutoff di nodi o un limite di tempo. Il C++ si
fermerebbe dichiarando INCOMPLETE se trovasse una proiezione aperta: nessun
record finale ha questo stato.

Output confrontati integralmente dal produttore e dal checker:

|Interno|Raccordi ancore|Pattern margini|Nodi prefissi|Foglie refutate|Aperte|
|---|---:|---:|---:|---:|---:|
|∅|2.626|1.280|31.321|17.121|0|
|{0345}|9.529|3.916|9.705|5.656|0|
|Totale|12.155|5.196|41.026|22.777|0|

|Ragione foglia|∅|{0345}|
|---|---:|---:|
|Singleton certamente negativa|3|0|
|Limite pair/singleton|5.077|16|
|Coppia esterna sovraccarica|3.307|8|
|Quadrupla duplicata|392|1|
|Grado esterno oltre16|3.712|287|
|Codegree oltre6|4.630|451|
|Box di traccia superato|0|4.893|

La copertura ereditata riduce ogni interno reale a uno dei due
residui. La nuova copertura delle righe e dei gradi contiene il suo percorso;
la relativa foglia viola una condizione necessaria. Nessuna P9 isolata può
quindi comparire nel link di un punto16 nelle ipotesi locali.

## 3. Nessuna singleton9; nuovo dominio uniforme

Se s_x(R)=9, R42/N42 e Δ≤16 impongono k_x=7 e d(x)=16. Le9 triple
disgiunte dall'ancora del link formano una P9. Il blocco omesso non può esserci,
altrimenti la singleton sarebbe10. L'isolamento rende disgiunti dal suo supporto
gli altri7 membri del link. Il teorema appena dimostrato dà una contraddizione.
Una singleton10 richiederebbe almeno10+7=17 nel grado globale. Quindi s≤8 ovunque.

I due generatori ricostruiscono e confrontano l'intera lista di24.002
righe,71 profili di grado. Non è aggiunto un filtro I7 non dichiarato.

|Intorno|Righe|Minimo grado|Somma minima coppia/membro|Massima carica Σ1/d|
|---|---:|---:|---|---|
|42|16.823|8|24/54|5/16|
|43|5.732|9|25/56|43/144|
|44|1.290|13|27/58|18/65|
|45|157|14|29/60|4/15|

Ogni punto usato appartiene a un membro, dunque ha grado≥8.
Il doppio conteggio |supp F|=Σ_R Σ_(v∈R)1/d(v) dà n≤69·5/16, quindi n≤21;
276≤16n dà n≥18. Il successivo uso delle fibre migliora il21 in20.


## Appendix: centre16 inherited interior exclusion

## 6. Primo avanzamento nel massimo16: P9 da79 a due interni

### 6.1 Dominio diverso, ricostruito a42

Si assume un punto x di grado16 con una P9 isolata su S={0,…,5}.
P9 è P10 privata di012, con P10=012,015,023,034,045,124,134,135,235,245.
Gli altri sette membri del link evitano S. Il centro nelle routine ha etichetta6:
questa etichetta non è un limite al supporto esterno.

Per ogni interno I=F∩C(S,4), assegnato con tutte le presenze e assenze, si usano41
conteggi n_U delle tracce nonvuote di taglia≤3. I membri a traccia vuota restano
non limitati. I box sono le capacità16/6/2 meno i coni e gli interni già prescritti.
I sei gradi sono condivisi attraverso tutte le nove ancore. I punti usati hanno
grado≥4; questo è più debole del minimo6 del dominio cap16 ereditato, quindi sicuro.

Per un punto C5, d(y)−I_y≤15. Quando la singleton di una
CENTRALE è≥8, B4 e il confinamento importato impongono una parte K_y intersecante
che contiene i membri prescritti. C5 non permette altre aggiunte esterne; P5 ne
permette al massimo due sulla sua unica copertura di due vertici, e quando
|K_y|≥8 i modelli importati la confinano ai sei punti. Non si applica questo
vincolo ad ancore generiche senza ricostruirne le ipotesi.

Per C5 si sommano tutte le categorie pair attraverso y; per P5 si esclude
alternativamente una delle due categorie della sua copertura minima. Con h=n_y
e b conteggio pair della sottofamiglia, si impongono b≤6 e5h+9b≤59. Sono limiti
necessari ereditati, non un'asserzione che tutte le famiglie esterne siano realizzabili.

### 6.2 Catalogo e77 certificati

L'augmentazione delle quadruple interne e un distinto controllo di tutte
le2^15 maschere danno373 interni, in79 orbite sotto i6 automorfismi P9. Tutti i79
modelli sono confrontati letteralmente, comprese le righe pair/singleton.

Settantacinque hanno già un'ancora senza alcuna riga. Altri due sono confutati
con combinazioni esatte:

|ID|Interno|Variabili|Uguaglianze usate|Disequazioni usate|H|L|H−L|
|---|---|---:|---:|---:|---:|---:|---:|
|P9_001|{0123}|312|12|0|−197|−23|−174|
|P9_019|{0135,1234}|385|21|2|−22|−21|−1|

Il cap è16, non17; il centro ha16 triple, non17. I vecchi certificati non vengono
copiati cambiando la sola intestazione.

Restano solo vuoto e{0345}, a meno di Aut(P9). Le orbite hanno
rispettivamente1 e3 elementi: quattro interni etichettati. Questi sono tipi di
interni, non quattro famiglie globali. Gli interni possono essere compatibili
con le ancore e tuttavia non avere alcuna estensione effettiva.

### 6.3 I due modelli aperti hanno punti razionali verificati

I file in `data/inherited/` forniscono
valori razionali per TUTTE le variabili. La verifica con Fraction controlla ogni
box, ogni uguaglianza e ogni disequazione, senza tolleranza:

|Interno|Variabili|Coordinate nonintere|Massimo denominatore|Somma singleton|
|---|---:|---:|---:|---|
|Vuoto|374|80|408|1504/51|
|{0345}|595|66|754|350/29|

Questi non sono famiglie effettive e non certificano un massimo dell'obiettivo.
Dimostrano soltanto che i precisi rilassamenti lineari non sono incompatibili.
NON comprendono H27-pool. In particolare il punto del caso vuoto supera27 nel
pool e non sarebbe ammissibile dopo tale rafforzamento.

### 6.4 Applicazione alle singleton9 e limite della riduzione

Se s_x(R)=9 nel cap16, allora k_x≥7 e d(x)≤16
forzano d(x)=16,k_x=7. Le nove triple disgiunte dall'ancora del link formano una
P9. Il suo blocco omesso non può essere presente, altrimenti la singleton sarebbe
almeno10. L'isolamento importato rende disgiunti dal supporto P9 gli altri sette
membri del link. La riduzione appena provata si applica quindi al suo interno.

