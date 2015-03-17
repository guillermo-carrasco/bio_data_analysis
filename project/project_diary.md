# Project diary

### 2015-03-17

**UPPMAX is totally unaccessible...**

Uppmax has had a major hardware issue and has been unabailable all the morning.
I have lots of jobs in queue which estmated time of start is N/A. In production we
have a dedicated cluster called Nestor that is going on maintenance tomorrow, but
with luck, if I submit short jobs with _our_ pipeline, it will execute them (our
pipeline analyses _per sample_, so it shouldn't take more than 5h per job).

I will transfer the data to our project directory on nestor and try to launch the jobs.

Data is there. Now what I have done is written this short bash script that will run
cutadapt and FastQC on each sample:

```bash
#!/bin/bash

#SBATCH -p core -n 8
#SBATCH -t 00:30:00
#SBATCH -A a2010002

module load bioinfo-tools
module load cutadapt
module load FastQC

PROJECT_HOME="/proj/a2010002/nobackup/BB2490_KTH_miRNA_project/src/bio_data_analysis/project"
DATA_DIR="/proj/a2010002/nobackup/BB2490_KTH_miRNA_project/data"
RESULTS_DIR=${PROJECT_HOME}/results/$(date +%Y-%m-%d)

# Prepare directories
project=$1
sample=$2
mkdir -p ${RESULTS_DIR}/${project}/${sample%.*}/FastQC

# Run cutadapt
cutadapt -f fastq -a TGGAATTCTCGGGTGCCAAGG -q 10 -O 3 -m 18 -o ${RESULTS_DIR}/${project}/${sample%.*}/${sample%.*}_trimmed.fastq  ${DATA
_DIR}/${project}/${sample} 2> ${RESULTS_DIR}/${project}/${sample%.*}/${sample%.*}_cutadapt.out

# Run FastQC
fastqc -o ${RESULTS_DIR}/${project}/${sample%.*}/FastQC  ${RESULTS_DIR}/${project}/${sample%.*}_trimmed.fastq
```

And called it like this, on each project directory

```bash
for sample in `ls *fastq*`; do sbatch -J $sample cut_and_fas.sh <project_name> $sample; done
```


### 2015-03-16

I’ve been talking with Phil this morning, and we’ve concluded that, given the very short time we have, we have to focus on what we have.

* The heatmap
* Contamination screening

**The heatmap**
There are a couple of things that need to be fixed for the heatmap, but specially
the color scale, it is pretty difficult to appreciate any difference with green
taking most of the scale. Also, usually more density implies a darker color.
What about a white to red gradual scale?

Also, I’m afraid that we don’t trust that much fastqx and how Marc is filtering the reads.
It is basically discarding everything longer than 35bp, which doesn’t help us much
on knowing how our data looks like. We have bad libraries and we know it, so a good
point would be to try to understand how bad they are, and conclude with something like:
We accept all libraries which % of reads longer than 25bp is < X.

Now what we should do is go back to where we started: cutadapt + FastQC.
I’ve already launched jobs in Uppmax for all our samples, but the estimated starting
 dates scare me… if by tomorrow none of them have started I’ll see what I can do.
 I don’t discard submitting a couple of jobs to Amazon or similar if the data transfer
 prices allows me to do it.

**Contamination screening**
This is quite useful, actually if you take a look at the contamination results for
peoject1 you’ll see that most of the reads are mapped to birds/reptiles. This is actually
because the samples are from non-human data. So this is expected, but is a quick and
simple check to avoid confusions.

### 2015-03-15

Jobs for 5/6 projects have finished, so we can start taking a look to those projects while the other one finishes. Copying the results locally for further analysis with `rsync -rvR --exclude="*.fa" --exclude="*.bwt" --exclude="*.ebwt" --exclude="*.fastq" --exclude="intensities" --exclude="*.arf" --exclude="*.tmp" --exclude=".bed" --exclude="*.tmp2" --exclude="*fa*" --exclude="*.fq" --exclude="tmp" --exclude="pre-processing" --exclude="*.converted" guilc@milou-b.uppmax.uu.se:/proj/b2013064/nobackup/BB2490_KTH_miRNA_project/data/[A-Z].* .`

### 2015-03-14

The pipeline tries to create the directories necessary for the analysis, and if they
already exist (which is the case), it crashes instead of overwriting the results. So
I have to remove the directories: `progress, contamination, breakdown_basic, summary` and `exogen`.

- Controlling contaminations step worked!
- enacting genome is working as well, but getting this error: `(in cleanup) Internal error: could not get STATE from IPC::Run`
(this is not a real problem, basically a lot of intermediate files will remain there)

**EXECUTION OK!** will launch jobs for all other projects, after removing all other directories.

Now, to wait again...

### 2015-03-13

Checking the pipeline logs we've seen lots of errors, the first one of them is a
conflict loading bowtie 0.12.6. I don't thin that this is a problem, as this is due to
the pipeline loading previously bowtie 1.1.0.

**Pre-processing data and controlling quality** do not raise any error.

**controlling contaminants**

Lots of errors in the reports generation: `Error in library(plotrix) : there is no package called ‘plotrix’`

I have installed the R package `plotrix`:

```bash
module load R/3.10.
> install.packages("plotrix")
```

**plotting lengths, enacting mirdeep2, enacting seqBuster, mapping to genome and calculating intensities**
do not raise any errors.

**breaking down annotation basic**, same `plotrix` error.

**enacting exogen**

```
Can't locate Statistics/R.pm in @INC (@INC contains: /sw/apps/bioinfo/mirdeep2/2.0.0.5/milou/bin/lib/x86_64-linux-thread-multi /sw/apps/bioinfo/mirdeep2/2.0.0.5/milou/bin/lib /home/guilc/opt/perl/lib/perl5/x86_64-linux-thread-multi /home/guilc/opt/perl/lib/perl5 /home/guilc/opt/perl/lib/perl5/x86_64-linux-thread-multi /home/guilc/opt/perl/lib/perl5 /usr/local/lib64/perl5 /usr/local/share/perl5 /usr/lib64/perl5/vendor_perl /usr/share/perl5/vendor_perl /usr/lib64/perl5 /usr/share/perl5 .) at /gulo/proj_nobackup/b2013064/BB2490_KTH_miRNA_project/smartar/EXOGEN/exogen_plot_v1.pl line 7.
```

Installed `cpanm Statistics::R`, should solve the problem.

So basically the steps that have failed have been: Controlling contaminants, breaking down
annotation analysis and enacting exogen.

Wil try to re-run the pipeline only executing these steps, i.e excluding all the
others. Modified `run_smartar.sh` to run the pipeline with the following parameters:
`perl $2 config.txt -s -t -u -v -j -k -m -n -o -p -q -r -s -t -u`, testing on
project 1 now.

```bash
sbatch -J SMARTAR_A.Simon_14_01 -o ../results/$p/SMARTAR_p1.out -e ../results/$p/SMARTAR_p1.err run_smartar.sh p1 $SMARTAT_PATH
```

(Execution time one day)

### 2015-03-12

SMARTAR miRNA pipeline workflow:

(You can skip any of the pipeline steps by using the command line options available)

1. **Define static files and code locations**: Defines where the reference fasta
files are, the indexes, annotation files, source codes for generating plots, etc.
_Important to note_ that all the paths are relative to the pipeline main script,
so this structure is strict:

    ```
    (master)guilc@milou-b:/proj/b2013064/nobackup/BB2490_KTH_miRNA_project/smartar$ tree -L 1
    .
    ├── EXOGEN
    ├── human_data
    ├── mouse_data
    ├── SMARTAR_mouse
    ├── SMARTAR_mouse_v1.0.9.pl
    ├── SMARTAR_nematode
    ├── SMARTAR_source
    ├── SMARTAR_static
    ├── SMARTAR_v1.0.9.pl
    ```

2. **Define names and variables:** For use in future references, like for example
the TrueSeq small RNA Illumina adapter sequence `TGGAATTCTCGGGTGCCAAGG`

3. **Parse configuration:** Creates `progress` directories and checks the tabular
configuration file.

4. **Preprocess data:** [FASTX-Toolkit](http://hannonlab.cshl.edu/fastx_toolkit/)

    * converts Sanger phred encoding to illumina encoding for use with the fastx suite
    * truncates the reads down to length 36 nts --> **uses:** `fastx_trimmer -f 1 -l 36`
    * removes reads which consists only of homo-nts (will still be filtered if three
    or less nts are different from the homo-nts) --> **uses:** `fastx_artifacts_filter`
    * remove reads where more than 50% of the nts have less than 10 phred quality.
    **uses:** `fastq_quality_filter -q 10 -p 50`
    * removes adapters with adrec (8 nt prefix, max 1 mismatch, some low-complexity filtering).
    **uses:** `AdRec.jar` _Not really sure what this is, haven't found information_
    * parses the tabular output format of adrec to mirdeep2 fasta format. **uses:** `adrec_to_fasta.pl`
    * discards reads shorter than 18 nts and maps the remaining against the genome for use for mirdeep2.
    **uses:** a custom script called `mapper.pl`
    * merges all resulting FASTA files.

5. **Control quality:** _This is the one we are most interested in_

    It uses two binaries called `fastx_quality_stats` and `fastq_quality_boxplot_graph.sh` that I don't
    really know what they are.

6. **Control contamination:** Uses the perl script `contamination_v4.pl`, wich detects clade-specific miRNAs.
Creates figures and tables for each FASTA file.

7. **Plot lengths:** Will plot length distributions.

8. **Queries [miRDeep2](https://www.mdc-berlin.de/8551903/en/)**: miRDeep2 is a
completely overhauled tool which discovers microRNA genes by analyzing sequenced RNAs.
The tool reports known and hundreds of novel microRNAs with high accuracy in seven
species representing the major animal clades.

9. **Queries miRBase:** Using [SeqBuster](https://github.com/lpantano/seqbuster)

10. **Generate opt files:** _Don't know what this is..._

11. **Map to genome:** Aligns the reads to the reference Genome using Bowtie (1)

12. **Calculate intensities:** Uses custom perls scripts, _not sure what it does_...

13. **Break down annotation, annotation basic and annotation detailed**: _don't
know what this is..._

14. **Construct table:** Constructs annotation tables.

15. **Make bed Graphs**

16. **Run SeqCluster:** Not much information about this...

17. **Exogen diagnose:** Running a custom stript as well..

18. Finall summary

### 2015-03-09

Details about the poster session next week in the course literature.

### 2015-03-08

Jobs were canceled due to time limit... have to re-run them with a higher time
limit. Re-queued them.

### 2015-03-07

In order to solve the space problems **and** the privacy problems, Phil gave us access
to the applications project, `b2013064`, so that we can put our data and results there.

Due to a [hardware problem](http://www.uppmax.uu.se/system-news/hardware-related-problems-with-gulo-glob-and-some-nobackup) that Uppmax had a few weeks ago, we have some data corruption for
some samples in some projects. However, for the scope of this project we have
enough data. This is the final dataset that we are going to analyze:

* 6 projects
* 113 samples in total
* 294 fastq files in total
* 45 GB of data in total

**Bash tricks**:

To count the number of samples within a project directory:

Given the following FASTQ naming format `SAMPLE_NAME_MORE_FIELDS.fastq.gz`

```bash
$> ls <project_dir> --color=never | cut -f 1,2 -d'_' | uniq -c
```

Count the number of files in a directory (including subdirs) following a pattern:
`find . -type f -name *fastq* | wc -l`

##### Running the pipeline

* Pipeline is located in `/proj/b2013064/nobackup/BB2490_KTH_miRNA_project/smartar`
* Project data located in `/proj/b2013064/nobackup/BB2490_KTH_miRNA_project/data`

The pipeline is written in Perl, so first I have to install perl dependencies.
[Howto here](http://www.uppmax.uu.se/faq/installing-local-perl-packages).

Installing perl dependencies:

```
$> cpanm Parallel::ForkManager
```

And this is the pipeline usage:

```
SMARTAR_v1.0.9.pl config_file

Evokes the full sRNA analysis.
The config file should contain a tab separated list
of fastq datasets and corresponding three-letter tags.

-d directory to source
-e directory to static files
-f adapter sequence
-g illumina phred encoding
-j omit pre-processing
-k omit quality test
-l omit contamination test
-m omit lengths
-n omit mirdeep2
-o omit seqbuster
-p omit mapping
-q omit intensities
-r omit simple annotation
-s omit vanilla annotation
-t omit detailed annotation
-u omit bedgraph files
-v omit seqcluster
-x omit exogen
-y omit summary
-z clean up
```

In order to run the pipeline, we need to create a `config.txt` file. This file is a
2-column tab delimited file which's first column is the name of a fastq file and the
second column is a 3-letter id. I'll name the fastq files like F01, F02, etc..

On each project directory, I've run the one-liner to construct the `config.txt` file:

```bash
n=`ls -l | wc -l` && i=1 && for fastq in `find . -type f | sed 's|./||'`; do id=F$(printf "%02d" $i) && i=`expr $i + 1` && echo -e $fastq'\t'$id >> config.txt; done
```

Which will create a file like this:

```
P962_103_TTAGGC_L001_R1_001.fastq.gz    F01
P962_105_ACAGTG_L001_R1_001.fastq.gz    F02
P962_101_ATCACG_L002_R1_001.fastq.gz    F03
P962_111_GGCTAC_L002_R1_001.fastq.gz    F04
P962_106_GCCAAT_L001_R1_001.fastq.gz    F05
P962_108_ACTTGA_L001_R1_001.fastq.gz    F06
P962_104_TGACCA_L001_R1_001.fastq.gz    F07
P962_110_TAGCTT_L001_R1_001.fastq.gz    F08
P962_107_CAGATC_L002_R1_001.fastq.gz    F09
P962_112_CTTGTA_L002_R1_001.fastq.gz    F10
P962_106_GCCAAT_L002_R1_001.fastq.gz    F11
P962_109_GATCAG_L002_R1_001.fastq.gz    F12
P962_102_CGATGT_L001_R1_001.fastq.gz    F13
P962_103_TTAGGC_L002_R1_001.fastq.gz    F14
P962_107_CAGATC_L001_R1_001.fastq.gz    F15
P962_105_ACAGTG_L002_R1_001.fastq.gz    F16
P962_110_TAGCTT_L002_R1_001.fastq.gz    F17
P962_109_GATCAG_L001_R1_001.fastq.gz    F18
P962_101_ATCACG_L001_R1_001.fastq.gz    F19
P962_108_ACTTGA_L002_R1_001.fastq.gz    F20
P962_111_GGCTAC_L001_R1_001.fastq.gz    F21
```

After creating all configuration files, I've ran the pipeline for all projects
with the following command:

```
for p in `ls -d --color=never [A-Z].*`; do mkdir ../results/$p && sbatch -J SMARTAR_$p -o ../results/$p/SMARTAR_$p.out -e ../results/$p/SMARTAR_$p.err run_smartar.sh $p $SMARTAT_PATH ; done
```

So they are being analyzed now:

```
(master)guilc@milou-b:/proj/b2013064/nobackup/BB2490_KTH_miRNA_project/data$ jobinfo -u guilc

CLUSTER: milou
Running jobs:
   JOBID PARTITION                      NAME     USER        ACCOUNT ST          START_TIME  TIME_LEFT  NODES CPUS NODELIST(REASON)
 4812486      core     SMARTAR_A.Simon_14_01    guilc       b2013064  R 2015-03-07T13:21:54    5:54:39      1    1 m158
 4812487      core  SMARTAR_C.Dixelius_13_05    guilc       b2013064  R 2015-03-07T13:21:54    5:54:39      1    1 m158
 4812488      core SMARTAR_J.Lundeberg_14_18    guilc       b2013064  R 2015-03-07T13:21:54    5:54:39      1    1 m164
 4812490      core   SMARTAR_O.Larsson_14_04    guilc       b2013064  R 2015-03-07T13:21:54    5:54:39      1    1 m167
 4812491      core SMARTAR_U.Pettersson_14_0    guilc       b2013064  R 2015-03-07T13:21:54    5:54:39      1    1 m167
 4812494      core    SMARTAR_N.Street_13_01    guilc       b2013064  R 2015-03-07T13:27:10    5:59:55      1    1 m164

```

### Problem
The pipeline does not accept compressed FASTQ files... so I have to uncompress them and
re-run the analysis


### 2015-03-05

We attended a miRNA seminar given by [Marc Friedländer](http://www.scilifelab.se/researchers/marc-friedlander/).
It was of high interest to us as we he has been studying miRNA for 9 years.

After the seminar we had a small informal chat with Marc in where we explained
our project. He offered us his pipeline, which is functional, so that we can focus
on the results. We also showed him some results and that was helpful. This is how we
will proceed now, given the time we have:

* Guillermo:
    * Collect more data from all possible miRNA projects in production/applications group.
    * Run SMARTAR (Marc's pipeline) on all our samples
    * Make results accessible to Sofia/Yim
* Sofia and Yim
    * Experiment with the results that we already have to construct a heatmap for
    the lengths distributions, try to cluster per-project if possible.
* Everyone:
    * Just... keep studying the results.

### 2015-03-03

Second seminar presentation today. Slides in the repo `project/doc/presentations`.


### 2015-03-02

Running the pipeline on all the data filled my home directory pretty quickly so
the job was killed and the results lost. I have then moved the data to the project
directory and will redirect the output to my home, should fit, hopefully.

Also, found some bugs in the sbatch script that was not creating the output directory
as I wanted, fixed them, new version in GitHub.

Ran the pipeline using [this](https://github.com/guillermo-carrasco/bio_data_analysis/blob/master/project/bin/pipeline_sbatch.sh) sbatch script, waiting for the results...

Commands ran (inside the `results/2014-03-02`) directory:

```bash
for i in {101..114}; do s=P1385_${i}; sbatch -J ${s}_miRNA -e ${s}_miRNA.err -o ${s}_miRNA.out ../../bin/pipeline_sbatch.sh $s <project_name>; done
```

(project name correspond to each of the three projects we are working with)

And jobs are running...

```
(master)guilc@milou-b:~/repos_and_codes/bio_data_analysis/project/results/2015-03-02 (master)$ jobinfo -u guilc

CLUSTER: milou
Running jobs:
   JOBID PARTITION                      NAME     USER        ACCOUNT ST          START_TIME  TIME_LEFT  NODES CPUS NODELIST(REASON)
 4783781      core           P1385_101_miRNA    guilc       g2015009  R 2015-03-02T16:31:29    4:37:50      1    8 m118
 4783782      core           P1385_102_miRNA    guilc       g2015009  R 2015-03-02T16:31:29    4:37:50      1    8 m118
 4783783      core           P1385_103_miRNA    guilc       g2015009  R 2015-03-02T16:31:29    4:37:50      1    8 m65
 4783785      core           P1385_105_miRNA    guilc       g2015009  R 2015-03-02T16:31:29    4:37:50      1    8 m87
 4783786      core           P1385_106_miRNA    guilc       g2015009  R 2015-03-02T16:31:29    4:37:50      1    8 m85
 4783784      core           P1385_104_miRNA    guilc       g2015009  R 2015-03-02T16:31:29    4:37:50      1    8 m180
 4783787      core           P1385_107_miRNA    guilc       g2015009  R 2015-03-02T16:32:31    4:38:52      1    8 m60
 4783788      core           P1385_108_miRNA    guilc       g2015009  R 2015-03-02T16:32:31    4:38:52      1    8 m67
 4783789      core           P1385_109_miRNA    guilc       g2015009  R 2015-03-02T16:33:31    4:39:52      1    8 m54
 4783790      core           P1385_110_miRNA    guilc       g2015009  R 2015-03-02T16:34:32    4:40:53      1    8 m22
 4783791      core           P1385_111_miRNA    guilc       g2015009  R 2015-03-02T16:34:32    4:40:53      1    8 m100
 4783792      core           P1385_112_miRNA    guilc       g2015009  R 2015-03-02T16:34:32    4:40:53      1    8 m70
 4783793      core           P1385_113_miRNA    guilc       g2015009  R 2015-03-02T16:34:32    4:40:53      1    8 m189
 4783794      core           P1385_114_miRNA    guilc       g2015009  R 2015-03-02T16:34:32    4:40:53      1    8 m84
 4783796      core           P1381_101_miRNA    guilc       g2015009  R 2015-03-02T16:34:32    4:40:53      1    8 m208
 4783797      core           P1381_102_miRNA    guilc       g2015009  R 2015-03-02T16:35:05    4:41:26      1    8 m184
 4783798      core           P1381_103_miRNA    guilc       g2015009  R 2015-03-02T16:35:05    4:41:26      1    8 m96
 4783799      core           P1381_104_miRNA    guilc       g2015009  R 2015-03-02T16:35:20    4:41:41      1    8 m197
 4783800      core           P1381_105_miRNA    guilc       g2015009  R 2015-03-02T16:36:21    4:42:42      1    8 m32
 4783801      core           P1381_106_miRNA    guilc       g2015009  R 2015-03-02T16:37:03    4:43:24      1    8 m105
 4783802      core           P1381_107_miRNA    guilc       g2015009  R 2015-03-02T16:37:18    4:43:39      1    8 m86
 4783803      core           P1381_108_miRNA    guilc       g2015009  R 2015-03-02T16:38:10    4:44:31      1    8 m33
 4783804      core           P1381_109_miRNA    guilc       g2015009  R 2015-03-02T16:38:59    4:45:20      1    8 m52
 4783805      core           P1381_110_miRNA    guilc       g2015009  R 2015-03-02T16:40:12    4:46:33      1    8 m82
 4783806      core           P1381_111_miRNA    guilc       g2015009  R 2015-03-02T16:40:38    4:46:59      1    8 m45
 4783807      core           P1381_112_miRNA    guilc       g2015009  R 2015-03-02T16:41:35    4:47:56      1    8 m85
 4783808      core           P1381_113_miRNA    guilc       g2015009  R 2015-03-02T16:41:57    4:48:18      1    8 m98
 4783809      core           P1381_114_miRNA    guilc       g2015009  R 2015-03-02T16:41:57    4:48:18      1    8 m63
 4783810      core           P1381_115_miRNA    guilc       g2015009  R 2015-03-02T16:42:14    4:48:35      1    8 m83
 4783811      core           P1381_116_miRNA    guilc       g2015009  R 2015-03-02T16:42:17    4:48:38      1    8 m172
```

**Update**: Jobs have failed in the htseq_counts step, but at least we've got the
FastQC data for all the samples, results directory updated. Command used to unzip
all results at once:

```
for d in `ls -d --color=never project*/*out/FastQC`; do cd $d && unzip *zip && rm *zip && cd ../../..; done
```

Preparing the presentation for tomorrow.

### 2015-02-28

I've found the data for the third project :-) New dataset is for this project is:

* 16 samples
* 62 FASTQ files (several samples ran on multiple lanes, single ended reads)
* 5.6GB more data


### 2015-02-28

Exploring [cutadapt](https://github.com/marcelm/cutadapt) for adapter sequence trimming.
After the first test analysis with FastQC it is clear that the first step to carry on is adapter trimming. Cutadapt has a **long** help string... There is an example in which apparently you have to specify the adapter sequence, that we
don't know..


>Assuming your sequencing data is available as a FASTQ file, use this
command line:
`$ cutadapt -e ERROR-RATE -a ADAPTER-SEQUENCE input.fastq > output.fastq`

I'll test just with one sample and see what comes out: `cutadapt 1_140828_AHA36KADXX_P1185_402_1.fastq.gz > cutadapt/1_140828_AHA36KADXX_P1185_402_1.fastq` and precisely, you need to provide at least one adapter sequence.

You only need the adapter that was ligated to the 3' end of the sequence:

```
-a ADAPTER, --adapter=ADAPTER
                        Sequence of an adapter that was ligated to the 3' end.
                        The adapter itself and anything that follows is
                        trimmed. If the adapter sequence ends with the '$'
                        character, the adapter is anchored to the end of the
                        read and only found if it is a suffix of the read.
```

I've ran the program with the adapter sequence `TGGAATTCTCGGGTGCCAAGG` (which
I've found that they use as default [here](https://github.com/ewels/miRNA_processing/blob/master/pipeline.py#L204)), until I discover which is the real adapter sequence.

`cutadapt -a TGGAATTCTCGGGTGCCAAGG 1_140828_AHA36KADXX_P1185_402_1.fastq.gz > cutadapt/1_140828_AHA36KADXX_P1185_402_1.fastq 2> cutadapt/1_140828_AHA36KADXX_P1185_402_1.stats`

The program gives you some nice stats that you can find [here](https://raw.githubusercontent.com/guillermo-carrasco/bio_data_analysis/master/project/results/2015-02-28/1_140828_AHA36KADXX_P1185_402_1_cutadapt_stats.stats) for this particular sample with that particular adapter.

One interesting point is the number of trimmed reads, which is 52.6%, **maybe if we look for the reverse complement of the adapter we'll find more?**. TODO/To research.

Just to see the difference, I've ran fastqc 0.11.2 again against that sample **after** trimming. The results are quite different, for example I've got a very different length distribution:

![Length distribution after trimming](https://raw.githubusercontent.com/guillermo-carrasco/bio_data_analysis/master/project/results/2015-02-28/1_140828_AHA36KADXX_P1185_402_1_fastqc_0.11.2_after_trimming/Images/sequence_length_distribution.png)

This is still quite bad, as it looks like most of the reads are still 48-51 nucleotides long, even though now we have a small pick (+1 million reads) of reads with length 18-25, which is what we want.

**Question:** Is this because the data is bad? Should we play more with cutadapt options?

**NOTE**: The data has been sequenced using the Illumina Kit TrueSeq small RNA, and looking at [the documentation](http://supportres.illumina.com/documents/documentation/chemistry_documentation/experiment-design/illumina-customer-sequence-letter.pdf), in page 15 I discovered that the sequence we are using as default is precisely the Illumina adapter for this protocol.

[Phil's miRNA pipeline](https://github.com/ewels/miRNA_processing) does all what we need. After understanding the
tools it uses, we should use this pipeline and focus on the results.

I am going to try to find more data we can use. There is more data from one of the project that is corrupted due
to an Uppmax data loss, I'll try to recover it and reprocess it from our backups... Found the two runs that have the third's project data in swestore. Will try to fetch and process them.

Trying `miRNA_processing` pipeline

### 2015-02-26

I have copied all raw project data to my home directory in Uppmax to be able to share it with Sofia and Yim, the data consists on:

* 2 projects
* 18 samples
* 8 FASTQ files for the first project (paired end reads)
* 56 FASTQ files for the second project (all samples ran in 2 lanes, paired end reads)
* 19 GB total amount of data

As a small test, ran fastQC in one sample, got weird results. For example there seem to be an excellent read quality:

![Read quality](https://raw.githubusercontent.com/guillermo-carrasco/bio_data_analysis/master/project/results/2015-02-26/1_140828_AHA36KADXX_P1185_402_1_fastqc_0.7/Images/per_base_quality.png)

But the sequence length distribution doesn't correspond to the expected length of miRNA data:

![Length distribution](https://raw.githubusercontent.com/guillermo-carrasco/bio_data_analysis/master/project/results/2015-02-26/1_140828_AHA36KADXX_P1185_402_1_fastqc_0.7/Images/sequence_length_distribution.png)

However that may be adapter contamination, even though on this example run of FastQC it doesn't seem to detect a lot of adapter sequences. Will run `cutadapt` first.

GC content seems pretty bad as well...

![GC content](https://raw.githubusercontent.com/guillermo-carrasco/bio_data_analysis/master/project/results/2015-02-26/1_140828_AHA36KADXX_P1185_402_1_fastqc_0.7/Images/per_sequence_gc_content.png)

**NOTE**: That I ran an old version (0.7) of FastQC, load the more recent one with `module load FastQC/0.10.1`

**Meeting with Sofia and Yim**

We have been talking about how to organize the project, we've decided to use [Trello](https://trello.com/b/ilZxZc99/mirna-qc-metrics-project) to
organize tasks and ideas.

It is difficult to organize the project given the short time that we have... We don't
have very clear what can be a realistic goal for the project. To begin with, we will
start by trying the selected tools with the project data, just to see what kind of
results we get.

A more precise organization is in Trello, but basically we've divided the tools
we are going to test between us, and we will share results in Trello/GitHub

I gave Sofia and Yim a brief introduction to Git/GitHub, they are really wanting to
learn :-), problem is again the short time we have for this project. We will see.

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
