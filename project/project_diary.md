# Project diary

### 2015-02-26

I have copied all raw project data to my home directory in Uppmax do be able to share it with Sofia and Yim, the data consists on:

* 2 projects
* 18 samples
* 8 FASTQ files for the first project (paired end reads)
* 56 FASTQ files for the second project (all samples ran in 2 lanes, paired end reads)
* 19 GB total amount of data

### 2015-02-24

##### Notes from the paper "_Functional shifts in insect microRNA evolution_"

* Again miRNA are short (~22 nucleotides) sequences that mediate RNA translation.
* miRNA are absent in unicellular organisms

### 2015-02-21

##### Notes from paper "_Next Generation Sequencing of miRNAs – Strategies, Resources and Method_"

* miRNA are small RNA species that have been demonstrated to play an important role in Gene Expression. This paper presents some methods and techniques in miRNA sequencing and analysis.
	* miRNA regulates gene expression by modulating translation and stability of mRNA
* miRNAs as well as short interfering RNAs (siRNAs) mediate RNA interference (RNAi)
by binding to the 3’-UTR of target mRNAs either resulting in repressed translation or mRNA decay

* In **the biology of miRNA** they talk a lot about the structure of miRNA. Apparently, there is the cmplementary strand of the mature miRNA (called miRNA*), that is not that important/visible in the sequencing, though it has been found as well in sequencing data.

* NGS of miRNA using Illumina Genome Analyzer: Talking about sequencing practices. An important step is size selection, where the RNA is sequenced, the band corresponding to the size of miRNAs is cut, so that longer sequences (rRNA,
mRNA, etc) are left apart. Then adaptors are ligated to the selected miRNA, followed by reverse transcription to cDNA _(in genetics, complementary DNA (cDNA) is double-stranded DNA synthesized from a messenger RNA)_.

* **Basic data processing steps:** Output will typically contain millions of short reads. Before addressing biological questions, a set of steps needs to be performed.
	1. A first filtration to discard the reads with bad quality (FASTQ format), or
	reads with too many missing nucleotides. _(This step is usually skipped because it is already performed by other software in one of the folowwing steps)_
	2. One important requirement is that the read should originate from the genome of the sequenced organism (contamination screening). Short read aligners are used for this. It is *important* to be careful on how the aligners treat duplicates, because miRNA are very small reads, and the probability of aligning in different places in the genome is high. Reads that first part (15-17bp) align perfectly are kept as potential miRNA. To identify known miRNA we can align against miRBase, an anotation database for miRNA.
	3. Adaptor trimming
	4. Filtering of other small RNA species (rRNA, cytoplasmic RNA, etc)

* **Expression profiling:** Quantitative comparison of miRNA expression in two or more samples. For each read, rpm (Reads per million) is computed as the division of the number of times a unique sequence appears in the sample, divided by the total number of reads in the sample. This mesure (rpm)should be representative of the expression level, however it has been shown that this number is highly influenced by the sequencing technique used.

![rpm formula](https://raw.githubusercontent.com/guillermo-carrasco/bio_data_analysis/master/project/doc/figures/rpm.png)

* Sequencing errors need to be treated as well. Given the fact that both the base error and the position of the error are expected to be random, the distribution of reads with errors is low. **This is why a common step is to eliminate reads with an rpm below certain threshold**. This threshold is usually selected arbitrarily (?).

* **Identification of isoforms:** In order to detect miRNAs, the software miRDeep
uses information about known patterns that the sequencing of these small RNA leave in the sequencing data.

* Several notes on **prediction of miRNA targets**, not much algorithmic detail. Different programs use different metrics, so it is important to run experiment verifications.

* Seems to be useful to compare miRMA expression with mRNA expression analysis, because as miRNA represses the expression of mRNA, an inverse correlation on their expression is expected.

* Tricky: one miRNA can inhibit the expression of several mRNAs, as well as a single mRNA can have several binding sites for one or several miRNAs.

* **TarBase** is used to search for for predicted or experimentally confirmed miRNA.

* Nice figure representing a common workflow for miRNA data analysis:

![Workflow for miRNA data analysis](https://raw.githubusercontent.com/guillermo-carrasco/bio_data_analysis/master/project/doc/figures/miRNA_analysis_workflow.png)

### 2015-02-20

Introduction presentation done.

After the presentation we have set up a couple of times during the following weeks when
we can meet and work together.

I've requested access for Sofia and Yim for our project data to Sverker Lundin at
SciLifeLab, and shouldn't be any problem, just that Sofia and Yim will need to sign an
NDA (I'll send it by mail), and anything we say about the data (organism, etc), we have
to ask to the user.

I had a meeting with Phil Ewels to plan the project a little bit and try to figure
out what can be done in a month (he has been planning it internally). I've created
a [*public trello board*](https://trello.com/b/ilZxZc99/mirna-qc-metrics-project) for
the project plan.

- Use SRA data (just look for miRNA a.k.a small RNA data, and make sure it is human) until they have access
to the real data
- Within the real data, look for human samples
- Literature: Papers within the Pipeline planning document
- To SL: Do we have any crappy data? Can we reschedule the workshop?

### 2015-02-19

Assigned project and project members. My mates will be Sofia Bergström and Yim Wing Chow.

I sent them an email with all the information I have for this project: Project
description and objectives (provisional) for the project. I will prepare the short
presentation for S1 tomorrow and after that we will meet and work around questions.

Proposed Git/GitHub as method for code versioning (strongly recommended) and for
the diary (personal).

Asked in SciLifeLab if it is possible to use customer data for the project. The
answer has been yes, _but_ we have to work around confidentiality issued, Yim and
Sofia will probably have to sign some sort of NDA, to be decided...
