# Larval CADO and Vibrio Genomic Analysis (CH 1 & 2)

Author: Megan Delatte-Guidry

Date: February 2026

### Overview
Bioinformatic analysis of EecSeq data from Larval CADO (ch 1) and Larval Vibrio challenge (ch 2) conducted the summers of 2023 and 2024. Genomic samples were processed for sequencing from fall 2024-summer 2025 using the [EecSeq protocol](https://github.com/amyzyck/RISG_LarvalCADO/blob/main/Analysis/RISG_Larval_Exposure_dDocent_SNPFiltering.md).

Samples processed here were from two projects: (1) Larval oyster CADO experiments on multiple hatchery lines and (2) *Vibrio coralliilyticus* disease challenge on larval oysters following CADO exposures. Samples from these projects were library prepped togehter and will be analyzed together here until SNP calling steps??***

### Chapter 1
Coastal acidification (CA) and hypoxia potentially limit the growth and survival of larvae in urbanized estuaries. These stressors could ultimately impact wild population structure, connectivity, and ecosystem function. Furthermore, it is not well understood how artificially selected lines of bivalves respond to stress as larvae. This study characterized changes in growth, survival, and allele frequencies of oyster larvae pools over a long-term exposure to CA and hypoxia and compared larval responses from different oyster lines. To do so, we built system treatments that mimic the diurnal cycling of pH and DO that occurs in an urbanized estuary throughout a 24-hour cycle. By bubbling in ambient air during the day and N2 and CO2 gas overnight, we achieved maximum values of pH≈7.9-8.1, DO≈7-8 during the day and minimum values of pH≈7, DO≈2.5 at night. Larvae from each line (ARC, NEH, MV) were exposed to 5-7 days of diel cycled stressors (described above). There were triplicate experimental trials for NEH and MV and one experimental trial for ARC. Larval sub-samples were be collected from replicate treatment buckets before and after the exposures for survivorship and growth assessments and genomic analysis. The samples analyzed here were processed with the EecSeq protocol and sequenced at Novogene.

### Chapter 2 
Following the experiments in Chapter 1, some of the surviving larvae from both treatments (ambient and stress) underwent a pathogenic challenge with *Vibrio coralliilyticus* (RE22 strain). Percent mortality was recorded across all treatment groups following the conclusion of the challenge. Genomic samples were also collected at the beginning and end of challenge to test for differential selection. The samples analyzed here were processed with the EecSeq protocol and sequenced at Novogene.

**Details on library preps, QC, and pooling can be found [here](https://drive.google.com/drive/u/1/folders/1a3Utlf2HO-6vMHOi476C0f64TBhEiNaN).**


***All of the following analysis was completed on PLOMEE server, KITT***

File Naming and Information:

location of reference genome on KITT: `/RAID_STORAGE2/Shared_Data/Oyster_Genome/masked/masked.cvir.genome.fasta`

- `masked.cvir.genome.fasta`: Eastern Oyster genome
- `ref_C_virginica-3.0_top_level.gff3`: annotation file for the Eastern Oyster, I also got this from Erin, it has the matching header line convention to work with the above genome


General notes: 

[**Easy Guide to tmux**](https://hamvocke.com/blog/a-quick-and-easy-guide-to-tmux/)
```
#create a new session and run desired command
tmux new -s my_session
your_command

#to detach from the session and have things run in the background
Ctrl + b, then d 
##or type
tmux detach

#list tmux sessions
tmux ls

#reattach to session
tmux attach -t my_session

#kill session (if needed)
tmux kill-session -t my_session
```

-------
## Steps:

1. Demultiplexing
2. Set up 
3. Raw read QC
4. Trimming with fastp
5. Trimmed read QC
6. 
7. 
8. 
9. 

________


## Before you begin...
Make and navigate to new directory within home directory
```{bash}
mkdir /home/mguidry/1_Larval-CADO
cd /home/mguidry/1_Larval-CADO
```

Install Bioconda (if needed) and create conda environment & install packages
```{bash}
# downloading Miniconda software
$ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
$ chmod +x Miniconda3-latest-Linux-x86_64.sh
$ ./Miniconda3-latest-Linux-x86_64.sh

# restarting window with source command
$ source ~/.bashrc

# adding different channels
$ conda config --add channels defaults
	# should get: "warning: 'defaults' already in 'channels' list, moving to the top"
$ conda config --add channels bioconda
$ conda config --add channels conda-forge

# to see if this worked with cat command
$ cat .condarc
```
> Bioconda is a bioinformatics software package manager. See more at https://bioconda.github.io.

```{bash}
#installing mamba because conda was taking forever
conda install mamba -c conda-forge

mamba create -n larvae ddocent multiQC
conda activate larvae

#followed prompts to initialize mamba
```
`conda list` will allow you to look at all of the packages you have installed in your environment.

## 1. Demultiplexing

**QUESTIONS FOR JON:**
- I thought these data were beind demultiplexed by novogene per emails in October?
- Where on KITT to do demultiplexing? In a RAID STORAGE and not home/?
- Use STACKS ??

Before proceeding with analysis reads will have to be demultiplexed, meaning assigning sample specific reads using the index pairs assigned at library prep and pooling steps.  

Multiplexed files are located in `/RAID_STORAGE2/Raw_Data/ASMFC_EECSEQ/01.RawData`

```{bash}
ll
```

```
drwxr-xr-x 2 root root 4096 Oct  7 05:18 i506_i706
drwxr-xr-x 2 root root 4096 Oct  7 05:18 i506_i707
drwxr-xr-x 2 root root 4096 Oct  7 05:19 i506_i708
drwxr-xr-x 2 root root 4096 Oct  7 05:19 i506_i712
drwxr-xr-x 2 root root 4096 Oct  7 05:20 i508_i706
drwxr-xr-x 2 root root 4096 Oct  7 05:21 i508_i707
drwxr-xr-x 2 root root 4096 Oct  7 05:23 i508_i708
drwxr-xr-x 2 root root 4096 Oct  7 05:24 i508_i712
drwxr-xr-x 2 root root 4096 Oct  7 05:21 i509_i706
drwxr-xr-x 2 root root 4096 Oct  7 05:22 i509_i707
drwxr-xr-x 2 root root 4096 Oct  7 05:22 i509_i708
drwxr-xr-x 2 root root 4096 Oct  7 05:23 i509_i712
drwxr-xr-x 2 root root 4096 Oct  7 05:24 i511_i706
drwxr-xr-x 2 root root 4096 Oct  7 05:25 i511_i707
drwxr-xr-x 2 root root 4096 Oct  7 05:26 i511_i708
drwxr-xr-x 2 root root 4096 Oct  7 05:27 i511_i712
drwxr-xr-x 2 root root 4096 Oct  7 05:27 i512_i706
drwxr-xr-x 2 root root 4096 Oct  7 05:29 i512_i707
drwxr-xr-x 2 root root 4096 Oct  7 05:26 i512_i708
drwxr-xr-x 2 root root 4096 Oct  7 05:27 i512_i712
drwxr-xr-x 2 root root 4096 Oct  7 05:12 Probes_501_701
drwxr-xr-x 2 root root 4096 Oct  7 05:12 Probes_501_703
drwxr-xr-x 2 root root 4096 Oct  7 05:13 Probes_501_704
drwxr-xr-x 2 root root 4096 Oct  7 05:13 Probes_501_705
drwxr-xr-x 2 root root 4096 Oct  7 05:12 Probes_501_710
drwxr-xr-x 2 root root 4096 Oct  7 05:13 Probes_502_701
drwxr-xr-x 2 root root 4096 Oct  7 05:14 Probes_502_703
drwxr-xr-x 2 root root 4096 Oct  7 05:14 Probes_502_704
drwxr-xr-x 2 root root 4096 Oct  7 05:14 Probes_502_705
drwxr-xr-x 2 root root 4096 Oct  7 05:15 Probes_502_710
drwxr-xr-x 2 root root 4096 Oct  7 05:15 Probes_503_701
drwxr-xr-x 2 root root 4096 Oct  7 05:15 Probes_503_702
drwxr-xr-x 2 root root 4096 Oct  7 05:16 Probes_503_703
drwxr-xr-x 2 root root 4096 Oct  7 05:16 Probes_503_704
drwxr-xr-x 2 root root 4096 Oct  7 05:16 Probes_504_701
drwxr-xr-x 2 root root 4096 Oct  7 05:17 Probes_504_703
drwxr-xr-x 2 root root 4096 Oct  7 05:17 Probes_504_704
drwxr-xr-x 2 root root 4096 Oct  7 05:16 Probes_504_710
drwxr-xr-x 2 root root 4096 Oct  7 05:17 Undetermined
```

Captured libraries are in the i50#_i70# directories. 
Unfortunately a good amount of probes remained in the pools and were sequenced as well - these are labeled with "Probes_".
The Undetermined directory contains reads that could not be resolved into either captured library indices or probe indicies.

> **Note!** The 710 probe files need to be renamed with 702. They were mislabeled in the table sent to novogene upon discovery of the unexpected probes in the sequencing run. 

Each of the captured library files (ex. i506_i706) contains 4-5 samples. These are identified down to the sample with the addition of an adapter sequence. 

Inside of each of these files is set of fwd and rev read fastq files labeled with 1 and 2 to indicate the read. 

> for example: 
> i506_i706_WKDL250004555-1A_22W7JGLT4_L7_1.fq.gz
> i506_i706_WKDL250004555-1A_22W7JGLT4_L7_2.fq.gz

U