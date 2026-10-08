# The separate C5 obstruction

The universal R16 classification supplies the existence of an internal degree-six point. The following local obstruction and rooted finite C5 certificate remain separate mathematical premises. The checker is scripts/check_c5.py, with certificates/C5_EMPTY_R16.bin. It covers 39 patterns and 572 complete cases.

## 1. Un'ostruzione C5 sulle triple, senza ipotesi globali su F

### 1.1 Il nucleo finito R16

**[CL5 da CL3, con il solo lemma R16/Δ≤5 importato e i fondamenti grafici] Lemma C5.** Non esiste R16 L contenente un punto c di grado5 il cui link sia C5 su cinque punti Y, se i soli membri di L contenuti in U={c}∪Y sono i cinque del cono c+C5.

**[CL5] Riduzione del dominio.** Ogni punto usato di R16 ha grado tra due e sei. Il cap sei segue dai link grafici: grado massimo due e matching massimo due. Un punto di grado uno in un'ancora xyz darebbe un intorno di al massimo 1+3+3+1=8 triple, contro le almeno nove richieste da R16.

Per una coppia xy USATA, scegliendo xyz∈L,

    9 ≤ |N_L[xyz]| ≤ d_L(x)+d_L(y)−d_L(x,y)+3.

Quindi d_L(x)+d_L(y)≥7 e

    d_L(x,y) ≤ min(2,d_L(x)+d_L(y)−6).

Una capacità non positiva vieta l'uso della coppia: non si impone un limite negativo a una coppia inutilizzata. Ogni tripla ha somma dei gradi almeno11, perché il suo intorno è al più la somma dei tre gradi meno due. Una tripla contiene al massimo un punto di grado2 o3.

Il lemma R16/Δ≤5 importato dà un punto z di grado6, con link grafico 2K3. Ogni vicino di c ha codegree due con c e quindi grado almeno3. Nessuno di questi cinque vicini può avere grado6: nel suo 2K3, i due archi attraverso c starebbero nello stesso triangolo e imporrebbero una nuova tripla interamente in U. Pertanto i cinque gradi vicini sono in {3,4,5}; z è ESTERNO a U. Il punto c non può essere usato nei triangoli di z, perché la stella di c è completa.

Siano a,b,c',d,e le molteplicità dei gradi2,3,4,5,6. Necessariamente

    2a+3b+4c'+5d+6e = 48,
    2a+3b ≤ 16,
    2a+5b+10c'+16d+24e ≥ 128,
    e≥1.

Per l'ultima stima, se Z conta le coppie di triple disgiunte e r(v) i vicini con codegree due,

    Z=120−Σ_v C(d_L(v),2)+(1/2)Σ_v r(v) ≤56.

I minimi di r(v) ai gradi2,…,6 sono0,1,2,4,6. Seguono dalla decomposizione dei piccoli link in cammini e cicli; il replay verifica anche tutti i grafi etichettati sui sei punti che bastano per questa classificazione. Sostituendo i minimi si ottiene la disequazione esposta.

Le 3^5 sequenze dei gradi lungo C5 danno39 tipi sotto le dieci simmetrie del ciclo. Enumerando poi TUTTE le molteplicità esterne consentite dal budget48, senza imporre un supporto arbitrario, si ottengono572 casi radicati:

| Supporto del link | 9 | 10 | 11 | 12 | 13 | Totale |
|---|---:|---:|---:|---:|---:|---:|
| Casi | 1 | 61 | 253 | 233 | 24 | 572 |

Il produttore usa partizioni non decrescenti del budget; il verificatore enumera le molteplicità dei cinque gradi e ricostruisce il gruppo del ciclo fra tutte le120 permutazioni. Concordano sull'intero elenco. I572 casi NON sono572 classi di isomorfismo di famiglie.

Ogni ipotetica L si rinomina ponendo c=0, ciclo1,…,5, e i punti esterni in ordine di grado. Si sceglie il primo esterno di grado6 come z. Su un supporto di n punti si esaminano tutti i C(n−2,6) insiemi di sei vicini di z, evitando c,z, e tutte le dieci partizioni non ordinate in due triangoli. La normalizzazione non impone automorfismi a L. Gli isolati non appartengono al supporto e non sono richiesti.

I casi producono829.850 radici etichettate. Per ciascuna il certificato contiene un testimone locale esatto:

| Motivo di esclusione | Radici |
|---|---:|
| Coppia usata oltre la propria capacità | 717.385 |
| Grado già superiore a quello prescritto | 40.941 |
| Incapacità di raggiungere il grado di un punto | 71.524 |
| Aperte | **0** |

Nell'ultimo caso si prendono TUTTE le triple che potrebbero ancora essere aggiunte individualmente: si escludono solo triple interne non prescritte, somme di grado insufficienti, gradi o coppie già saturi, sunflower letterali con due membri prescritti e violazioni monotone di R16. Se anche includendo tutte le triple rimaste un punto non raggiunge il proprio grado, nessun completamento esiste. Non si presume compatibilità reciproca di tutte le candidate: ignorarla allarga la capacità, e rende il rifiuto più forte.

`certificates/C5_EMPTY_R16.bin` contiene un byte per radice. I codici0,…,n−1 indicano un punto senza capacità; 32+j una coppia sovraccarica; 128+v un grado sovraccarico. Non esistono byte OPEN accettati. Il C++ produce i testimoni; `scripts/check_c5.py` ricostruisce indipendentemente casi, stelle e capacità con interi Python. Il predicato Python usa l'assenza di punti di molteplicità esattamente due in una terna, quello C++ confronta le tre intersezioni. Non vi sono cutoff nel certificato finale. Questo conclude il lemma R16.

### 1.2 Rafforzamento senza assumere R16

**[CL5, usando il lemma appena certificato e B4] Corollario C5 vuoto.** Una famiglia sunflower-free di SEDICI triple non può avere un punto c di grado5 con link C5 e soltanto i cinque membri del cono sul relativo supporto U di sei punti. Non si assume R16 nell'enunciato di questo corollario.

**Dimostrazione.** Se una tripla A avesse almeno otto membri disgiunti, B4 dividerebbe L in due intersecanti D(A),N[A], ciascuna di taglia al più dieci e quindi almeno sei. Se la parte da almeno otto è P8, P9 o P10, l'isolamento rende disgiunti i supporti delle due parti: un eventuale blocco omesso è interno al supporto della parte D(A) e sarebbe anch'esso disgiunto da A, quindi non potrebbe appartenere a N[A]. La stessa conclusione vale se la P8 è la parte N[A]: i suoi blocchi omessi incontrano A, perché appartengono alla stessa P10, e non possono essere nella parte D(A).

Il punto c e tutta la sua stella C5 appartengono quindi a una sola parte intersecante, di taglia almeno sei. Ogni altra tripla di questa parte deve incontrare tutte le cinque triple della stella; se evita c deve coprire C5 con almeno tre punti. È dunque interamente in U. Ne risulta almeno un membro interno ulteriore, contro l'ipotesi.

Resta soltanto la separazione8+8 con due Q8. Un punto del nucleo di una Q8 ha nel link un triangolo oppure un C4, nessuno dei quali può essere sottografo di C5. Un punto periferico in entrambe ha grado totale al massimo due. Neppure questo caso può avere il punto c richiesto. Questo argomento NON presume disgiunte le foglie delle due Q8.

Pertanto ogni tripla ha al massimo sette disgiunti: L soddisfa R16. Il lemma del §1.1 lo esclude. □

La riduzione precedente è una dimostrazione interna, non una nuova enumerazione delle famiglie non-R16. Il corollario non usa H27, 71, μ44, E17/E18, un cap sul supporto di F o un cap sui suoi gradi. Conserva B4/isolamento e il lemma finito R16/Δ≤5 importati, oltre al certificato C5 nuovo.

