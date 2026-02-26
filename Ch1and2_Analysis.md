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

1. 
2. 
3. 
4. 
5. 
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
*see [Demultiplex.md](/Demultiplex.md) for details*

Demultiplexed in `RAIDSTORAGE3`

```
mkdir /home/mguidry/1_Larval-CADO/raw_seq
cd raw_seq
# link demultiplexed fastq files
ln -s /RAID_STORAGE3/mguidry/demux_fastq/*fastq.gz .
ls -1 | wc -l  #output: 182 (yay!)
```

## 2. Raw reads FastQC & MultiQC report

### FastQC
FastQC is a program designed to visualize the quality of high throughput sequencing datasets. The report will highlight any areas where the data looks unusual or unreliable.
```
mkdir /home/mguidry/1_Larval-CADO/fastqc_raw
cd fastqc_raw

#run the following in tmux session - used two (one for FWD and one for REV)

conda activate larvae
cd raw_seq
fastqc -o /home/mguidry/1_Larval-CADO/fastqc_raw/ ./*F.fastq.gz #11AM start
fastqc -o /home/mguidry/1_Larval-CADO/fastqc_raw/ ./*R.fastq.gz #11AM start

# check progress
ls -1 | wc -l 

# total number of fastqc files expected = 364
# will have an html and zip file for each sample
# 182 samples * 2 fastqc files per sample = 364
```

### Multiqc report
Ran multiqc to generate a readable report to investigate the quality of the sequence data. Ran in the directory with the fastqc output files.

```
conda activate larvae
cd fastqc_raw
multiqc .
```

The multiqc command generates multiqc_data directory and multiqc_report.html. The .html report file can be transferred to local computer or to github and visualized on a web browser.

**REVIEW MULTIQC REPORT HERE!!!**


## 3. Trimming raw reads, mapping to reference genome, and SNP calling with dDocent

NEXT STEPS:
- update raw read names to fit [dDocent naming convention](https://ddocent.com/UserGuide/#naming-convention)!!
- make config file for dDocent
- trim raw reads, mapping, and SNP calling with dDocent  
	- no to assembly bc we have a reference genome 👍🏻
- SNP filtering (once I have the VCF)*
- ANALYSIS! Yay!

**QUESTIONS FOR JON:** 
- Look at read quality 
- Should I run trimming, mapping and SNP calling all in one dDocent run? or is there a reason to do it step-wise?
- Should I first test mapping on a subset first to optimize? or just go for it with default BWA parameters? 
	- optimizing with samtools flagstats
- VCF Filtering - use the `TotalRawSNPs.vcf` *NOT* `Final.recode.vcf`?? 
	- `Final.recode.vcf` is more useful for comparing different pipeline runs
	- but it is also a filtered snp data set?? 
	- i am confused about the difference between these two VCFs
- **FILL IN QUESTIONS ON VCF FILTERING!!**
- Compressed filtered VCF (*.vcf.gz) is what I'll use for PCAdapt and other analyses yes??
- ANALYSES!
	- PCA for a first look
	- FILL THIS IN TOO!!



Trimming with dDocent vs. trimming outside of dDocent. Since data looks relatively good and we don't have any nonstandard concerns, we can proceed with trimming in dDocent just to make it as straightforward as possible.

[dDocent](https://ddocent.com/quick/) website with more info!

```
cd Shared_Data/ROD_CADO
conda activate ROD_CADO
mkdir analysis
cd analysis
ln -s ../dDocent_ngs .  #link dDocent file into this new analysis directory
ln -s ../raw_seq/*.fq.gz #link raw seq files into analysis directory
ln -s ~/eager_obj1b/Genome/masked.* refernce.fasta #link new haplotig masked genome into directory and name it reference.fasta (from JMG previous directory)
#nano config.file #dDocent always needs a `config.file` to run with instructions on how to complete the run -OR- you can do interactive prompts (we did interactive prompts) 
./dDocent_ngs

# prompts below come up
processors: 48
trim?: yes
perform assembly?: no
map reads? yes
new parameters for BWA? no 
call SNPS? no
enter email # this will run a while!
ctrl+z 
bg
disown -h 
top #shows you programs running currently - press q to leave
tail temp.LOG #shows you progress of read trimming
```

dDocent was set to trim (take off bad basepairs) and map with default bwa mem parameters. Mapped reads were then marked for duplicated with picard then samtools was used to filter out duplicated and select for reads with a mapping quality above 10