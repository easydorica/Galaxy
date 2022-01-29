# Guida pratica al corso Galaxy

# Sommario
1. [Accedere all'istanza Galaxy](#accesso)
2. [Introduzione al workflow di analisi per panneli genici (amplicon-based)](#introduzione)
3. [Lanciare un workflow condiviso](#workflow1)
4. [Creare un workflow combinando più subworkflow](#workflow2)
5. [Utilizzo di Rabdomyzer in Galaxy](#Rabdomyzer)

## 🖥️ Accedere all'istanza Galaxy "https://galaxy.aosp.biodec.com/" <a name="accesso"></a>
* Aprire un qualsiasi browser (es. Googe Chrome).
* Nella barra degli indirizzi del browser inserire l'indirizzo  [https://galaxy.aosp.biodec.com](https://galaxy.aosp.biodec.com), al quale è raggiungibile l'istanza Galaxy presente sul nostro server.
* Dal menù di testata, in alto a destra, click "**Login or Register**" ed inserire le proprie credenziali di acceso (email personale e password) richieste nella finestra di dialogo.

## Introduzione al workflow di analisi per panneli genici (amplicon-based) <a name="introduzione"></a>
**"SNP/InDels calling pipeline"** è un workflow di analisi dedicato alla chiamata di varianti a singolo nucleotide e piccole inserzioni/delezioni da dati di pannelli genici NGS ottenuti con il metodo basato su ampliconi e la tecnologia di sequenziamento Ion Torrent, usando per l'allineamento il genoma di riferimento hg19.
Il workflow è stato costruito concatenando diversi subworkflow ogniuno dei quali rappresenta uno step dell'analisi bioinformatica.

![immagine](https://user-images.githubusercontent.com/89908049/151522286-a60cd3ac-af1e-44ae-8c33-4a8c482e48de.png)

> **_STEP_1:_** (FASTQ quality check): This workflow performs a quality control check on sequence data in fastq format. The analysis is performed by two tools (__FastQC and fastp__) which provide a quick overview of whether the data looks good and there are no problems or biases which may affect downstream analysis. Results and evaluations are returned in the form of charts and tables summarized in MultiQC report. 
The final output will be a collection of fastq files containing the trimmed reads.  
🔧 `FastQC` `fastp`

> **_STEP_2:_** (alignment): This workflow performs the alignment of the previously processed reads to the reference genome hg19 using BWA-MEM.  
🔧 `BWA_MEM` `Samtools` `Picard`

> **_STEP_3:_** (Calling to create a multi-sample VCF): This workflow starts with aligned sequencing data (BAMs) of multiple individuals, and ends with a single multi-sample VCF file comprising all analyzed samples and only the genomic position within the target regions where at least one indivudal has a mutation or a polymorphism. Low-quality variants are flagged in the final VCF file and calling statistics are summarized in the final MultiQC report.  
🔧 `bcftools`

> **_STEP_4:_** (MultiQc report): This step creates a single report visualising quality metrics resulting from multiple tools (FastQC, fastp, samtools flagstat, bcftools stats) across many samples.  
🔧 `MultiQC`

> **_STEP_5:_** (Variant annotation): This workflow performs annotation of SNPs and short indels contained in the input VCF file, including also funcional annotation such as: scores of predicted impacts (SIFT, PolyPhen, CADD)-clinical significance (Clinvar)-dbSNP identifiers-allele frequencies (GnomAD)  
🔧 `SnpEFF` `SnpSift` **`Extraeff`**   
>
>       📖 Extraeff:è un tool custom utilizzato per coinciliare i comportamenti dei 
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
:tools: `Rabdomyzer`

## 🖥️ Lanciare un workflow condiviso <a name="workflow1"></a>
* Dalla barra di menù in alto click **Shared Data** e dal menù a tendina click **Data Libraries**
* Click sulla cartella **corso_aosp**
* Seleziona "sample1" e "sample2" e click **Export to History as a Collection**. Creare una collection come **List** e assegnare un nome (es:Fastq)

![immagine](https://user-images.githubusercontent.com/89908049/151391444-fd7d9202-0125-48b6-aca0-8236f9c9a61c.png)

* Click su :homes: per tornare alla schermata principale. Nella propria History sarà possibile visualizzare la collection appena importata.
* Dalla barra di menù in alto click **Shared Data** e dal menù a tendina click **Workflows**
* Click sul workflow **Quality_check+alignment** e dal menù a tendina click **Run**

![immagine](https://user-images.githubusercontent.com/89908049/151392744-92ed07f6-1046-40d6-904a-eead3d580c2d.png)

* Compila il form con le informazioni richieste:
  * Fastq input dataset collection
  * Library name (LB)
  * Date that run was produced (DT)  
Quindi click su **Run Workflow**

![immagine](https://user-images.githubusercontent.com/89908049/151394762-50f1cb92-bc21-4ad4-9ce6-1ac83b57666b.png)

## 🖥️ Creare un workflow combinando più subworkflow <a name="workflow2"></a>
* Per importare un workflow condiviso click **Shared Data** e dal menù a tendina click **Workflows**
* Click sul workflow **Calling to create a multi-sample VCF** e dalla menù a tendina click **Import**. Una volta completata l'operazione ritorna alla pagina precedente.
* Ripetere la stessa operazione anche per i workflow **Variant annotation** e **Rabdomyzer**
* Tornare alla schermata principale :homes: 
* Dalla barra di menù in alto click **Workflow** e in alto a destra click :heavy_plus_sign: **Create**
* Assegnare un nome al workflow che s'intende creare (es:vcf_analysis) e click su **Create**
* Dalla sezione **Tools** selezionare **Workflows**
* Click sul nome dei subworkflow che s'intende inserire.
* Ordinare i subworkflows, collegando gli output del primo box agli input del secondo, e cosi via.

![immagine](https://user-images.githubusercontent.com/89908049/151401536-a5f7cdfd-536a-4670-8852-06e35b255798.png)

* Per inserire l'input del workflow, dalla sezione **Tools** selezionare **Inputs** e quindi click su **Input dataset collection**. 

![immagine](https://user-images.githubusercontent.com/89908049/151402844-03c02d50-d921-41f5-9c27-d60b0b2b7288.png)

* Per inserire i file target e quelli di annotazione richiesti nel subworkflow per l'annotazione e/o da Rabdomyzer, slezionare **Input dataset** dalla sezione **Inputs**.  
> ❗ è importante assegare una **Label** a tutti i dataset di input.

![immagine](https://user-images.githubusercontent.com/89908049/151403771-3fd2f772-796d-4346-96cd-5c3e92e33804.png)

* Una volta completata la creazione del workflow click in alto a destra su :floppy_disk: **Save Workflow**

* Prima di lanciare il workflow, fare l'import all'interno della propria History dei file di annotazione richiesti:
   - `Shared Data`  
   - `Data Libraries` 
      - 📁 corso_aosp 
         - 📁 Annotation 
           - 📄 spunta tutti i file 
           - 📘 `Export to History` 
           - `as Datasets` 
    - `Data Libraries`
       - 📁 VCF database
         - 📄 spunta _"clinvar_20210718.vcf"_ e _"gnomad.exomes.r2.1.1.sites_customann.vcf"_
         - 📘 `Export to History`
         - - `as Datasets` 

* Dalla schermata principale, click **Workflow** e dalla lista selezionare quello appena creato.
* click su :arrow_forward: (Run workflow)
* Compila il form con le informazioni richieste. Quindi click su **Run Workflow**.

 ![immagine](https://user-images.githubusercontent.com/89908049/151519731-385e320b-ddb9-4e86-bb95-f2784078f662.png)

## 🖥️  Utilizzo di Rabdomyzer in Galaxy <a name="Rabdomyzer"></a>

> 📖 Rabdomyzer è un programma "custom" sviluppato per interpretare le varianti a singolo nucleotide (SNV) e le piccole inserzioni e delezioni (InDels), semplificando la visualizzazione dei risultati NGS.
Consente di filtrare le varianti in base alla frequenza degli alleli minori (MAF) e al modello di ereditarietà stabilito, definito nel file model specificato.
Il modello potrà essere:  
 **_"trio"_** se nelle colonne dei genitori verrà specificato il loro ID (_variant and gene based analysis_)
**_"singolo"_** se entrambe le colonne dei genitori contengono 0 (_variant based filtering_).

![immagine](https://user-images.githubusercontent.com/89908049/151526447-12b55d2e-c52b-4fc8-9c7e-e87be027c028.png)

> Alla fine del processo, Rabdomyzer genera output in formato testuale contenenti le varianti suddivise in varianti genetiche erezigoti, omozigoti e (se possibile) eterozigoti composte e un file excel che unisce tutti gli output txt.

* Per iniziare importare nella propria History il file vcf condiviso negli `Shared Data`:
 - `Shared Data`  
   - `Data Libraries` 
      - 📁 corso_aosp
         - 📄 spunta _"vcf_multisample.vcf"
         - 📘 `Export to History`
         - `as Datasets` 
* Crea un file model come da esempio

| proband | father | mother | control | unknown |
| ------ | ------ | ------ | ------ | ------ |
| BE45 | 0 | 0 | 0 | 0 |

❗ utilizzare il TAB come separatore 

* Richiamare il tool **Rabdomyzer** dalla sezione **Tools** nella schermata principale della nostra istanza Galaxy
* Click su **Rabdomyzer filtration**
* Compila il form con le informazioni richieste. Quindi click su **Execute**.

![immagine](https://user-images.githubusercontent.com/89908049/151532146-519cf3c9-867c-4702-80dd-1fdd8512cf6f.png)

* 👁️ visualizzare il file excel ottenuto
