## Creare un account Galaxy 
* Accedere al nostro terminal server “genmedts", aprendo dal menù di Windows l'applicazione “Connessione Desktop Remoto”, e inserire le credenziali personali di accesso.
* Nella schermata di connessione al desktop remoto aprire un qualsiasi browser (es. Googe Chrome).
* Nella barra degli indirizzi del browser inserire l'indirizzo  [https://galaxy.aosp.biodec.com](https://galaxy.aosp.biodec.com), al quale è raggiungibile l'istanza Galaxy presente sul nostro server.
* Dal menù di testata, in alto a destra, click "**Login or Register**" e sulla finestra di dialogo in basso click "**Register here**".

![Galaxy1](https://user-images.githubusercontent.com/89908049/146198544-329b06d5-cbc0-471c-bbfd-17f696a9b8c1.png)

* Compilare la finestra di dialogo con le informazioni richieste (email personale e password).
* Una volta creato l'account procedere al login utilizzando le credenziali usate per la registrazione.

## Caricare un file di prova
* Dalla barra di menù in alto click "Shared Data" e dal menù a tendina selezionare "**Data Libraries**"
![galaxy2](https://user-images.githubusercontent.com/89908049/146207844-ae8a9b61-c045-4c3d-959e-4edc9b1c9f8f.png)
* Dalla schermata che si ottiene click "**Test**", quindi spuntare entramabi i file con estensione fastqsanger.gz presenti.
* Dal menù in alto click su "**Export to History**" e dal menu a tendina selezionare "**as Datasets**". Quindi nella finestra di dialogo che appare click "**Import**"

![galaxy3](https://user-images.githubusercontent.com/89908049/146209498-37cb6d11-b8b0-4b7d-b52d-e8b3bf5deea6.png)

* A questo punto i due fastq selezionati dovranno apparire  nella sezione di destra della schermata principale, denominata "History" e destinata all'archiviazione dei file in galaxy.

![galaxy4](https://user-images.githubusercontent.com/89908049/146211223-bd1094cf-73e5-4864-8ed2-8fad9bbe4dbb.png)

## Provare a lanciare uno dei tool presenti
* Nella sezione di sinistra denominata "Tools", nella relativa barra di ricerca scrivere "BWA" quindi scegliere dalla lista ottenuta il tool "**Map with BWA-MEM - map medium and long reads (> 100 bp) against reference genome (Galaxy Version 0.7.17.2)**". Questo tool viene utilizzato per l'allineamento delle reads al genoma di riferimento, generando a partire dai fastq un file .bam.
- A questo punto nella sezione centrale della schermata di esecuzione dei programma compilare come segue i diversi parametri del tool:
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
