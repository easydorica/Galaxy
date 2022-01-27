# Sommario
1. [Accedere all'istanza Galaxy](#accesso)
2. [Introduzione al workflow di analisi di panneli genici (amplicon-based)](#introduzione)



## Accedere all'istanza Galaxy "https://galaxy.aosp.biodec.com/" <a name="accesso"></a>
* Aprire un qualsiasi browser (es. Googe Chrome).
* Nella barra degli indirizzi del browser inserire l'indirizzo  [https://galaxy.aosp.biodec.com](https://galaxy.aosp.biodec.com), al quale è raggiungibile l'istanza Galaxy presente sul nostro server.
* Dal menù di testata, in alto a destra, click "**Login or Register**" ed inserire le proprie credenziali di acceso (email personale e password) richieste nella finestra di dialogo.

## Introduzione al workflow di analisi di panneli genici (amplicon-based) <a name="introduzione"></a>
**"SNP/InDels calling pipeline"** è un workflow di analisi dedicato alla chiamata di varianti a singolo nucleotide e piccole inserzioni/delezioni da dati di pannelli genici NGS ottenuti con il metodo basato su ampliconi e la tecnologia di sequenziamento Ion Torrent, usando per l'allineamento il genoma di riferimento hg19.
Il workflow è stato costruito concatenando diversi subworkflow ogniuno dei quali rappresenta uno step dell'analisi bioinformatica.

![immagine1](https://user-images.githubusercontent.com/89908049/151352349-5f94dca7-ed97-48e9-98dd-8762a2670f71.png)

> **_STEP_1:_** (FASTQ quality check): This workflow performs a quality control check on sequence data in fastq format. The analysis is performed by two tools (__FastQC and fastp__) which provide a quick overview of whether the data looks good and there are no problems or biases which may affect downstream analysis. Results and evaluations are returned in the form of charts and tables summarized in MultiQC report. 
The final output will be a collection of fastq files containing the trimmed reads.
`FastQC` `fastp`

> **_STEP_2:_** (alignment): This workflow performs the alignment of the previously processed reads to the reference genome hg19 using BWA-MEM.
`BWA_MEM` `Samtools` `Picard`

> **_STEP_3:_** (Calling to create a multi-sample VCF): This workflow starts with aligned sequencing data (BAMs) of multiple individuals, and ends with a single multi-sample VCF file comprising all analyzed samples and only the genomic position within the target regions where at least one indivudal has a mutation or a polymorphism. Low-quality variants are flagged in the final VCF file and calling statistics are summarized in the final MultiQC report.
`bcftools`

> **_STEP_4:_** (MultiQc report): This step creates a single report visualising quality metrics resulting from multiple tools (FastQC, fastp, samtools flagstat, bcftools stats) across many samples.
> `MultiQC`

> **_STEP_5:_** (Variant annotation): This workflow performs annotation of SNPs and short indels contained in the input VCF file, including also funcional annotation such as: scores of predicted impacts (SIFT, PolyPhen, CADD)-clinical significance (Clinvar)-dbSNP identifiers-allele frequencies (GnomAD)
`SnpEFF` `SnpSift` **`Extraeff`**

```
Extraeff è un tool custom utilizzato per coinciliare i comportamenti dei diversi tool di annotazione e armonizzare il formato di annotazione del vcf, cosi da renderlo analizzabile dal tool Rabdomyzer. xtraeff ricerca le annotazioni di SnpSift che sono elencate nel file di annotazione e le integra nelle annotazioni di SNPEff, generando un file VCF in cui le annotazioni di interesse sono tutte separate da “|”.
```

![image](/uploads/897c55090bfde68a1d126993d58df9d3/image.png)



* Dalla barra di menù in alto click "Shared Data" e dal menù a tendina selezionare "**Data Libraries**"
![galaxy2](https://user-images.githubusercontent.com/89908049/146207844-ae8a9b61-c045-4c3d-959e-4edc9b1c9f8f.png)
* Dalla schermata che si ottiene click "**Test**", quindi spuntare entramabi i file con estensione fastqsanger.gz presenti.
* Dal menù in alto click su "**Export to History**" e dal menu a tendina selezionare "**as Datasets**". Quindi nella finestra di dialogo che appare click "**Import**"

![galaxy3](https://user-images.githubusercontent.com/89908049/146209498-37cb6d11-b8b0-4b7d-b52d-e8b3bf5deea6.png)

* A questo punto i due fastq selezionati dovranno apparire  nella sezione di destra della schermata principale, denominata "History" e destinata all'archiviazione dei file in galaxy.

![galaxy4](https://user-images.githubusercontent.com/89908049/146211223-bd1094cf-73e5-4864-8ed2-8fad9bbe4dbb.png)

## Provare a lanciare uno dei tool presenti
* Nella sezione di sinistra denominata "Tools", nella relativa barra di ricerca scrivere "BWA" quindi scegliere dalla lista ottenuta il tool "**Map with BWA-MEM - map medium and long reads (> 100 bp) against reference genome (Galaxy Version 0.7.17.2)**". Questo tool viene utilizzato per l'allineamento delle reads al genoma di riferimento, generando a partire dai fastq un file .bam.
- A questo punto nella sezione centrale della schermata di esecuzione del programma compilare come segue i diversi parametri del tool:
  - dal menù a tendina dell'opzione "**Using reference genome**" scegliere **hg19**
  - dal menù a tendina dell'opzione "**Single or Paired-end reads**" scegliere **Paired**
  - dal menù a tendina dell'opzione "**Select first set of reads**" selezionare il fastq nominato **sample1-f** e in "**Select second set of reads**" selezionare **sample1-r**
 - Quindi premere il pulsante in fondo "**Execute**"
 - L'output in elaborazione comparirà nella sezione di destra in arancione. Soltanto se il processo verrà portato a termine correttamente l'output verrà colorato di verde.

![galaxy5](https://user-images.githubusercontent.com/89908049/146215847-b8bc8b14-904e-4d70-b0bd-e67584c43952.png)

## Visualizzare un BAM su IGV
* Senza chiudere la pagina del browser relativa a galaxy, ritornare sul desktop ed aprire una qualsiasi delle versioni disponibili di IGV, facendo doppio click sull'icona relativa (es: igv6G). Quindi attendere l'apertura del programma e il caricamento del genoma di riferimento (Human hg19).
* Tenendo aperta la finestra di IGV, riaprire la schermata di galaxy
* Una volta completato il porcesso di allineamento (il box relativo all'output deve essere verde), click sull'output di BWA-MEM all'interno della history quindi scegliere "**display with IGV**" facendo click su **local**.
* Automaticamente il bam verrà caricato nella finestra di IGV precedentemente aperta.
* Per visualizzare il contenuto del bam, scrivere **chrM** nella finestra di navigazione e premere invio.
Dovreste visualizzare il nome del file bam nella sezione di sinistra della schermata di IGV e vedere le reads allineate al centro.

![desktopgalaxy](https://user-images.githubusercontent.com/89908049/146219184-bdff24a1-1dd7-498f-be41-5746f6748c53.png "output atteso")
