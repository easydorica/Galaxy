# Guida pratica al corso Galaxy

# Sommario
1. [Accedere all'istanza Galaxy](#accesso)
2. [Introduzione al workflow di analisi per panneli genici (amplicon-based)](#introduzione)
3. [Importare all'interno della propria History i file condivisi](#shareddata)
4. [Lanciare un workflow condiviso](#workflow1)

## 💻 Accedere all'istanza Galaxy "https://galaxy.aosp.biodec.com/" <a name="accesso"></a>
* Aprire un qualsiasi browser (es. Googe Chrome).
* Nella barra degli indirizzi del browser inserire l'indirizzo  [https://galaxy.aosp.biodec.com](https://galaxy.aosp.biodec.com), al quale è raggiungibile l'istanza Galaxy presente sul nostro server.
* Dal menù di testata, in alto a destra, click "**Login or Register**" ed inserire le proprie credenziali di acceso (email personale e password) richieste nella finestra di dialogo.

## Introduzione al workflow di analisi per panneli genici (amplicon-based) <a name="introduzione"></a>
**"SNP/InDels calling pipeline"** è un workflow di analisi dedicato alla chiamata di varianti a singolo nucleotide e piccole inserzioni/delezioni da dati di pannelli genici NGS ottenuti con il metodo basato su ampliconi e la tecnologia di sequenziamento Ion Torrent, usando per l'allineamento il genoma di riferimento hg19.
Il workflow è stato costruito concatenando diversi subworkflow ogniuno dei quali rappresenta uno step dell'analisi bioinformatica.

![immagine](https://user-images.githubusercontent.com/89908049/151522286-a60cd3ac-af1e-44ae-8c33-4a8c482e48de.png)

> **_STEP_1:_** (FASTQ quality check): This workflow performs a quality control check on sequence data in fastq format. The analysis is performed by two tools (__FastQC and fastp__) which provide a quick overview of whether the data looks good and there are no problems or biases which may affect downstream analysis. Results and evaluations are returned in the form of charts and tables summarized in MultiQC report. 
The final output will be a collection of fastq files containing the trimmed reads.  
⚒️ `FastQC` `fastp`

> **_STEP_2:_** (alignment): This workflow performs the alignment of the previously processed reads to the reference genome hg19 using BWA-MEM.  
⚒️ `BWA_MEM` `Samtools` `Picard`

> **_STEP_3:_** (Calling to create a multi-sample VCF): This workflow starts with aligned sequencing data (BAMs) of multiple individuals, and ends with a single multi-sample VCF file comprising all analyzed samples and only the genomic position within the target regions where at least one indivudal has a mutation or a polymorphism. Low-quality variants are flagged in the final VCF file and calling statistics are summarized in the final MultiQC report.  
⚒️ `bcftools`

> **_STEP_4:_** (MultiQc report): This step creates a single report visualising quality metrics resulting from multiple tools (FastQC, fastp, samtools flagstat, bcftools stats) across many samples.  
⚒️ `MultiQC`

> **_STEP_5:_** (Variant annotation): This workflow performs annotation of SNPs and short indels contained in the input VCF file, including also funcional annotation such as: scores of predicted impacts (SIFT, PolyPhen, CADD)-clinical significance (Clinvar)-dbSNP identifiers-allele frequencies (GnomAD)  
⚒️ `SnpEFF` `SnpSift` **`Extraeff`**   
>
>       Extraeff:è un tool custom utilizzato per coinciliare i comportamenti dei 
>       diversi tool di annotazione e armonizzare il formato di annotazione del vcf, cosi da 
>       renderlo analizzabile dal tool Rabdomyzer. Extraeff ricerca le annotazioni di SnpSift 
>       che sono elencate nel file di annotazione e le integra nelle annotazioni di SnpEFF,
>       generando un file vcf in cui le annotazioni d'interesse sono tutte separate da "|".

L'output conclusivo di questo workflow è un file vcf multisample annotato comprendente tutti i campioni analizzati e solo le posizioni genomiche alternative (in almeno un individuo della coorte) all'interno delle regioni target.
Questo file vcf puo essere utilizzato come input del workflow **Rabdomyzer**, che rappresenta lo **STEP_6** della nostra analisi.

![immagine](https://user-images.githubusercontent.com/89908049/151382830-d1201d0c-7031-437c-a30a-4c83eae02b52.png)

> **_STEP_6:_** (Rabdomyzer): Rabdomyzer is a tool used to interpret single nucleotide variants (SNVs) and small insertions and deletions (InDels), simplifying NGS results visualization. 
It enables filtering variants based on minor allele frequency (MAF) and established inheritance pattern, defined in the specified model file.
At the end of the process, Rabdomyzer generates outputs of variant interpretation results in text format splitted in herezygous, homozygous and (if possible) compound heterozygous genetic variants and an excel file merging all txt outputs.  
⚒️ `Rabdomyzer`
---
> :book: Rabdomyzer <a name="rabdomyzer"></a> è un programma "custom" sviluppato per interpretare le varianti a singolo nucleotide (SNV) e le piccole inserzioni e delezioni (InDels), semplificando la visualizzazione dei risultati NGS.
> Consente di filtrare le varianti in base alla frequenza degli alleli minori (MAF) e al modello di ereditarietà stabilito, definito nel file model specificato.
> Il modello potrà essere:  
>  **_"trio"_** se nelle colonne dei genitori verrà specificato il loro ID (_variant and gene based analysis_)
>  **_"singolo"_** se entrambe le colonne dei genitori contengono 0 (_variant based filtering_).
>  Il file di modello è un file testuale tab-delimited come da esempio:  

| proband | father | mother | control | unknown |
| ------ | ------ | ------ | ------ | ------ |
| BE45 | 0 | 0 | 0 | 0 |

> Alla fine del processo, Rabdomyzer genera output in formato testuale contenenti le varianti suddivise in varianti genetiche eterozigoti, omozigoti e (se possibile) eterozigoti composte e un file excel che unisce tutti gli output txt.
---

## 💻 Importare all'interno della propria History i file condivisi <a name="shareddata"></a>
I file condivisi si trovano all'interno della sezione Shared Data della nostra istanza Galaxy, nella barra di menù in alto. 
All'interno di questa sezione ci sono sia i file fastq di test, che i file di annotazione neccesari ai fini dell'analisi sopra descritta.  
❗ Attenzione: per poter essere richiamati da un workflow i file devono essere presenti all'interno della history personale in cui s'intende lanciare l'analisi.  
**Per importare i file di annotazione: **
   - `Shared Data`  
   - `Data Libraries` 
      - 📁 corso_aosp 
         - 📁 Annotation 
           - 📄 spunta tutti i file 
           - 📕 `Export to History` 
           - `as Datasets`  
  **Per importare i database di annotazione**
   - `Data Libraries`
       - 📁 VCF database
         - 📄 spunta _"clinvar_20210718.vcf"_ e _"gnomad.exomes.r2.1.1.sites_customann.vcf"_
         - 📕 `Export to History`
         - - `as Datasets` 
 **Per importare i file di test:**
    - `Data Libraries`
       - 📁 corso_aosp 
         - 📄 spunta i file "sample1_IonCodeX" e "sample2_IonCodeY"
         ⚠️ I file fastq per poter essere utilizzati in input al workflow devo rispettare la seguente struttura del nome "sampleID_Ioncode". 
         - 📕 `Export to History as a collection`. Creare una collection come **List** e assegnare un nome (es:Fastq)
![immagine](https://user-images.githubusercontent.com/89908049/151391444-fd7d9202-0125-48b6-aca0-8236f9c9a61c.png)

Ai fini di lanciare l'analisi dovrà essere creato un file "model" come descritto nella precedente sezione dedicata a [Rabdomyzer](#rabdomyzer).  
⚠️ I nomi dei campioni inseriti nel file model devono corrispondere esattamente a quelli riportati nel vcf.  
Ciascuna riga del file corrisponde ad un modello di analisi, quindi un probando/famiglia.
Questo puo essere creato in locale sul proprio PC (esempio con Blocco Note) oppure direttamente in Galaxy andando su:  
* Upload Data 
* Paste/Fetch data
* Assegnare un nome al file 
* Definire come datatype tabular
* click Start

## 💻 Lanciare un workflow condiviso <a name="workflow1"></a>
* Dalla barra di menù in alto click **Shared Data** e dal menù a tendina click **Workflows**
* Click sul workflow **SNP/InDels calling pipeline** e dal menù a tendina click **Run**

* Compila il form con le informazioni richieste:
  * Library name (LB)
  * Fastq input dataset collection
  * Date that run was produced (DT)
  * Target regions
  * GnomAD vcf
  * Clinvar vcf
  * extraeff annotation file
  * model
  * maf
  * db.gene .rabdomyzer
  * ontology file
  * annotation file rabdomyzer

Quindi click su **Run Workflow**

Gli output appariranno nella sezione di destra "History" come box numerati in ordine progressivo. I box arancioni rappresentano i file in corso di elaborazione, quelli verdi gli output. In caso di errori i box si coloreranno di rosso.
Per visualizzare gli output click sul box corrispondente e quindi sull'icona :eye:
