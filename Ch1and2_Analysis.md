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
fastqc -o /home/mguidry/1_Larval-CADO/fastqc_raw/ ./*F.fastq.gz #11AM start - 4:30PM end
fastqc -o /home/mguidry/1_Larval-CADO/fastqc_raw/ ./*R.fastq.gz #11AM start - 4:30PM end

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

cd multiqc_data
```

The multiqc command generates multiqc_data directory and multiqc_report.html. The .html report file can be transferred to local computer or to github and visualized on a web browser.


At first glance, things look pretty good!

Highest depth of unique reads ~20M

NEH2_SB1 has the lowest unique reads ~5M, but is an annomaly.

Most sequence files are falling between 10-20M unique reads.

Quality scores & per base sequence content look good!


## 3. Trimming raw reads, mapping to reference genome, and SNP calling with [dDocent](https://ddocent.com)

### renaming files 
Update fastq names to fit [dDocent naming convention](https://ddocent.com/UserGuide/#naming-convention)

Here's bash code to rename those files by removing the second underscore:
```bash
for f in *TV0*.fastq.gz; do
    new_name=$(echo "$f" | sed 's/\(.*_.*\)_/\1/')
    mv "$f" "$new_name"
done
```

This renames files like so:

- `NEH1_T0_1.F.fastq.gz` → `NEH1_T01.F.fastq.gz`
- `NEH2_T0_3.R.fastq.gz` → `NEH2_T03.R.fastq.gz`

To **test first without renaming**, swap `mv` for `echo`:
```bash
for f in *TVE*.fastq.gz; do
    new_name=$(echo "$f" | sed 's/\(.*_.*\)_/\1/')
    echo "$f" → "$new_name"
done
```

Simplify the Vibrio sample names by removing "Probed"
```
for f in *Probed*.fastq.gz; do
    new_name=$(echo "$f" | sed 's/Probed//')
    mv "$f" "$new_name"
done
```

Check for samples with more than 1 underscore
```
for f in *.gz; do
    count=$(echo "$f" | tr -cd '_' | wc -c)
    if [ "$count" -ne 1 ]; then
        echo "$f has $count underscores"
    fi
done
```
This didn't return anything, so all of my sample names should be good!

One last thing, for uniformity, I want to change the file extension to .fq.gz instead of .fastq.gz
```
for f in *.fastq.gz; do
    new_name=$(echo "$f" | sed 's/\.fastq\.gz$/.fq.gz/')
    mv "$f" "$new_name"
done
```

### download dDocent file specific to EecSeq + pooled samples
There is a new version of dDocent specific to EecSeq and pooled samples `dDocent_ngs_3.2`. I downloaded from Amy's [RISG_LarvalCADO]((https://github.com/amyzyck/RISG_LarvalCADO/tree/main/Scripts)) repo, and have it stored in `/home/mguidry/1_Larval-CADO/Scripts` on KITT.

### Setting up 

Activate conda env (from earlier) with dDocent installed

```
conda activate larvae
conda list #check all installed packages
```

Make directory for dDocent and link files plus `dDocent_ngs_3.2` file in 
```
mkdir Larval_ddocent
cd Larval_ddocent/

#link files
ln -s ../raw_seq/*.fq.gz .
ls -1 | wc -l  #check to make sure we have all 182 files!

# link in dDocent 
ln -s ../Scripts/dDocent_ngs_3.2 .

# link in reference genome
ln -s /home/Genomic_Resources/C_virginica/reference.fasta .
```

### Running dDocent for trimming, mapping and SNP calling
- Testing values for match score, mismatch score, and gap penalty for read mapping (A = 2, B = 4, and O = 6)

```
bash dDocent_ngs_3.2
```
```
dDocent 3.1.0 

Contact jpuritz@uri.edu with any problems 

 
Checking for required software

All required software is installed!

dDocent version 3.1.0 started Fri Aug 16 21:17:12 EDT 2024 

30 individuals are detected. Is this correct? Enter yes or no and press [ENTER]
yes
Proceeding with 30 individuals
dDocent detects 80 processors available on this system.
Please enter the maximum number of processors to use for this analysis.
20

Do you want to quality trim your reads?
Type yes or no and press [ENTER]?
yes

Do you want to perform an assembly?
Type yes or no and press [ENTER].
no

Reference contigs need to be in a file named reference.fasta

Do you want to map reads?  Type yes or no and press [ENTER]
yes
BWA will be used to map reads.  You may need to adjust -A -B and -O parameters for your taxa.
Would you like to enter a new parameters now? Type yes or no and press [ENTER]
yes
Please enter new value for A (match score).  It should be an integer.  Default is 1.
2
Please enter new value for B (mismatch score).  It should be an integer.  Default is 4.
4
Please enter new value for O (gap penalty).  It should be an integer.  Default is 6.
6
Do you want to use FreeBayes to call SNPs?  Please type yes or no and press [ENTER]
no
Is this a pooled sequencing data set?  Please type yes or no and press [ENTER]
yes

Please enter your email address.  dDocent will email you when it is finished running.
Don't worry; dDocent has no financial need to sell your email address to spammers.
```

### Resulting files

```
.F.fq.gz and .R.fq.gz #original sequence files
.R1.fq.gz #trimmed read (fwd)
.R2.fq.gz #trimmed read (rev)
.RGmg.bam #mapped reads to the genome
.F.bam #filtered, mapped reads 
```

`bamlist.list`: a list of all BAM files passed to FreeBayes

## Trimmed reads FastQC & MultiQC report

### FastQC
FastQC is a program designed to visualize the quality of high throughput sequencing datasets. The report will highlight any areas where the data looks unusual or unreliable.
```
mkdir /home/mguidry/1_Larval-CADO/fastqc_trimmed
cd fastqc_trimmed
#run the following in tmux session - used two (one for FWD and one for REV)
conda activate larvae
cd Larval_dDocent/
fastqc -o /home/mguidry/1_Larval-CADO/fastqc_trimmed/ ./*F.fastq.gz 
fastqc -o /home/mguidry/1_Larval-CADO/fastqc_trimmed/ ./*R.fastq.gz 

# had to reinstall multiqc in the conda environemnt for some reason ##
# after fastqc is done - ran multiqc from the dir with the fastqc outputs
multiqc .
```

### Mapping optimization
After trimming and mapping are done, we can look at optimizing mapping with samtools.

Take a look at how mapping went with default parameters then we can run mapping with different parameters on a few samples to explore the data a bit more.

`samtools` helps us look at BAM files. Can check a couple samples to see what the difference is between filtered and unfiltered reads or different mapping parameters.

```
conda activate larvae
ls *.bam 
samtools #shows you everything samtools can do
```


samtools report exploring **filtered** mapped reads
```
samtools flagstats -@16 ARC2_CB1.F.bam > ARC2_CB1.F.flagstats.txt 
samtools flagstats -@16 NEH2_CB1.F.bam > NEH2_CB1.F.flagstats.txt 
samtools flagstats -@16 NEH1_CB1.F.bam > NEH1_CB1.F.flagstats.txt 
samtools flagstats -@16 NEH3_CB1.F.bam > NEH3_CB1.F.flagstats.txt
samtools flagstats -@16 MV1_CB1.F.bam > MV1_CB1.F.flagstats.txt
samtools flagstats -@16 MV2_CB1.F.bam > MV2_CB1.F.flagstats.txt
samtools flagstats -@16 MV3_CB1.F.bam > MV3_CB1.F.flagstats.txt

samtools flagstats -@16 CON_TV0Vibrio.F.bam > CON_TV0Vibrio.F.flagstats.txt
samtools flagstats -@16 VS1_TVEVibrio.F.bam > VS1_TVEVibrio.F.flagstats.txt
samtools flagstats -@16 CC1_TVECombined.F.bam > CC1_TVECombined.F.flagstats.txt
samtools flagstats -@16 VC1_TVECombined.F.bam > VC1_TVECombined.F.flagstats.txt

mv *flagstats.txt ./map_opt/flagstats/

## run for all samples 
for bam in *.F.bam; do
    base=${bam%.F.bam}                # strip .F.bam
    samtools flagstat -@16 "$bam" > "map_opt/flagstats/${base}.flagstats.txt"
done
```
Mapping looked pretty good across all samples! I'll stick with this for now. I may end up spending more time optimizing and fine-tuning mapping later, but I am happy with this!

**Following trimmed fastqc and mapping investigation, I submitted a new dDocent run to call SNPs**

## 4. Variant filtering
Following Jon's analysis from [Larval CASE project](https://github.com/jpuritz/Puritz_etal_CASE); analysis description can also be found in [`Scripts/CASE_FULL_FINAL.Rmd`](Scripts/CASE_FULL_FINAL.Rmd)

### Download Popoolation2 scripts
```
cd Scripts
git clone https://github.com/ToBoDev/assessPool.git
```

### Create conda (mamba) environment called `CADO`
```
mamba env create --file CADO_environment.yaml
mamba env create --file random_draw_environment.yaml
```

### Run filtering script
Filtering to a depth cutoff of 20

```
mamba activate CADO
cd ../Larval_ddocent/raw.vcf/
bash ../../Scripts/CASE_PVCF_filter2.sh CADO 64 20
```

```
source activate CADO
cd ../raw.vcf 
bcftools index CADO.TRSdp.20.g5.nDNA.FIL.vcf.gz
bcftools query -l CADO.TRSdp.20.g5.nDNA.FIL.vcf.gz > samples
```


## Create Sync file
Filtered for missing data less than 10% and MAF of > 0.015 based on read counts using VCF file first then filters by sites with 2-4 alleles and outputs filtered sites in a compressed VCF.

Can also conver to bed file with SNP coordinates and assign gene annotations to these gene IDs
```{bash, eval=FALSE}
source activate CADO

cd ../raw.vcf
# filters for missing data less than 10%, MAF of >0.015 based on read counts and filters by sites with 2-4 alleles then outputs a compressed VCF
bcftools view CADO.TRSdp.20.g5.nDNA.FIL.vcf.gz | bcftools view -i 'F_MISSING<0.1'  | bcftools view -M 4 -m 2 | bcftools +fill-tags -- -t 'AAF:1=sum(FORMAT/AO)/sum(FORMAT/DP)' | bcftools +fill-tags -- -t  FORMAT/VAF | bcftools view --threads 40 -i 'AAF > 0.015 && AAF < 0.985' -O z -o SNP.CADO.TRSdp.20.B90.2a.perp.vcf.gz

# converts final VCF to BED file of SNP coordinates (0-based start, 1-based end)
#bcftools view --threads 40 SNP.CASE.TRSdp.20.B90.2a.perp.vcf.gz | mawk '!/#/' | cut -f 1,2 | mawk '{print $1"\t"$2-1"\t"$2}' > total.snp.bed

# intersects SNPS with gene annotation BED, extracting gene IDs matching gene=LOC...;g, cleans them and produced a unique list of basckground genes for enrichment analysis (like topGO)
#bedtools intersect -wb -a total.snp.bed -b ~/CASE/analysis/sorted.ref3.0.gene.bed | grep -oh "gene=LOC.*;g" | sed 's/gene=//g' | sed 's/;g//g' | sort | uniq > CASE.study.background.LOC
```

> NOTE: Because the previous filtering script didn't separate InDels from SNPs with pooled data,
> the filtered variant call file (VCF) I have here are loci that have 4 alleles or less. 
> These can be a mixture of SNP, InDels, and complex mutations. 
>
> see below for filtering to just snps with `bcftools view --type snps` to get the conversion from vcf to sync file to work

### Create Sync files
```{bash, eval=FALSE}
source activate CADO

bcftools view --threads 40 ../raw.vcf/SNP.CADO.TRSdp.20.B90.2a.perp.vcf.gz  | mawk -F'\t' -v OFS='\t' '{ for(i=1;i<=NF;i++) if($i==".:.:.:.:.:.:.:.") $i="."; print }' > temp.vcf
bcftools view --type snps -m2 -M2 temp.vcf -o temp_snps.vcf

# convert to sync file
python2 ../../Scripts/VCFtoPopPool.py temp_snps.vcf Larval.snps.sync 

# pull positions of CHAPTER 1 SNPs from vcf file
bcftools view -S <(grep -E '^(ARC|NEH|MV)' samples) temp_snps.vcf | bcftools query -f '%CHROM\t%POS\n' > Chapter1.Larval.pos

# pull positions of CHAPTER 2 SNPs from vcf file
bcftools view -S <(grep -E '^(VC|VS|CC|CS|CON|STR)' samples) temp_snps.vcf | bcftools query -f '%CHROM\t%POS\n' > Chapter2.Larval.pos

#rm temp.vcf temp_snps.vcf
```

I added in the `--type snps` line because I was running into the error below. I believe this error arose from issues with the way the VCFtoPopPool.py script was dealing with complex haplotypes. I think where the script was randomly assigning a nucleotide to complex haplotypes lead to a mismatch in the OBS and n variables. When I got the error, the script still generated a sync file, however I think it was truncated as it was much smaller in size than the sync file generated after running the snp filter.

--type snps removes indels and MNPs, which are the most common sources of malformed or inconsistent allele/count fields in FreeBayes output
-m2 -M2 enforces strictly biallelic sites, so alleles is always exactly [REF, ALT1] — a length-2 list, and OBS = RO + AO will always also be length 2, so n never exceeds the bounds of OBS
```{bash, eval=FALSE}
#note - Larval.sync file is the truncated result of the vcf->sync converstion of the full vcf with complex haplotypes
(CADO) python2 ../../Scripts/VCFtoPopPool.py temp.vcf Larval.sync 
91
Traceback (most recent call last):
  File "../../Scripts/VCFtoPopPool.py", line 110, in <module>
    a[z[alleles[n]]]=OBS[n]
IndexError: list index out of range
```

### This sort is to maintain reproducibility across older analysis
```{bash}
mawk 'BEGIN {OFS="\t"
    order["CHROM"] = 0
    order["NC_035789.1"] = 1
    order["NC_035780.1"] = 2
    order["NC_035781.1"] = 3
    order["NC_035782.1"] = 4
    order["NC_035783.1"] = 5
    order["NC_035784.1"] = 6
    order["NC_035785.1"] = 7
    order["NC_035786.1"] = 8
    order["NC_035787.1"] = 9
    order["NC_035788.1"] = 10
}
{ print order[$1], $2, NR, $0 }' Larval.snps.sync | sort -k1,1n -k2,2n -k3,3n | cut -f4- > test.sync

mv test.sync Larval.snps.sync
```

## Split sync files by project with positional lookup***
```{bash}
cat <(echo -e "CHROM\tPOS") Chapter1.Larval.pos > Ch1.head.pos
cat <(echo -e "CHROM\tPOS") Chapter2.Larval.pos > Ch2.head.pos

# Chapter 1: ARC2, NEH, MV populations - with positional look up ***
mawk 'NR==FNR{a[$1,$2]; next} ($1,$2) in a' Ch1.head.pos Larval.snps.sync \
  | mawk 'NR==1{for(i=1;i<=NF;i++)if(i<=3||$i~/^(ARC|NEH|MV)/)k[i]}
          {o="";for(i=1;i<=NF;i++)if(i in k)o=o?o OFS $i:$i;print o}' OFS='\t' \
  | mawk '!/\t\.\t/' \
  > Chapter1.Larval.snps.sync


# Chapter 2: VC, VS, CC, CS, CON, STR populations - with positional look up ***
mawk 'NR==FNR{a[$1,$2]; next} ($1,$2) in a' Ch2.head.pos Larval.snps.sync \
  | mawk 'NR==1{for(i=1;i<=NF;i++)if(i<=3||$i~/^(VC|VS|CC|CS|CON|STR)/)k[i]}
          {o="";for(i=1;i<=NF;i++)if(i in k)o=o?o OFS $i:$i;print o}' OFS='\t' \
  | mawk '!/\t\.\t/' \
  > Chapter2.Larval.snps.sync


# Count samples per file (subtract 3 for CHROM, POS, REF)
head -1 Chapter1.Larval.snps.sync | tr '\t' '\n' | wc -l  
# output = 66 -3 = 63 samples = 9 samples/exp * 7 exp = 63 samples (looks good!)
head -1 Chapter2.Larval.snps.sync | tr '\t' '\n' | wc -l
# output = 31 - 3 = 28 samples = 14 samples/probeset * 2 probesets = 28 (looks good!)
head -1 Larval.snps.sync | tr '\t' '\n' | wc -l
# output = 94 -3 = 91 samples 
# 63+28 = 91 (all good)

#check out column names for each sync file
head -1 Chapter1.Larval.snps.sync | tr '\t' '\n'
head -1 Chapter2.Larval.snps.sync | tr '\t' '\n'
```

## CHAPTER 1 - Add coverage stats to sync file and filter by minimum and mean coverage
```{bash, eval=FALSE}
source activate CADO

# add coverage stats to each sync file and check those out to decide on depth limits
mawk -f ../../Scripts/add_cov_sync.txt Chapter1.Larval.snps.sync > Ch1.cov.sync
mawk '{print $1, $2, $(NF-2), $(NF-1), $NF}' OFS='\t' Ch1.cov.sync > Ch1.coverage_stats.txt

#check column index numbers
mawk 'NR==1 { for(i=1; i<=NF; i++) print i, $i }' Ch1.cov.sync
# 67 MIN_COV
# 68 MAX_COV
# 69 MEAN_COV

# filter the sync file for specific coverage stats (be sure to update column numbers - they correspond to min and mean coverage)
mawk '$67 > 9 && $69 > 24' Ch1.cov.sync > Ch1.dp25.cov.sync

cat Ch1.cov.sync | wc -l 
# 146,537
cat Ch1.dp25.cov.sync | wc -l 
# 98,680
```
Here I only kept SNPs that had a minimum depth of 10 or greater and a mean depth of 25 or greater (47,857 snps removed).

## CHAPTER 2 - Add coverage stats to sync file and filter by minimum and mean coverage
```{bash, eval=FALSE}
source activate CADO

# add coverage stats to each sync file and check those out to decide on depth limits
mawk -f ../../Scripts/add_cov_sync.txt Chapter2.Larval.snps.sync > Ch2.cov.sync
mawk '{print $1, $2, $(NF-2), $(NF-1), $NF}' OFS='\t' Ch2.cov.sync > Ch2.coverage_stats.txt

#check column index numbers
mawk 'NR==1 { for(i=1; i<=NF; i++) print i, $i }' Ch2.cov.sync
# 32 MIN_COV
# 33 MAX_COV
# 34 MEAN_COV

# filter the sync file for specific coverage stats (be sure to update column numbers - they correspond to min and mean coverage)
mawk '$32 > 9 && $34 > 24' Ch2.cov.sync > Ch2.dp25.cov.sync

cat Ch2.cov.sync | wc -l 
# 146,537
cat Ch2.dp25.cov.sync | wc -l 
# 145,530
```
Here I only kept SNPs that had a minimum depth of 10 or greater and a mean depth of 25 or greater (1,007 snps removed).


could also filter coverage for the combined chapter 1 & 2 sync file, but I didn't need to
```{bash, eval=FALSE}
#mawk -f ../../Scripts/add_cov_sync Larval.snps.sync | mawk '$66 > 9 && $68 > 24' > Larval.snps.cov.sync
```

## REMAINING ANALYSES IN R!

### Chapter 1 filtered sync file
`Ch1.dp25.cov.sync` copied into 1_Larval-CADO Analysis directory

### Chapter 2 filtered sync file
`Ch2.dp25.cov.sync` copied into 2_Vibrio-Challenge Analysis directory


See ____.Rmd
_________________________________________________________


# QUESTIONS FOR JON:
- look at --type snps filtering step
- why are there the same number of loci in each chapter sync file before filtering for coverage? I only pulled the sites specific to each chapter but the .pos files seem to be the same?