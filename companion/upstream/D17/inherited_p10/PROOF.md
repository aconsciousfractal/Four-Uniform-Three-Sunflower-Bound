# Complete finite P10 core: ALL15 and ONE14

The original finite-domain headers are retained in the certificates and verifier. Their application to17/42 is established by PROOF.md §2 and check_p10_bridge.py; the historical centre18/mu43 global application is not imported.

## 2. Dieci righe, gradi condivisi e due profili residui

### 2.1 Il cap15 sui sei vicini è ereditario

Se y∈S e d_F(y)≥16, scegliamo16 membri di L_y
includendo tutte le cinque triple della stella di x. Non ve ne sono altre
attraverso x, perché la componente P10 è completa e isolata. Sui sei punti
{x}∪(S\{y}) le sole triple sono proprio quelle cinque: qualunque altra che evita
x corrisponderebbe a una quadrupla interna aS. La sottofamiglia scelta sarebbe
un C5 vuoto di16 triple, vietato dal corollario importato. Pertanto d_F(y)≤15.

Questo passaggio NON richiede prima di escludere17,18,19,20: si sceglie una
sottofamiglia di16 triple. Non usa direttamente E17 per il vicino.

### 2.2 Ricostruzione elementare delle righe

Per A={a,b,c}∈P10 poniamo R={x,a,b,c}. Indichiamo con e il numero dei
residui con traccia A, con w=(w_ab,w_ac,w_bc) le tracce esatte di coppia fra i
punti di A, e con s=(s_a,s_b,s_c) le singleton. Si hanno

    e∈{0,1},  0≤w_ij≤3,
    k_i=5+e+w_ij+w_ik,
    d_F(i)=k_i+s_i≤15,
    |N[R]|=18+e+Σw+Σs≥43.

R43.7/N43.7 escludono s_i=9,10, perciò s_i≤8. Se s_i=8, B4 rende intersecante
K_i. Essa contiene l'intero cono x+C5; ogni ulteriore tripla che evita x deve
coprire C5 con tre punti, quindi sarebbe interna. Ne segue k_i=5.

Enumerare soltanto questi piccoli intervalli dà esattamente10 righe:

| Tipo, a meno di permutare a,b,c | w_ab,w_ac,w_bc | e | s_a,s_b,s_c | d_a,d_b,d_c | Righe |
|---|---|---:|---|---|---:|
| un13 | 0,0,3 |0|8,7,7|13,15,15|3|
| un14 | 1,1,2 |0|7,7,7|14,15,15|3|
| tutti15, e=0 |1,2,2|0|7,7,6|15,15,15|3|
| tutti15, e=1 |1,1,1|1|7,7,7|15,15,15|1|

Il controllo confronta anche letteralmente queste righe con quelle dell'auditor
upstream per P1,P2,Q. Ogni riga ha |N[R]|=43. Ogni coppia diS compare in due
blocchi P10: non possono quindi esserci due punti con grado inferiore a15.
I soli profili globali sui sei punti sono tutti15, un14/cinque15, un13/cinque15.

### 2.3 Il profilo13 cade su una codegree condivisa

Rinominare il punto13 come0 è lecito: il gruppo P10 è
transitivo sui sei punti. Nell'ancora012 la tabella forza e=0 e w_12=3. Il numero
m_12 dei residui che contengono la coppia12 è dunque3. L'altra ancora124 ha tre
gradi15 e forza m_12≤2. È la STESSA codegree residua: contraddizione3≤2.
Rimangono tutti15 e un14/cinque15. Non serve il precedente strato v3 di LP.

## 3. Tutte le proiezioni intere, senza fissare i punti esterni

Per ogni U⊆S con1≤|U|≤3 sia n_U il numero dei membri Q∈F che evitano x
e hanno Q∩S=U. Gli interni di taglia4 sono assenti. Ci sono41 coordinate nonvuote
(6+15+20). I membri con traccia vuota non entreranno nel nucleo: il loro numero
non viene limitato e nessun supporto esterno viene fissato.

Sia m_ij=Σ_(U⊇{i,j}) n_U. Per un blocco T∈P10,

    e_T=n_T,                 w_ij(T)=m_ij−n_T,
    d_F(y)−5=Σ_(U∋y)n_U.

Queste uguaglianze collegano tutte le ancore. Per T∈P10 si ha n_T≤1 (la tripla
ha già il membro xT); per T∉P10 si ha n_T≤2. Le due procedure esauriscono il
seguente dominio completo necessario.

Nel profilo tutti15 ogni m_ij è1 o2. In ogni blocco T, o tutti i tre
margini sono2 e n_T=1, oppure uno solo vale1 e n_T=0. I margini deboli formano
un matching sul grafo che collega i due blocchi di ogni coppia. Le2^15 scelte
si riducono a332 pattern. Nel profilo con0 di grado14, m_0j=1; sui cinque blocchi
che contengono0 il margine opposto è2 e n_T=0. Sui restanti si applica la regola
tutti15: rimangono11 pattern.

Per ogni pattern, dopo aver sottratto i n_T prescritti, si enumerano i valori0,1,2
delle dieci triple complementari, mantenendo tutte le capacità di coppia. I
conteggi delle coppie sono poi esattamente le capacità rimaste; quelli delle
singleton sono determinati dai sei gradi. Si respingono soltanto coordinate
negative. Nessun cutoff è previsto.

| Profilo normalizzato | Pattern dei margini | Proiezioni intere nonvuote |
|---|---:|---:|
| tutti15 |332|17.303|
| un14/cinque15 |11|946|
| Totale ||18.249|

Qualunque famiglia ipotetica determina un profilo e quei
margini. I suoi conteggi delle triple complementari sono uno dei valori visitati;
le coppie e singleton sono quindi ricostruite esattamente. Gli altri punti diS
sono rinominati, non identificati; non si impone un automorfismo aF.

Le18.249 sono proiezioni numeriche, NON famiglie o classi d'isomorfismo.
Il produttore unisce righe di ancore e assegna le triple in ordine crescente;
il checker visita maschere binarie di coppie e assegna le triple in ordine
inverso. Le LISTE COMPLETE di41 coordinate sono confrontate letteralmente.
Il numero di membri con traccia nonvuota è35–42 o37–42. Non è stata scartata
nessuna proiezione mediante un vincolo sul numero dei membri a traccia vuota.

## 4. Lemma delle tracce di due punti: al massimo sei per vicino C5

**Lemma.** Fissato y∈S, i residui Q con y∈Q e |Q∩S|=2 sono al massimo6.
Questo lemma non richiede μ43, cardinalità70, interni vuoti o un cap sul supporto.

**Dimostrazione.** Scriviamo tali membri come {y,j}∪E, con E coppia esterna a
S∪{x}. Due coppie esterne E,F devono incontrarsi. Se il loro j è lo stesso,
scegliamo un blocco P10 che contiene y,j: il cono e i due residui formerebbero
un sunflower con nucleo {y,j} se E,F fossero disgiunte. Se i due j,k sono diversi,
la stella C5 di y contiene un arco che evita j,k: due vertici coprono al massimo
quattro dei cinque archi. Il relativo cono e i due residui darebbero allora un
sunflower con nucleo {y}.

Le coppie esterne formano quindi una famiglia intersecante, con molteplicità.
Ogni stessa coppia {a,b} può comparire al massimo due volte: altrimenti la tripla
{y,a,b} avrebbe codegree almeno3. Se tutte le coppie hanno un punto comune z,
il codegree d_F(y,z) limita il totale a6. Se non esiste un punto comune, le
coppie distinte sono contenute nei tre lati di un triangolo: da ab,ac e da un
lato che evita a segue bc; un altro lato che incontra tutti e tre deve essere
uno dei tre. Con molteplicità al massimo2 il totale è ancora6. □

Poniamo B_y=Σ_(j≠y)n_{yj}. Ogni proiezione realizzabile soddisfa B_y≤6.

Per una stella P5 la sola coppia di vicini che può coprire
tutti gli archi è la sua unica2-copertura {a,b}. Eliminando i residui con traccia
{y,a}, oppure quelli con traccia{y,b}, lo stesso argomento dà

    B_y−n_{ya}≤6,             B_y−n_{yb}≤6.

Questa variante è usata nel controllo R99 del §9, NON nella chiusura P10.

## 5. Le estensioni esterne devono essere gli stessi punti fisici

### 5.1 Triple marcate e singleton

Ogni occorrenza contata da n_U, |U|=3, rappresenta un membro U∪{z_i},
con un punto esterno z_i. Per U uguali e occorrenze distinte, i z_i devono essere
distinti, perché F è semplice. Sia H_y la famiglia delle parti esterne dei
residui con traccia{y}; |H_y|=n_{y}.

Se y∈U, ogni H∈H_y deve contenere z_i. Infatti esiste T∈P10 con
T∩U={y}. Il numero di tali T è5−2−2+[U∈P10], quindi uno oppure due. In assenza
di z_i in H, i tre membri xT, U∪{z_i}, {y}∪H avrebbero tutte le intersezioni
uguali a{y}. Ne seguirebbe un sunflower.

Se n_y≥3, tutti i punti z_i delle triple U che contengono y devono dunque
coincidere. Due punti esterni distinti presenti in tutte le H∈H_y darebbero
codegree almeno3 alla tripla che li unisce a y.

### 5.2 Due triple con coppia comune

Siano U≠V con |U∩V|=2. Se non sono entrambe blocchi P10, allora z_U=z_V.
Esiste infatti un blocco P10 che contiene U∩V e il cui terzo punto evita gli
altri due punti di U∪V: le due sole eccezioni esaurirebbero i due blocchi P10
attraverso quella coppia, rendendo U,V entrambe blocchi. Se z_U≠z_V, quel cono
e i due residui avrebbero nucleo comune U∩V. Contraddizione.

Si prende la chiusura transitiva di queste uguaglianze e di quelle del §5.1.
Una classe così ottenuta deve rappresentare UN punto esterno effettivo. Classi
diverse NON sono presunte distinte: ignorare loro eventuali coincidenze è lecito
per i limiti inferiori che seguono.

### 5.3 Coppie marcate

Se V⊂U è una coppia e un residuo ha traccia V, la sua parte esterna deve
contenere z_U. Basta scegliere l'altro blocco P10 attraverso V, evitando U\V.
Se la parte esterna non contenesse z_U, il cono e i due residui avrebbero tutte
le intersezioni uguali a V.

Il checker non si limita ai nomi delle regole: su P10 ricostruisce i
coni e verifica letteralmente i sunflower che si avrebbero usando due etichette
esterne distinte. Le uguaglianze sono poi propagate con componenti connesse;
il produttore usa invece union-find e la descrizione per intersezioni di triple.

## 6. Quattro certificati locali di impossibilità

Sia C una classe di occorrenze di triple del §5. Essa ha un unico punto
esterno z. Poniamo

    Y_C = unione delle triple della classe,
    P_C = {V⊂S: |V|=2, n_V>0 e V⊂U per qualche U della classe}.

Se C contiene due occorrenze della stessa U, i membri U∪{z} coinciderebbero:
contraddizione alla semplicità. Altrimenti le categorie di membri qui sotto
sono disgiunte, perché hanno traccia su S di taglia rispettivamente3,1,2. Quindi

    d_F(z) ≥ |C| + Σ_(y∈Y_C)n_y + Σ_(V∈P_C)n_V =: D_C,

    d_F(y,z) ≥ #{i∈C:y∈U_i} + [y∈Y_C]n_y
                            + Σ_(V∈P_C,y∈V)n_V =: C_{C,y}.

Non si conta due volte una famiglia di coppie presente sotto più triple: P_C
è un INSIEME di coppie. Il medesimo vale per Y_C. Membri a traccia vuota,
altri membri della stella di x ed eventuali coincidenze con altre classi sono
ignorati: possono soltanto aumentare i gradi reali.

Ogni proiezione viene rifiutata con uno dei seguenti testimoni:

* **P:** B_y>6, contro il lemma del §4;
* **S:** due occorrenze della stessa tripla hanno lo stesso z;
* **D:** D_C>20, contro il cap universale del grado;
* **C:** C_{C,y}>6, contro il cap di codegree di coppia.

I due certificati compressi danno la seguente copertura completa.

| Profilo | P: troppe tracce-pair | S: stessa quadrupla | D: grado esterno>20 | C: codegree>6 | Aperte |
|---|---:|---:|---:|---:|---:|
| tutti15 |4.666|1.630|10.977|30|0|
| un14/cinque15 |145|90|711|0|0|
| Totale |4.811|1.720|11.688|30|0|

Nei testimoni D, il grado forzato è27–41 nel primo profilo e23–41 nel secondo;
nei30 testimoni C il codegree forzato è esattamente7. Le prime esclusioni P
richiedono7–10 tracce-pair, oppure7–8 nel secondo profilo.

Una famiglia ipotetica determina
una delle18.249 proiezioni. Le relazioni del §5 valgono per i suoi punti esterni
reali. Il testimone associato alla proiezione viola perciò un vincolo necessario
della famiglia. Questo esclude tutte le famiglie nelle ipotesi del nucleo,
indipendentemente dalla cardinalità o dal supporto esterno. □

