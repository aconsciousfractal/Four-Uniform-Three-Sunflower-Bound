# The mu42 bootstrap

Work with a finite simple four-uniform family containing no three-sunflower, including empty core. Write N[R] for its closed member neighbourhood and mu for the minimum of |N[R]|. The applicable universal R16 classification, maximality, separate C5 obstruction and bootstrap/degree premises are specified in the acyclic [mathematical dependency map](../../../proof/DEPENDENCIES.md). H27 is applied only to intersecting families. The proof below gives the exact trace, point-identification, symmetry, coverage and pruning arguments.

## 1. Ricostruzione del dominio locale alla soglia corretta

Su un'ancora ordinata R={r0,r1,r2,r3}, la riga è (p,t,s): sei tracce
esatte di coppia p_ij in ordine lessicografico, quattro tracce triple t_i che
omettono ri, quattro singleton s_i. Poniamo

    k_i=1+Σ_(j≠i)p_ij+Σ_h t_h−t_i,
    d_i=k_i+s_i,                 |N[R]|=1+Σp+Σt+Σs.

Il dominio usa p_ij∈{0,1,2,3}, t_i∈{0,1}, s_i∈{0,…,10}, d_i≤20,
|N[R]|≥42 e i seguenti vincoli universali ereditati, senza rafforzamenti a43.

Per d_i=17 le coppie(s_i,k_i) sono(7,10),(8,9),(9,8),(10,7); per18 sono
(8,10),(9,9),(10,8); per19 sono(9,10),(10,9); per20 sono(10,10).
Se s_i≥8, K_i è intersecante: k_i≤10, somma delle tre p incidenti≤6 e si
applicano le firme radicate dei modelli di taglia8/9/10, rispettivamente21/6/1.
Le tracce triple impongono le capacità di coppia pertinenti. Per q singleton<8,

    Σp+Σt≤(12,14,17,19,22)[q].

Sono mantenute le identificazioni e distinzioni delle estensioni esterne del
§D dei fondamenti e il cap di due punti di grado≥19 in un membro.
Non si richiede una firma I7 quando k=7: questo renderebbe il dominio più stretto,
ma non è necessario al nuovo risultato.

Ogni ancora vera può essere rinominata ordinando i suoi
gradi. Le procedure esaminano tutti i valori nei suddetti intervalli. La prima
sceglie p prima di t, costruisce firme con insiemi e usa unione di equivalenze;
la seconda sceglie t prima di p, costruisce firme con maschere ed esamina tutte
le15 partizioni dei quattro indici. Ordinare un'ancora non impone simmetrie aF.

Le liste complete coincidono letteralmente:

    980.624 righe, 1.233 profili di grado;
    minimo grado2, somma minima di coppia20, somma minima di membro46;
    reciproco massimo2/3, reciproco minimo37/170.

Ogni punto/coppia usato appartiene a un'ancora; i primi minimi2/20 possono quindi
entrare nel bootstrap. Il solo massimo2/3 darebbe supporto≤46 a F69, non23.
I conteggi sono condizioni numeriche necessarie, NON famiglie realizzate.

## 2. Primo bootstrap: non perdere le correlazioni fra le ancore

### 2.1 Componenti isolate e tutti gli interni

Una singleton di taglia10 o9 fornisce una
componente M=P10 oppure P9 del link L_x su sei punti S. Nel caso P9 il blocco
omesso non può essere presente: sarebbe disgiunto dall'ancora originaria e farebbe
salire la singleton a10. Tutti gli altri membri del link evitano S.
Per ogni componente consideriamo tutte le quadruple interne I=F∩C(S,4).

Delle2^15 scelte,292 sono compatibili per P10 e373 per P9. Le due
procedure confrontano l'intera copertura. Non si assume I vuoto.

Per k≤5 possiamo rilassare il valore del centro sostituendolo con5 nelle ancore
centrali x∪T. Aumentano solo la singleton del centro, il suo grado e |N[R]|;
il centro resta sotto16 e la sua singleton sotto8. Non si attraversa una soglia
di classificazione alta. Tutti i vincoli diventano più deboli o invariati.
Questa monotonia NON è affermata per un passaggio generico a k=8.

### 2.2 Confinamento del complemento di un vicino

Per y∈S, il link prescritto ha una stella completa x+C5 oppure x+P5,
oltre alle triple degli interni che contengono y. P5 indica il cammino di quattro
archi su cinque vertici, non il ciclo. Indichiamo con I_y il numero degli interni
attraverso y. Per C5, cancellare queste I_y triple dal link lascia esattamente il
cono sul suo supporto di sei punti. L'ostruzione importata implica

    d_F(y)−I_y≤15.

Se s_y≥8, B4 rende intersecante la parte K_y; anche per d_F(y)≥17 la
separazione E17/E18/C1 fornisce questo controllo. Tutti i membri interni
prescritti sono nella stessa parte K_y. Per P8/P9/P10 nella parte opposta,
l'isolamento lo impone; per Q8 il suo nucleo di cinque punti è evitato dalla
stella prescritta, e ogni tripla della Q8 usa almeno due punti di quel nucleo.
Una tripla completamente interna non può quindi appartenere alla parte opposta.
Non si suppongono esterne tutte le foglie Q8.

Ogni nuova tripla di K_y che evita x deve coprire la stella. Nel C5 servono tre
vertici: l'aggiunta sarebbe interna ed è già assegnata. Nel P5, l'unica possibile
aggiunta esterna usa la sua unica copertura di due vertici, più un punto esterno.
La codegree2 di quella coppia nel link permette al massimo due aggiunte. Le due
etichette ausiliarie usate nel controllo sono rappresentanti distinti, non un
limite al supporto globale. Se |K_y|≥8, la classificazione confina di nuovo tutto
ai sei punti: Q8 non contiene P5 in un link di punto, P8/P9/P10 usano sei punti
già occupati dalla stella. Si ricalcola anche la compatibilità con gli interni.

Quando K_y non è controllata non le si impone l'intersecanza: si richiede soltanto
che contenga i membri prescritti che incontrano l'ancora pertinente.

### 2.3 Le famiglie esterne devono essere le stesse attraverso tutte le ancore

Posto U=S∪{x}, definiamo H_y={T:T∩U=∅, {y}∪T∈F}. Per y≠z, un
blocco di M evita entrambi. Due triple disgiunte di H_y,H_z, con quel cono,
formerebbero un sunflower vuoto. Le H_y sono quindi cross-intersecanti. Una
tripla può appartenere ad al massimo due H_y, per il cap della sua codegree.

Una P10 ha esattamente dieci trasversali triple; P9 ne ha undici;
nessuna ha una trasversale di due punti. Questo esclude anche trasversali triple
che usino punti esterni al loro supporto. Pertanto

    Σ_y |H_y|≤20 se una H_y ha10 membri;
    Σ_y |H_y|≤22 se una H_y ha9 membri.

Se una singleton centrale di y ha taglia10/9, coincide con H_y. Se ha taglia8,
sono certamente esterne soltanto le sei triple del nucleo nel possibile Q8:
si usa |H_y|≥6, NON8. Per singleton≤7 si usa il solo limite inferiore0.

Il primo controllo sostituisce le alternative di ogni ancora con minimi
coordinata per coordinata: questo allarga il problema ma perde correlazioni.
Restano16 stati P10 e24 P9. Ora conserviamo, per ciascuna riga, l'INTERA tripla
dei limiti inferiori in{0,6,9,10}, e raccordiamo gli stessi sei gradi globali.

In una famiglia vera, per ogni y
si prenda il massimo dei limiti richiesti dalle ancore scelte. Il vettore h
appartiene a{0,6,9,10}^6. Se contiene10 la somma è≤20; se contiene9 ma non10,
la somma è≤22. Ogni completamento vero determina dunque uno dei256 vettori h
rimasti. Non si impone che i valori h siano le cardinalità ESATTE delle H_y.
Ogni ancora deve poter scegliere una riga i cui tre requisiti siano≤h.

Il produttore interseca insiemi di possibilità rappresentati da bitset;
l'auditor prova esplicitamente tutti i256 vettori. Confrontano inoltre tutte
le alternative locali conservate nei casi residui:

| Componente, k≤5 | Interni | Righe centrali | Gradi raccordati prima del cap H | Dopo il cap scalare | Dopo il raccordo congiunto |
|---|---:|---:|---:|---:|---:|
| P10 |292|61.620|341|16|0|
| P9  |373|39.012|666|24|0|

Sono4.096+6.144 controlli finali di stato/h. Lo zero copre tutti i completamenti
nel dominio necessario. **Si ottengono R42.6 e N42.6**, senza usare R43/N43.
I JSON scalari con stato OPEN sono volutamente conservati: sono la tappa
precedente al raccordo, non il verdetto finale.

## 3. Il passo k=6:92 sistemi locali con aritmetica esatta

### 3.1 Un modello di41 tracce, senza fissare l'esterno

Assegniamo un interno I completo, con presenze e
assenze. Per ogni ∅≠V⊆S, |V|≤3, sia n_V il numero dei membri che evitano x,
non sono interni e hanno traccia esattamente V suS. Le41 coordinate comprendono
6 singleton,15 coppie e20 triple. Il numero dei membri con traccia vuota e il
numero dei punti esterni NON vengono limitati. Non compare H27 nel sistema.

Il bound di ogni coordinata n_V è la capacità20/6/2 meno i membri già prescritti
che contengono V. Se due membri prescritti più quella traccia formano un
sunflower, n_V è posto a zero: i due membri sono interamente in S∪{x}, perciò
l'esito non dipende dalle etichette esterne della quadrupla.

Ogni vicino ha un unico selettore del suo grado; ogni ancora x∪T sceglie una
combinazione convessa di righe complete. Le tracce residue di tutte le ancore
sono le somme degli STESSI n_V. I gradi sono collegati agli STESSI selettori.
Gli interni assegnati forniscono contributi costanti. Una famiglia reale
produce selettori0/1; ammettere frazioni può solo allargare il dominio.

Si applica il confinamento del §2.2. Per P5, E17/E18/C1 richiedono anche almeno
1,4,5,6 interni attraverso y quando d(y)=17,18,19,20 rispettivamente. A17,
fra almeno tre aggiunte alla stella P5 soltanto due possono essere esterne;
a18 e oltre l'intera componente è interna sui sei punti già occupati.
Non si trasforma una I7 arbitraria in P8 o Q8.

### 3.2 Ordine e copertura dei certificati

I292 interni P10 hanno13 orbite sotto60 automorfismi. I373 interni P9
hanno79 orbite sotto6 automorfismi. Il produttore usa augmentazione dei membri;
il secondo catalogo controlla tutte le2^15 maschere e tutte le720 permutazioni.
Le coperture complete coincidono. Le orbite rinominano l'intera famiglia
con il suo interno, non impongono simmetrie al completamento.

Ordine obbligatorio:

1. P10 con esattamente6 membri del link fuoriS; sono disponibili soltanto r10=r9=6.
2. Dopo aver escluso questi13 casi, R42.7 è acquisito.
3. P9 con esattamente6 membri fuoriS; si usa r10=7 e ancora r9=6.
4. Dopo i79 casi segue N42.7.

Tutti i92 sistemi sono incompatibili. Novanta hanno già un'ancora senza
righe, quindi l'equazione0=1. Le sole due combinazioni nontriviali sono:

| Caso | Interno P9 | Variabili | Uguaglianze | Uguaglianze usate | Minimo del membro sinistro | Membro destro | Gap |
|---|---|---:|---:|---:|---:|---:|---:|
| P9_000 |vuoto|242|405|12|−18|−71|−53|
| P9_004 |{0345}|327|405|10|−10|−210|−200|

Queste sono combinazioni intere, alla scala1000: imporrebbero rispettivamente
−18≤−71 e−10≤−210. Il minimo sugli intervalli delle variabili è pagato
integralmente. Non si arrotonda un obiettivo numerico vicino a una soglia.

Per Ez=f e l≤z≤u, il certificato fornisce interi η. Si calcolano
q=Eᵀη, H=η·f, L=Σ_j min(l_j q_j,u_j q_j). Se H−L<0, una soluzione imporrebbe
L≤q·z=H<L. Il checker ricostruisce matrici, membri destri, intervalli e domini;
confronta ogni coefficiente con il produttore prima di verificare il certificato.
Il solver è servito a cercare η, non decide l'esclusione.

Ogni interno reale è coperto e induce una soluzione di uno dei
sistemi refutati. I casi k≤5 erano esclusi al §2. Pertanto il Teorema A è provato:

    μ≥42 ⇒ s=9,10 richiede k≥7.

## 4. Il punto di grado2: un'ostruzione ordinaria tramite tre Q8

### 4.1 Il dominio grezzo isola il caso

Tra TUTTE le980.624 righe iniziali vi è un'unica riga con un grado2:

    p=(0,0,0,3,3,3), t=(1,0,0,0), s=(1,10,10,10), d=(2,18,18,18).

Un punto x di grado2 avrebbe quindi due membri x∪A e x∪B, dove A,B sono triple
disgiunte, e tutti i sei punti di A∪B hanno grado18. Applicare la stessa riga
all'altro membro è necessario; non basta controllare una sola ancora.

Una famiglia senza3-sunflower NON può avere
un punto x di grado2, con membri x∪A,x∪B, A∩B=∅, se tutti i sei punti di
A∪B hanno grado18. Questo lemma non assume μ42, H27 o |F|=69.

### 4.2 Le tre Q8 dei punti di A devono condividere il triangolo

Nel link di ogni a∈A, il punto x ha grado1. Per E18, quel link deve
quindi essere P10⊔Q8 e x è una foglia della Q8. I due hub sono A\{a}.
Sia C_a il triangolo della Q8 e y_a l'altra foglia. Il membro A∪{y_a} è presente.
La codegree2 della tripla A impone che tutti gli y_a siano lo stesso punto y.

Per due distinti a,b∈A, i cinque membri contenenti entrambi sono xA,yA e i tre
membri {a,b}∪E, E∈C(C_a,2). La stessa descrizione nel link di b forza
C(C_a,2)=C(C_b,2), dunque C_a=C_b=:C. Le tre coppie determinano il triangolo,
non soltanto la sua cardinalità.

Sono prescritti xA,yA e tutti i nove membri

    E_A∪E_C,       E_A∈C(A,2), E_C∈C(C,2).

I punti A,C,x,y sono distinti a gruppi; per ogni a∈A la seconda componente
H_a=P10 del suo link evita U=A∪C∪{x,y}. Inoltre d_F(a,y)=1.

y non appartiene aB. Altrimenti avrebbe grado18 e il suo link
conterrebbe A con tutti e tre i punti di A di grado1 nel link. Nessuno dei
modelli E18 contiene una simile tripla: le P10/P9/P8 non hanno punti di
grado1; Q8 ha due foglie e ogni sua tripla ne contiene al massimo una.

### 4.3 Se B evita C, tre P10 condividono una trasversale

Supponiamo B∩C=∅. B evita allora tuttoU. Per a∈A e T∈H_a,
se B∩T=∅ i tre membri

    xB,      aT,      (A\{a})∪E_C

sarebbero disgiunti, scegliendo una qualunque coppia E_C⊂C. Quindi B incontra
ogni tripla di H_a: è una trasversale di tre punti della P10.

Le sole trasversali triple di P10 sono i suoi dieci blocchi. Infatti essa
contiene esattamente una tripla per ciascuna coppia di triple complementari
sui sei punti; una tripla assente non incontra il proprio complemento
presente. Una trasversale che usa un punto esterno richiederebbe una copertura
di al più due punti, impossibile. Dunque B∈H_a per ogni a∈A. I tre membri aB
formano un sunflower con nucleoB: contraddizione.

### 4.4 Se B incontra C, è precisamente C

Sia c∈B∩C. Nel link L_c sono prescritte le sei triple

    {t}∪E_A,          t∈C\{c}, E_A∈C(A,2).

Sono pairwise intersecanti, quindi occupano la stessa componente E18. Per ogni
a∈A, le quattro triple attraverso a danno un cicloC4 nel suo link grafico.
Nessun sottosistema di P10 ha tale link: ogni link di P10 è C5, che non
contiene C4. La componente è dunque Q8. Solo i tre punti del triangolo Q8
hanno un C4 nel link; i due hub hanno K3⊔P3 e le foglie un arco. Il triangolo
èA e gli hub sonoC\{c}.

x ha grado1 in L_c e deve essere una foglia di questa Q8, non un punto della
P10. Il suo membro x∪(B\{c}) impone B\{c}=C\{c}, quindi B=C.
Per ogni c∈C la componente P10 H_c evita A∪C.

Per a∈A,c∈C e triple T∈H_a,V∈H_c, se T,V fossero disgiunte, i tre membri

    aT,       cV,       (A\{a})∪(C\{c})

sarebbero disgiunti. H_a e H_c sono quindi cross-intersecanti. Ogni tripla
di H_c è una trasversale tripla di H_a, dunque H_c⊆H_a; entrambe hanno dieci
membri, perciò coincidono. Fissato c, tutte le tre H_a coincidono. Una loro
tripla T dà nuovamente i tre membri aT con nucleoT. Contraddizione. □

Q8 ha gradi5 sui due hub,4 sui tre punti del triangolo,1 sulle due
foglie. Questi ruoli non vengono scambiati. Il controllo ricostruisce tutti
i210 Q8 etichettati su sette punti; soltanto uno contiene il nucleo di sei
triple appena usato con A e gli hub fissati.

### 4.5 Il grado3 e il controllo positivo del confine

Le sole quattro righe grezze con un punto di grado3 hanno
sempre singleton2 su quel punto. Tutte le tre triple del suo link sarebbero
quindi pairwise disgiunte, dando un sunflower con nucleo il punto. Il grado1
non compare nel dominio grezzo. Con il lemma precedente ogni punto usato
ha dunque grado almeno4.

Una famiglia effettiva di13 membri è data dai nove E_A∪E_C e dai
quattro membri xA,yA,xC,yC. È senza sunflower; tutte le286 terne sono
verificate. x,y hanno grado2 e gli altri sei punti grado8. Questo esempio
controlla che NON stiamo affermando l'impossibilità universale del grado2.
Le ipotesi sui sei vicini di grado18 sono essenziali all'argomento qui usato.

## 5. Dominio aggiornato e bilanci di stelle

Il dominio grezzo, filtrato per i nuovi vincoli, dà:

| Stato dei vincoli | Righe | Profili |
|---|---:|---:|
| Nessun rafforzamento R/N |980.624|1.233|
| R42.6 e N42.6 |537.483|1.062|
| R42.7 e N42.7 |292.565|971|
| Inoltre grado usato≥4 |292.560|966|

L'auditor ricostruisce anche direttamente il dominio con r10=r9=7 e lo
confronta con la lista filtrata. Solo cinque righe sono eliminate dal minimo4.
Le somme minime sono20 sulle coppie usate e52 sui membri.
Il massimo reciproco puntuale, dopo il minimo4, è117/272; da solo darebbe
supporto al massimo29 a F69. Occorre un vincolo sulle INTERE stelle.

### 5.1 Mantel: la prova classica e la corretta molteplicità

Il grafo delle disgiunzioni del link
L_v ha d=d_F(v) vertici e non contiene triangoli. Per un suo arco ij,
deg(i)+deg(j)≤d. Sommare sugli archi dàΣ deg(i)^2≤d e, dove e conta gli
archi. Cauchy dàΣ deg(i)^2≥4e²/d. Se e=0 è immediato; altrimenti e≤d²/4,
dunque e≤floor(d²/4). Quindi

    Σ_(R∋v) s_v(R) ≤2 floor(d²/4).

Per d=4 definiamo

    G4(R)=Σ_(v∈R,d(v)=4) (4s_v(R)−8).

Ogni punto4 compare in quattro ancore. Sommando si haΣ_R G4(R)≤0. Questa
non è la falsa affermazione G4(R)≤0 per ogni singola ancora.

### 5.2 Identità dei link alti

Per un'ancoraR definiamo

    B17a=Σ_(d(v)=17) (7[s_v=7]−10[s_v=10]),
    B17b=Σ_(d(v)=17) (8[s_v=8]− 9[s_v=9]),
    B18 =Σ_(d(v)=18) (8[s_v=8]−10[s_v=10]),
    B19 =Σ_(d(v)=19) (9[s_v=9]−10[s_v=10]),

con tutte le somme ristrette a v∈R. Ciascuna ha somma globale zero. Per
P10⊔I7 al grado17 ci sono10 ancore s7 e7 s10; per P9⊔I8,9 ancore s8 e8 s9.
Al grado18 si hanno10 s8 e8 s10 oppure soltanto s9; al grado19,10 s9 e9 s10.
Le parti sono intersecanti e i supporti disgiunti. Non si esclude P10⊔I7.

Poniamo anche

    T16(R)=Σ_(v∈R,d(v)=16) (9[s_v=9]−7[s_v=7]).

Se esiste una singleton9 nel link16, B4 e l'isolamento P9 producono P9⊔I7:
9 ancore hanno s7 e7 s9, con contributo zero. Il blocco omesso P9 non può
stare nella parte vicina perché sarebbe disgiunto dall'ancora. Se non esiste
singleton9, il contributo è nonpositivo. PerciòΣ_R T16(R)≤0.
Questa disuguaglianza non usa un falso limite su D26 e non esclude tutte le R16.

## 6. Un certificato piccolo su tutte le292.560 righe

Sia c(R)=Σ_(v∈R)1/d(v). Il certificato `STAR_CHARGE42.json` contiene
la seguente combinazione di piccoli interi:

    10000 c(R) ≤ 3400 +26 G4(R)
                       −33 B17a(R)−21 B17b(R)−38 B18(R)+9 B19(R)
                       +18 T16(R).                                      (C)

Il checker verifica(C) su TUTTE le292.560 righe, moltiplicando per
lcm(1,…,20)=232.792.560. Ogni operazione decisiva è intera. Il massimo della
carica corretta è28719/85000, con margine minimo rispetto a17/50:

    17/50−28719/85000 =181/85000>0.

Non si rivendica l'ottimalità di queste costanti. Il solver numerico ha soltanto
proposto pesi; la verifica finale non carica SciPy o NumPy.

Sommiamo(C) su tutti i membri. G4 e T16 hanno somme nonpositive
e moltiplicatori26,18 nonnegativi. I quattro B hanno somma zero, perciò i loro
coefficienti possono avere entrambi i segni. Segue

    Σ_R c(R)≤(17/50)|F|.

Ogni punto usato compare in d(v) membri e contribuisce1/d(v) ciascuna volta:
Σ_R c(R)=|suppF|. Il minimo puntuale37/170 dà l'altra disuguaglianza.
Questo è il trasferimento finito/generale: ogni ancora vera appartiene al
dominio e le correzioni si sommano con i segni provati sulle stelle.

Il margine calcolato consentirebbe anche il coefficiente28719/85000 anziché
17/50; per F69 dà lo stesso limite intero23. Manteniamo nel teorema la costante
più semplice17/50, senza affermarla ottimale.

Per F69, μ≥69−27=42. Pertanto

    2553/170≤|suppF69|≤1173/50,

ossia16≤|suppF69|≤23. Non si assume che tutte le righe del dominio siano
simultaneamente realizzabili, né che esista una famiglia da69 membri.

