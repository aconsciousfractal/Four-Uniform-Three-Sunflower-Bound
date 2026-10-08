# Exclusion of maximum degree nineteen

Work with a finite simple four-uniform family containing no three-sunflower, including empty core. Write N[R] for its closed member neighbourhood and mu for the minimum of |N[R]|. The applicable universal R16 classification, maximality, separate C5 obstruction and bootstrap/degree premises are specified in the acyclic [mathematical dependency map](../../../proof/DEPENDENCIES.md). H27 is applied only to intersecting families. The proof below gives the exact trace, point-identification, symmetry, coverage and pruning arguments.

## 1. Modello necessario a69, non quello della cardinalità precedente

Normalizziamo x=22,Y={0,…,5},Z={6,…,11},W={12,…,21}. SuY fissiamo

    P10=012,015,023,034,045,124,134,135,235,245;

suZ la copia traslata di6 che omette012. I19 coni x∪T sono prescritti. I50 residui sono scelti fra tutte le C(22,4)=7.315 quadruple che evitano x. W contiene dieci ETICHETTE e può includere punti inutilizzati. Il modello conserva tutti i supporti16–23.

Ogni quadrupla residua ha una variabile z_Q∈[0,1]. Ogni punto diverso da x ha un unico selettore di grado: i vicini hanno almeno il loro grado già prescritto (5 oppure4), gli altri grado0 oppure4,…,19. Il cap sul numero di etichette inutilizzate è7. Punti, coppie e triple soddisfano i cap19/6/2, sottraendo i membri prescritti. Le disuguaglianze H27 sono applicate soltanto ad ancore effettive, prescritte o marcate.

Su un'ancora ordinata R, p_ij,t_i,s_i denotano le sei tracce pair, le quattro triple che omettono i, e le quattro singleton. Si impongono

    d_i=1+s_i+Σ_(j≠i)p_ij+Σ_h t_h−t_i,
    |N[R]|=1+Σp+Σt+Σs≥42.

Il dominio completo mantiene i vincoli universali e R42/N42, inclusi i limiti sulle firme e le identificazioni. Per ogni ancora, variabili λ_r scelgono una combinazione convessa delle righe. La somma delle z_Q con una data traccia, più il contributo prescritto, è uguale al conteggio di quella traccia nella combinazione. Tutte le ancore condividono le STESSE z_Q e gli STESSI selettori di grado. Le tracce contenenti x nelle ancore centrali sono già fissate dal link completo.

Una famiglia vera induce selettori interi e una sola riga reale per ancora. Permettere combinazioni frazionarie allarga il problema: non se ne richiede il converso. Le ancore marcate generiche usano tutte le14 tracce e NON ricevono il confinamento della stella centrale. Una quadrupla è vietata soltanto se forma un sunflower letterale con due membri selezionati oppure se contraddice una premessa già stabilita/assegnata del caso.

La maggiorazione non impone Σz_Q=50. Alcuni altri vincoli sono comunque conseguenze dell'ipotesi F69; il limite ottenuto è quindi condizionato a quel bersaglio e non un nuovo cap per famiglie più piccole.

## 2. Completamento interno prima dello svuotamento

Per S=Y oppureZ e y∈S, sia I_y=#{Q∈F:y∈Q⊆S}. SuP10 tutti i sei punti hanno stella C5; suP9 i punti6,7,8 hanno P5 e9,10,11 hanno C5. P5 è un cammino di quattro archi su cinque punti.

Togliendo dal link di un vicino C5 i membri corrispondenti ai suoi I_y interni, si mantiene la stella completa x+C5 e nessun altro membro sui relativi sei punti. L'ostruzione universale dà

    d(y)−I_y≤15.

Questa disuguaglianza vale con I_y ancora variabile. Per i P5 si importano i completamenti E17/E18: I_y≥1,4,5 ai gradi17,18,19. Il caso17 ammette una I7 arbitraria: il cammino ha un'unica copertura di due punti, che permette al massimo due aggiunte esterne. Ai gradi18/19, la componente di taglia≥8 non può essere Q8 e occupa i sei punti già prescritti.

In un'ancora CENTRALE, se s_y≥8, B4 rende intersecante il complemento K_y. Esso contiene tutte le triple prescritte della stella. Una tripla aggiunta che evita x deve coprire i suoi archi. Nel C5 usa tre punti interni; nel P5 può usare la sua unica copertura di due punti più un esterno, al massimo due volte. Perciò

    k_y≤5+I_y per C5;             k_y≤6+I_y per P5.

La versione lineare, prima di assegnare I_y, è

    Σ_r λ_r [s_y(r)≥8] max(0,k_y(r)−b_y) ≤ I_y,
    b_y=5 per C5, 6 per P5.

Per una famiglia effettiva un solo λ vale1, e la disuguaglianza precedente la implica. Sono57 righe condizionali, tre per ciascuna delle19 ancore. Non si presume intersecante K_y quando s_y<8.

Con interni completamente assegnati si restringono i selettori di grado e le righe incompatibili con i valori esatti I_y. Si mantengono le colonne originarie ponendo a zero gli intervalli delle colonne escluse. Tutte le presenze e assenze interne sono fissate; gli interni dell'altra componente restano liberi salvo quando la loro assenza è già dimostrata. H27 su un interno selezionato conta il residuo con la sua variabile: non si sottrae due volte.

## 3. Svuotamento degli interni: cinque più dodici certificati

### 3.1 Prima la P9, lasciando libera la P10

Aut(P9) ha6 elementi. I marcatori I01={6,7,8,9}, I02={6,7,9,10}, I03={6,7,9,11} coprono rispettivamente3,3,6 interni. I limiti esatti sono

    61889/1250,     302811/6250,     6236/125,

tutti inferiori a50. Restano soltanto {u,9,10,11},u=6,7,8. La tripla comune9,10,11 può essere estesa al massimo due volte. Le scelte interne sono quindi sette, con orbite di cardinalità1,3,3 secondo che si scelgano zero,uno,due membri.

J1 assegna l'unico interno{6,9,10,11}, e tutti gli altri interni P9 assenti: residui≤48237/1000<50. J2 assegna due interni{6,9,10,11},{7,9,10,11}, e gli altri assenti: gap esatto−99/125. P10 è ancora libera in entrambi i casi. Sono così escluse tutte le scelte P9 nonvuote.

Ogni trasporto rinomina l'intera famiglia, senza imporre simmetrie al completamento. P9 è vuota in ogni candidata del ramo.

### 3.2 Poi tutti gli interni P10 nonvuoti

Le15 quadruple interne P10 hanno2^15 sottofamiglie. Il controllo dei sunflower con i dieci coni lascia292 possibilità, con distribuzione per cardinalità0,…,5:

    1,15,75,135,60,6.

Sotto i60 automorfismi formano13 orbite. Un algoritmo genera i prefissi ammissibili; l'altro ricostruisce50 pattern proibiti e prova tutte le32.768 maschere. Le intere coperture coincidono. La P9 vuota è invariante sotto questi trasporti.

P01–P12 assegnano tutti i dodici interni P10 nonvuoti con P9 vuota. Tutti sono refutati: due maggiorazioni e dieci incompatibilità. I due limiti sono11533/250 e21659/500, inferiori a50. In P06 eP11 un'ancora ha già dominio vuoto e la contraddizione è0=1. Gli altri certificati sono controllati sulle matrici complete, non soltanto dopo il presolving numerico.

L'interno vuoto non va refutato in questo stadio: è l'unica possibilità rimasta. Entrambe le componenti sono ora vuote. Non è stato necessario che il singolo marcatore P10 iniziale fosse sufficiente: quel modello era rimasto fattibile numericamente a50⅓.

I nove vicini C5 hanno grado≤15, i tre P5≤16. Dal totale276 delle incidenze,

    D(W)≥276−19−9·15−3·16=74.

Questo vincolo è usato soltanto nello stadio esterno. NON si impone D(W)≥100, né che ogni residuo usi già due puntiW: rimarranno effettivamente ammesse60 colonne con un solo puntoW.

## 4. Ventisei marcature esterne: due orbite lasciate ammesse

Sotto Aut(P10)×Aut(P9)×Sym(W), senza scambiare componenti diverse, le quadruple non interne con zero oppure un puntoW formano28 orbite, in totale

    C(12,4)−2C(6,4)+10C(12,3)=2665.

La generazione espande le orbite; il checker classifica tutte le7.315 quadruple tramite firme canoniche dei sottoinsiemi nelle due componenti. Le partizioni coincidono letteralmente. I marcatori e le dimensioni completi sono in `data/ORBIT_CATALOGUE.json`.

Ventisei certificati escludono2605 quadruple. Sei casi, E09M,E11M,E15M,E18M,E19M,E21M, richiedono anche l'ancora completa del membro marcato, oltre alle19 centrali. Il suo dominio è collegato alle stesse variabili e gradi. Non si applica a quell'ancora il confinamento del §2 riservato alle centrali.

Le due orbite NON escluse dalla prova sono:

|ID|Marcatore|Taglia|κ, coni disgiunti|Tipo|
|---|---|---:|---:|---|
|E24|{6,7,11,12}|30|10|Tripla effettiva P9 più un esterno|
|E26|{6,9,11,12}|30|11|Tripla eccezionale P5 più un esterno|

Ogni residuo ha ora al massimo due punti inY∪Z, oppure esattamente tre, tutti inZ e appartenenti a una di queste due orbite. Non sono permessi quattro punti del link o tre punti distribuiti sulle due componenti. Il successivo lemma è formulato deliberatamente con questa premessa più debole.

L'indice portante contiene esattamente43 certificati:17 interni e26 esterni,11 maggiorazioni e32 incompatibilità. I candidati E24M/E26M prodotti durante l'esplorazione non sono dipendenze della prova e non ricevono qui credito di replay separato.

## 5. Copertura con eccezioni per una tripla pura

### 5.1 Enunciato parametrico

Sia un link completo di centrox formato da due P9/P10 su supporti disgiuntiY,Z. Supponiamo che ogni residuoQ abbia |Q∩(Y∪Z)|≤2, oppure |Q∩(Y∪Z)|=3 con tutti e tre i punti nella stessa componente. Sia presente

    M={y,z,a,b},     y∈Y,z∈Z,a,b esterni e distinti.

Ogni residuo appartiene a una delle categorie

    A: contiene{y,z};       B: contienea;       C: contieneb;

salvo, al massimo, due estensioni di una tripla eccezionale per ciascuno dei punti marcati che sia P5 in una P9.

### 5.2 Dimostrazione della copertura

Prendiamo Q che evitaa,b e non contiene entrambi y,z. Se Q∩M è vuota, una delle componenti contiene al massimo un punto diQ. Questo vale anche quandoQ ha tre punti puri, scegliendo l'altra componente. In quella componente si sceglie un blocco che eviti il suo punto marcato e l'eventuale punto diQ: P10 ha due blocchi che evitano ogni coppia, e P9 ne conserva almeno uno. Il cono è disgiunto daM eQ, dando un sunflower vuoto.

Se Q∩M={y}, si cerca un blocco della componenteY che contengay ed eviti gli altri punti interni diQ. Se c'è al massimo un altro punto, P9/P10 lo consentono sempre. Se ce ne sono due, Q ha una tripla puraU={y,u,v} inY. La scelta fallisce precisamente quando{u,v} copre l'intero link grafico della stella diy nella componente.

Per C5 nessuna coppia copre tutti i cinque archi. Per P5 la copertura di due vertici è unica. Nella P9 che omette012, le triple eccezionali sono

    y=0:035;       y=1:145;       y=2:234.

Sono triple assenti dalla P9, non il blocco omesso012. Ogni tale tripla può avere al massimo due estensioni nella famiglia, per il cap2 sulle codegree delle triple. Il caso Q∩M={z} è simmetrico. Questo prova la copertura con al massimo2e eccezioni, dovee conta i punti marcati di tipoP5.

### 5.3 Il numero dei residui

Le tre categorie principali hanno cardinalità≤6,D,D se i gradi globali sono≤D. Il membroM appartiene a tutte e tre: nella somma è contato tre volte, nell'unione una. Quindi

    r≤6+D+D−2+2e=2D+4+2e.

Le eventuali altre sovrapposizioni riducono l'unione e possono essere ignorate. Nel ramoP10⊔P9,e≤1 eD=19, dunque

    r≤44<50.

**Nessun residuo misto può esistere.** Questo passaggio non usaH27; usa la premessa geometrica appena prodotta e le capacità universali. PerP9⊔P9,e≤2: la formula rimane valida, ma non si afferma che la sua premessa sia già acquisita nel successivo ramo18.

### 5.4 Verifiche e controllo positivo delle eccezioni

SuP10⊔P10,P10⊔P9,P9⊔P9, per ogni coppia di punti marcati si ricostruiscono tutte le436 tracce canoniche della forma ammessa, con rappresentanti nuovi per i punti esterni non marcati. Sono47.088 controlli. Fuori dalle tre categorie,12.690 tracce hanno un sunflower letterale e54 sono precisamente le eccezioniP5. Le tre radici hanno rispettivamente0,18,36 tracce eccezionali. La prova generale non dipende da una limitazione degli esterni: le intersezioni con i coni eM dipendono soltanto dalla traccia.

Un controllo positivo contiene i19 coni, M={0,6,12,13} e

    {6,9,11,14},     {6,9,11,15}.

Sono22 quadruple senza tre-sunflower, verificate su tutte le1540 terne. I due ultimi membri evitano le categorieA,B,C e realizzano entrambe le estensioni eccezionali ammesse. Il controllo haμ=11, non42. Esso impedisce di eliminare silenziosamente il termine+2e.

## 6. Il deficit residuo è3, mentre ne servono37

L'universo terminale, dopo i30 interni, le2605 colonne esterne certificate e le1620 miste escluse dal lemma, ha

    7315−30−2605−1620=3060

quadruple. Il loro istogramma diκ(Q), numero dei19 coni disgiunti, è:

|κ|10|11|12|14|15|19|
|---|---:|---:|---:|---:|---:|---:|
|Colonne|30|840|540|1080|360|210|

Ogni colonna haκ≥11, salvo le30 diE24. Queste estendono tre tripleP9 effettivamente prescritte:

    {6,7,11},       {6,8,9},       {7,8,10}.

Ciascuna tripla ha già il cono attraversox. Il cap2 lascia al massimo UNA estensione residua per tripla. Perciò il numero totale di membriE24 è≤3 e

    Σ_Q max(0,11−κ(Q)) z_Q≤3.

Non si usa il più debole limite6 e non si impone che nessunaE24 sia presente. E26 haκ=11 e non contribuisce al deficit.

Per cinquanta residui, contando le disgiunzioni con i19 coni,

    Σ_Q κ(Q) ≥11·50−3=547.

Per H27 ogni cono è disgiunto da al massimo27 membri, dunque

    Σ_Q κ(Q)≤19·27=513.

La contraddizione è **547≤513**. Equivalentemente il deficit necessario è11·50−513=37, mentre il massimo appena provato è3.

Il checker terminale somma letteralmente le19 disuguaglianzeH27 e le tre capacità residue delle triple speciali: ogni colonna terminale riceve coefficiente almeno11 e il membro destro è513+3=516. Quindi11r≤516, impossibile perr=50. Questo è un certificato intero elementare, non un LP ulteriore.

Ogni candidataF69/max19 determina un internoP9 coperto, poi un internoP10 coperto, poi un marcatore di ciascuna orbita che potrebbe violare la geometria. Tutti i suoi stati sono compresi nei sistemi necessari; le refutazioni o i limiti esatti li escludono. Le due orbite intenzionalmente rimaste e ogni posizione degli esterni sono coperte dal lemma e dal conteggio. Il ramo19 è interamente chiuso, non soltanto un insieme di punti frazionari del modello.

## 7. Natura della certificazione e verifica

Un sistema ha Az≤b,Ez=f,l≤z≤u con coefficienti interi. Il certificato usa moltiplicatori interiy≥0,η liberi e scalat>0. Ponendoq=Aᵀy+Eᵀη,H=y·b+η·f, per l'incompatibilità si verifica

    H−Σ_j min(l_jq_j,u_jq_j)<0.

Per un limite superiore all'obiettivoc·z si poner=tc−q e si verifica

    H+Σ_j max(l_jr_j,u_jr_j)<50t.

I coefficienti negativi sono pagati sui rispettivi intervalli; nessuna tolleranza decide il risultato. I43 modelli vengono ricostruiti da un produttore a maschere/p-prima-di-t e da un auditor a insiemi/t-prima-di-p. Il confronto è letterale su tutti i campi, comprese le colonne congelate, non soltanto sugli hash.

I primi tre certificatiP9 erano scoperti prima dell'aggiunta delle57 righe condizionali. Sono stati trasportati al sistemaV2 con moltiplicatori zero sulle righe aggiunte e rigiocati sul sistema completo. Questo non modifica la combinazione né cancella una premessa.

I test negativi modificano sei dati per ciascuno dei43 certificati: valore,scala,target,indice,peso e combinazione vuota. Altri dodici test alterano copertura, ordine, premesse, eccezioni e metadati di stadio. Totale270 rifiuti deliberati per modalità. I controlli sono limitati: non costituiscono una prova che il software sia privo di ogni possibile difetto.

Tutte le43 famiglie iniziali prescritte/marcate sono controllate come famiglie effettive:53.926 terne complessive, con le ripetizioni fra controlli dichiarate. Sono controllate separatamente la famiglia da22 delle eccezioni e il testimone inferiore54, su1540 e24.804 terne. Nessuna famiglia positiva è un esempio nel dominioμ42 della candidata69.

La verifica completa è eseguita dall’unico ingresso `scripts/verify.py` nella radice del companion, secondo `SUITE_PLAN.json`. Per questo ramo i controlli esatti sono `check_linear`, `check_geometry`, `check_extended_cover`, `check_controls` e `check_scope`; coprono43 certificati, tutte le orbite e le eccezioni pure-three, i controcontrolli e il dominio successivo. Gli input selezionati sono file ordinari inclusi nel companion; nessuna ZIP baseline è letta. La suite completa include separatamente MU42 e C5, senza attribuire al solo ramo D19 la loro verifica.

