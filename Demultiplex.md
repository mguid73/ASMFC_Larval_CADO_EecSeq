# Demultiplexing Chapter 1 & 2 Larval EecSeq data

**TO-DO:**
- make sample file with barcodes info

**QUESTIONS FOR JON:**
- I thought these data were beind demultiplexed by novogene per emails in October?
- run qc before *and* after demultiplexing? Whats the benefit of running before? just overall seq quality?
- to be conscious of space on KITT - Where on KITT to do demultiplexing? In RAID STORAGE (which one?) and not home/? 
    - write access in RAID STORAGE?

- Using Amy's [STACKS](https://github.com/amyzyck/EecSeq_NB_EasternOyster/blob/master/Analysis/Analysis_Part1/EecSeq_Cvirginica_dDocent.md) pipeline or [dDocent_demux](https://github.com/jpuritz/dDocent_demux)???
- review plan below! 
    - sample file and run script for each index pair??? or can I give it 1 sample file and use *_1.fq.gz and *_2.fq.gz as inputs??
    - y-inline a and b adapter seqs become adapter_1 and adapter_2 - if using stacks? 
    - q: y-inline barcodes for dDocent_demux - double check that I'm using the right sheet and pulling the right seq.
        - Barcode_R1 = y-inline a
        - Barcode_R2 = y-inline b
        - pull ***inline barcode*** column?? for y-inline??
        - pull ***Barcode Index*** column for i7;i5?? which one (2500 or 4000)?

_________________________________________________________

Before proceeding with analysis reads will have to be demultiplexed, meaning assigning sample specific reads using the index pairs assigned at library prep and pooling steps.  

Multiplexed files are located in `/RAID_STORAGE2/Raw_Data/ASMFC_EECSEQ/01.RawData`

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


## Demultiplexing with [`dDocent_demux`](https://github.com/jpuritz/dDocent_demux)
Run from `/home/mguidry/1_Larval-CADO/` on KITT

### Download script and make executable
```
chmod +x dDocent_demux.txt
```

### Construct sample file for each index pair
The script automatically detects the demultiplexing mode based on column headers in the tab-delimited sample file. Here, I made a file with the sample name, header indices (i7/i5) and the inline barcode (+reverse compliment???)


### Run script
**RUN FOR EACH INDEX PAIR** (for my data run it 20x)?

```
dDocent_demux -r1 <R1.fastq.gz> -r2 <R2.fastq.gz> -s <samples.txt> -o demux
```

________________________________________________________________________________


________________________________________________________________________________

## Demultiplexing with [`STACKS`](https://catchenlab.life.illinois.edu/stacks/):

### Make barcode files for each library
Each library needs a separate barcodes file in txt format

### Turning barcode files into a list of barcodes

### Make a new direcotry for each library

### In each library directory download renaming script from J Puritz

### Move each barcode txt file to the appropriate library directory

### Use the function `process_shortreads` to demultiplex each file
Program options can be found [here](https://catchenlab.life.illinois.edu/stacks/comp/process_shortreads.php)

```
process_shortreads -1 D501_R1_001.fastq.gz -2 D501_R2_001.fastq.gz -b barcodes_A -r -i gzfastq -o /RAID_STORAGE2/mguidry/ASMFC_
```

## Library outputs

#### Library 1

#### Library 2

#### Library 3

#### Library 4

#### Library 5

#### Library 6

#### Library 7

#### Library 8

#### Library 9

#### Library 10

#### Library 11

#### Library 12

#### Library 13

#### Library 14

#### Library 15

#### Library 16

#### Library 17

#### Library 18

#### Library 19

#### Library 20


### Copy sample files from each `Library` directory to `ASMFC_EECSEQ_DEMUX` directory


> There should be 182 files total: 91 samples x 2 reads/sample

### Count raw reads for each file
```{bash}
for fq in *.fq.gz
do
echo $fq
zcat $fq | echo $((`wc -l`/4))
done
```


## Post-demultiplexing quality check

### Run `fastqc` then `multiqc` for report

