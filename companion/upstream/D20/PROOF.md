# Exclusion of maximum degree twenty

Lavoriamo con una famiglia finita semplice di quadruple senza tre-sunflower, compreso il nucleo vuoto. Scriviamo N[R] per il vicinato chiuso di un membro e mu per il minimo di |N[R]|. Le premesse sono la classificazione universale R16 e la sua massimalità per i link alti, l'ostruzione C5 separata e le precedenti riduzioni di bootstrap e di grado, nell'ordine aciclico descritto dal paper. H27 si applica soltanto a famiglie intersecanti. Le premesse e i rispettivi testi sono indicati nella [mappa delle dipendenze](../../../proof/DEPENDENCIES.md), alla voce «Ordinary premises and source replacements».

## 1. Normalizzazione e modello necessario

Scegliamo x=22 e

    Y={0,…,5}, Z={6,…,11}, W={12,…,21}.

La P10 canonica è

    012 015 023 034 045 124 134 135 235 245.

Il link di x consiste in questa P10 suY e nella sua traslazione di6 suZ.
I20 membri x∪T sono fissati. Il supporto di F69 è al massimo23; le dieci etichette
W possono includere punti inutilizzati. Non si suppone che il supporto sia23.
Si scelgono49 residui fra TUTTE le C(22,4)=7.315 quadruple che evitano x.

Le variabili z_Q hanno intervallo[0,1]. Per ogni punto diverso da x,
un selettore sceglie un unico grado: sui dodici vicini il minimo è5, perché sono
presenti già cinque coni; sugli altri punti si ammette0 oppure4,…,20. Il limite
inferiore16 sul supporto dà al massimo sette etichette inutilizzate. Il programma
non fissa artificialmente i punti esterni a grado positivo.

### 1.1 Tracce, ancore e gradi condivisi

Su un'ancora ordinata R, siano p le sei tracce esatte
pair, t_i la traccia tripla che omette il punto i, e s_i le quattro singleton.
Le identità sono

    d_i=1+s_i+Σ_{j≠i}p_ij+Σ_h t_h−t_i,
    |N[R]|=1+Σp+Σt+Σs.

Si enumerano p_ij∈{0,1,2,3}, t_i∈{0,1}, s_i∈{0,…,10}. Si applicano TUTTI i
vincoli del predicato importato a42, incluse R42.7/N42.7, firme alte e di I8/I9/I10,
identificazioni delle estensioni, margine Σp+Σt e le somme minime20/52.
Ogni ancora sceglie una combinazione convessa delle righe possibili.

Le tracce sono legate alle STESSE z_Q in tutte le ancore, e il grado dello stesso
punto è legato agli STESSI selettori. I contributi dei20 membri prescritti sono
costanti sottratte dal membro destro. Ogni famiglia vera produce selettori0/1 e
una riga vera in ciascuna ancora; ammettere frazioni allarga il dominio.
Non è richiesto il converso: una soluzione del modello può non essere una famiglia.

Sono necessari i cap20/6/2 sulle presenze di punti/coppie/triple. Per ogni
membro R prescritto oppure marcato,

    Σ_{Q residuo, Q∩R=∅} z_Q ≤27−#{T prescritto:T∩R=∅}.

I membri disgiunti daR sono intersecanti: due di essi disgiunti fra loro darebbero
conR un sunflower vuoto. È precisamente l'ipotesi richiesta da H27.
Una quadrupla è posta a zero soltanto quando completa letteralmente un sunflower
con due membri selezionati, oppure quando viola una premessa già dimostrata dello
stadio. Una marcatura z_M=1 non presuppone altre marcature.

### 1.2 Il vincolo C5 si usa PRIMA dello svuotamento

Per un vicino y in una componente S=Y oZ, sia

    I_y=#{Q∈F:y∈Q⊆S}.

Togliere questi membri dal link di y lascia l'intero cono x+C5 sui sei punti
{x}∪(S\{y}) e nessun altro membro interno a quei sei punti. Non può restare una
famiglia di almeno16 triple: scegliendone16 che includano i cinque coni si viola
l'ostruzione universale importata. Dunque

    d_F(y)−I_y≤15.

Questa disuguaglianza è inserita nel primo modello con I_y ancora variabile.
Non si usa il cap15 dei vicini prima di aver dimostrato I_y=0.

Il modello di maggiorazione NON impone Σz_Q=49. Una candidata F69 lo
soddisferebbe comunque; maggiorare il rilassamento strettamente sotto49 è sufficiente.
Le capacità globali utilizzate restano esplicitamente quelle di una candidata F69.

## 2. Un certificato esclude tutti i30 interni

Si marca M={0,1,2,3}, lasciando liberi tutti gli altri interni. Il sistema
I00 ha317.989 variabili,1.839 disequazioni superiori e1.164 uguaglianze. Il certificato
verificato dà

    Σ_Q z_Q ≤9733/200=48,665<49.

Il margine è67/200. Il solver aveva restituito numericamente47,6: NON sostituiamo
quel valore al limite effettivamente certificato, che paga i residui dei box.

I60 automorfismi P10 agiscono transitivamente sulle sue
15 quadruple. Lo scambio delle due componenti conserva l'intera stella di20 membri.
L'orbita del marcatore copre quindi TUTTI i30 interni suY oppureZ. Una famiglia
con un interno può essere rinominata, insieme a tutti i suoi membri e punti,
nel casoI00. Non si impone che il completamento sia simmetrico. Entrambi gli
interni sono dunque vuoti.

Il limite ereditario diventa d(y)≤15 per tutti i dodici vicini.
Le276 incidenze di F69 danno ora

    D(W)=Σ_{w∈W}d(w) ≥276−20−12·15=76.

Questo vincolo entra soltanto nello stadio successivo.

Se una singleton di un vicino su un'ancora CENTRALE è≥8, B4 rende intersecante
il suo complemento K. Esso contiene tutti i cinque coni C5. Ogni ulteriore tripla
che evita x deve coprire il ciclo con tre punti e sarebbe interna alla componente,
appena esclusa. Pertanto k=5. Questo confinamento NON viene imposto alla generica
ancora marcata, che potrebbe non contenere x.

Le righe possibili di ciascuna ancora centrale passano da17.289 a928 dopo
lo svuotamento. Il rilassamento non marcato con queste premesse è ancora fattibile
numericamente a52 residui. Non è una refutazione e non è una famiglia effettiva.

## 3. Sei certificati impongono almeno due punti esterni per residuo

Si considerano tutte le quadruple non interne che usano zero oppure
un puntoW. Il gruppo è il prodotto dei due gruppi P10 e delle permutazioni diW,
con lo scambio delle componenti. Le sue sei orbite sono:

| Certificato | Marcatore | Taglia dell'orbita | κ(M) | Esito esatto |
|---|---|---:|---:|---:|
|E00|0126|120|5|gap −13/250|
|E01|012·12|200|10|residui≤48003/1000<49|
|E02|0136|120|6|gap −1463/1000|
|E03|013·12|200|11|gap −1261/125000|
|E04|0167|225|4|gap −59/125|
|E05M|016·12|1.800|7|gap −28827/500000|

Qui «012·12» indica {0,1,2,12}, non una concatenazione ambigua di etichette.
κ(M) conta i20 coni disgiunti dal membro marcato. Un gap negativo è una
contraddizione aritmetica con correzione dei box, NON una cardinalità negativa.

Le taglie sommano

    C(12,4)−2C(6,4)+10C(12,3)=465+2200=2.665.

Il verificatore classifica TUTTE le7.315 quadruple mediante firme canoniche dei
sottoinsiemi delle due componenti e numero di puntiW. Il produttore, invece,
espande direttamente l'orbita di ogni marcatore. Le partizioni coincidono.

Il marcatoreE05 lasciava numericamente51 residui nel modello delle sole
ancore centrali. Per E05M si impongono anche le14 tracce COMPLETE del membro
{0,1,6,12}, che deve essere un'ancora vera con |N[M]|≥42. Il suo dominio contiene
4.813 righe. Questo raccordo, alle stesse z_Q e ai medesimi gradi globali,
fornisce la refutazione; il confinamento C5 delle ancore centrali non è imposto
impropriamente aM. Gli altri cinque certificati non richiedono tale estensione.

Ogni residuo di una candidata F69 deve quindi usare almeno due
puntiW, ossia incontrare Y∪Z in al massimo due punti. In particolare D(W)≥98.
La conclusione è successiva ai sei certificati, non una loro premessa nascosta.

## 4. Lemma ordinario: un membro misto copre tutti i residui con tre categorie

### 4.1 La copertura

Il seguente argomento non usa μ42, H27 o il numero dei puntiW.
Assumiamo soltanto la stella P10⊔P10 completa e che ogni residuo abbia al massimo
due punti in S=Y∪Z. Supponiamo presente

    M={y,z,a,b},       y∈Y, z∈Z, a,b∈W, a≠b.

Per ogni altro residuo Q vale

    {y,z}⊆Q  oppure  Q∩{a,b}≠∅.                              (COV)

Per provarlo, supponiamo Q∩{a,b}=∅ e poniamo K=Q∩{y,z}. Se K={y,z}, la prima
alternativa è già vera. Restano due casi.

**Caso K=∅.** TraY,Z esiste una componente che contiene al massimo un punto diQ,
poiché |Q∩S|≤2. In quella P10 scegliamo un bloccoT che evita il punto distinto
marcato y oppurez e l'eventuale punto diQ. Una P10 ha5 blocchi attraverso ogni
punto e2 attraverso ogni coppia: esistono2 blocchi che evitano due punti distinti,
e5 se basta evitarne uno. Il cono xT è disgiunto sia daM sia daQ; M eQ sono già
disgiunti. I tre membri distinti formano un sunflower vuoto: impossibile.

**Caso K={y}**, simmetrico a K={z}. Nella P10 suY scegliamo T contenentey ed evitando
l'eventuale altro punto diQ suY. Questo è possibile: ci sono5 blocchi attraversoy,
oppure5−2=3 dopo aver vietato un secondo punto. Allora

    xT∩M=xT∩Q=M∩Q={y},

un sunflower. Il cono è distinto dai due residui perché contiene x; Q≠M perché
Q evita a,b. Questo conclude(COV), compresi i nuclei vuoti e singleton.

### 4.2 Le capacità danno44, non46

Siano A i residui contenenti{y,z}, B quelli contenentia e C quelli
contenentib. La(COV) dice che tutti i residui appartengono ad A∪B∪C.
Nessun membro della stella di x appartiene a queste categorie: le componenti
sono disgiunte, e a,b sono esterni. Perciò

    |A|≤d(y,z)≤6,             |B|≤d(a)≤20,             |C|≤d(b)≤20.

Il membro M appartiene a TUTTE e tre le categorie. Nella somma |A|+|B|+|C| è
contato tre volte, mentre nell'unione una volta. Sottraendo almeno quel doppio
conteggio, ed eventualmente ignorando altri sovrapposti,

    numero dei residui ≤6+20+20−2=44.

Quindi |F|≤20+44=64. È una dimostrazione ordinaria, non la trasformazione di un
output del solver in teorema. Non si rivendica che64 sia raggiunto o ottimale.

La candidata richiede49 residui. Dunque non può contenere
alcun membro misto M. Un trasporto per automorfismi porta qualunque tale membro
in{0,6,12,13}, ma la prova precedente già tratta direttamente y,z,a,b arbitrari.

### 4.3 Forma parametrica per P9/P10

La medesima prova è valida per H1⊔H2, con ciascuna componente uguale aP9
oP10. Infatti le sole proprietà della componente usate nella(COV) sono:

- esiste un blocco che evita qualunque coppia di punti;
- esiste un blocco contenente un punto e non contenente un secondo punto distinto.

Per P10 i numeri sono rispettivamente2 e3. Togliere un blocco lascia almeno1 e2,
perciò la P9 conserva entrambe le proprietà, compresi i punti del blocco omesso.
La codegree della coppia interna mista resta≤6; se i gradi dei punti sono≤D,
lo stesso membro marcato contato tre volte dà

    r≤6+D+D−2=2D+4,        |F|≤d+2D+4.

A F69, nel massimo19, questo darebbe r≤42 contro50; nel massimo18, r≤40 contro51,
SE la geometria con almeno due punti esterni per residuo sarà stata dimostrata.
Non si dichiara qui acquisita quella geometria per gli altri gradi.

In assenza di residui misti, una coppia nella stessa componente
incontra al massimo8 blocchi anche nella P9, perché la cancellazione non può
aggiungerne. Ne segue

    (d−8)r≤27d.

Con il cap universaleD=20, unendo i due casi si ottengono i cap GEOMETRICI65
perd=20o19 e66 perd=18. Non sono nuovi cap globali per M(4,3): conservano sempre
la premessa |Q∩(Y∪Z)|≤2 per ogni residuo. Questa proposizione non usa μ42 o
un limite sul numero dei punti esterni.

### 4.4 Verifiche finite del lemma e confine essenziale

Il checker tratta P10⊔P10, P10⊔P9 eP9⊔P9, e ciascuna
 delle36 scelte dei due punti interni marcati per radice. Per ogni scelta esamina
316 tracce canoniche: zero/uno/due puntiS, zero/uno/due fra i due punti esterni
marcati, e i restanti punti esterni rappresentati da etichette nuove.
Sono34.128 controlli di traccia; le8.424 tracce fuori dalla(COV) hanno tutte un
cono che forma letteralmente il sunflower. Non si tratta di un campione del
supporto: le intersezioni con M e i coni dipendono soltanto da questa traccia.

La famiglia costituita dai20 coni, da
M={0,6,12,13} e daQ={0,1,3,4} è senza sunflower: tutte le1.540 terne sono controllate.
Q sfugge alle tre categorie, ma usa QUATTRO punti diS. Essa verifica perché
l'ipotesi «al massimo due puntiS» non può essere soppressa. Non ha μ≥42 e non è un
controesempio alla chiusura F69.

E06 fornisce anche una refutazione
aritmetica del marcatore{0,6,12,13} dopo lo stadio del §3. Il suo gap è−2/25.
È rigiocata, con confronto letterale di20.047 variabili,1.841 disequazioni e864
uguaglianze. Non è necessaria alla dimostrazione, sostituita dai §§4.1–4.2.
La dimostrazione usa quindi SETTE certificati lineari portanti; E06 è un
certificato supplementare, non un'ulteriore dipendenza lineare dell'esclusione.

## 5. Chiusura mediante il bilancio delle disgiunzioni

Ogni residuo usa almeno due puntiW e non ha la coppia interna mista.
Restano soltanto queste tre forme:

| Forma del residuo | Numero di quadruple nell'universo | Coni disgiunti κ(Q) |
|---|---:|---:|
|Due punti nella stessa P10, due puntiW|2·C(6,2)·C(10,2)=1.350|12|
|Un puntoS, tre puntiW|12·C(10,3)=1.440|15|
|Quattro puntiW|C(10,4)=210|20|

Per una coppia nella stessa P10, i blocchi che la incontrano sono5+5−2=8;
per un singolo punto sono5. I conti riguardano tutti i20 coni delle due componenti.
Sono3.000 colonne terminali. Non si dichiara che siano simultaneamente realizzabili.

La partizione completa verifica

    7.315−30−2.665−1.620=3.000.

Le1.620 quadruple eliminate dal lemma sono le C(6,1)² C(10,2) miste. Le codegree
non vengono usate per respingere invece le1.350 coppie nella STESSA componente:
quelle rimangono ammesse perché non serve eliminarle.

Contiamo le coppie disgiunte (R,Q), con R prescritto e Q residuo.
Ciascuno dei49 residui è disgiunto da almeno12 coni, quindi ne occorrono almeno588.
Per ciascuno dei20 coni, H27 permette al massimo27 membri disgiunti. Si avrebbe

    12·49=588 ≤20·27=540,

impossibile. Questo esclude TUTTO il massimo20 di F69.

Sotto la sola geometria del §4 e H27,
se è presente un residuo misto vale|F|≤64; se non è presente,12r≤540 dà r≤45,
quindi|F|≤65. Questo cap65 CONSERVA l'ipotesi che ogni residuo usi al massimo due
punti del supporto del link. Non è un nuovo limite globale M(4,3)≤65.

Questo blocco esclude il massimo grado20 per una famiglia di69 membri.
Le esclusioni degli altri gradi sono nei blocchi separati indicati nella
[mappa delle dipendenze](../../../proof/DEPENDENCIES.md), alla voce
«Preliminary finite blocks».

## 6. Certificazione aritmetica e validità dei rifiuti

Ogni sistema è Az≤b, Ez=f, l≤z≤u, con coefficienti interi. Il certificato
fornisce y≥0 eη liberi, tutti interi, e una scala positiva t. Posto q=Aᵀy+Eᵀη,
H=y·b+η·f, si controlla

    H−Σ_j min(l_jq_j,u_jq_j)<0

per l'incompatibilità. Per maggiorare l'obiettivo c·z si pone r=tc−q e si controlla

    H+Σ_j max(l_jr_j,u_jr_j)<49t.

I coefficienti negativi non sono ignorati: il costo del relativo box è pagato
esattamente. Una virgola mobile interviene soltanto nella ricerca dei moltiplicatori;
la decisione finale è fra interi Python.

`model.py` e `audit.py` ricostruiscono separatamente le matrici, i box,
le variabili e i domini completi. Il primo usa maschere e p-prima-di-t, il secondo
insiemi, t-prima-di-p e il predicato a partizioni `audit43.py`. Il confronto è
LETTERALE su ogni oggetto, non soltanto su un hash. La necessità matematica del
modello rimane quella dimostrata sopra e importata per i predicati.

Una famiglia reale produce uno dei marcatori
coperti e una soluzione del modello necessario. Il certificato esclude quel
modello oppure maggiora i residui sotto49. Dopo le sei esclusioni esterne,
l'argomento ordinario copre tutti i residui misti; il doppio conteggio termina.
Non si promuove un pattern o un campione a teorema.

