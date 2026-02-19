# Demultiplexing Chapter 1 & 2 Larval EecSeq data
_________________________________________________________

Before proceeding with analysis reads will have to be demultiplexed, meaning assigning sample specific reads using the index pairs assigned at library prep and pooling steps. After demultiplexing, I'll do some QC with fastqc/multiqc.

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

Unfortunately a good amount of probes remained in the pools and were sequenced as well. Fortunately, the probe libraries were constructed with distinct indices that were not used in the gDNA captured libraries. Sequenced probes are in the multiplexed folders labeled "Probes_".
The Undetermined directory contains reads that could not be resolved into either captured library indices or probe indicies.

> **Note!** The 710 probe files need to be renamed with 702. They were mislabeled in the table sent to novogene upon discovery of the unexpected probes in the sequencing run. 


For now, I will only demultiplex and focus on the captured libraries. 
Each of the captured library files (ex. i506_i706) contains 4-5 samples. These are identified down to the sample with the addition of an adapter sequence. 

Inside of each of these files is set of fwd and rev read fastq files labeled with 1 and 2 to indicate the read. 

> for example: 
> i506_i706_WKDL250004555-1A_22W7JGLT4_L7_1.fq.gz
> i506_i706_WKDL250004555-1A_22W7JGLT4_L7_2.fq.gz

### Download script to working directoryy and make executable
```
cd /RAID_STORAGE3/mguidry/
mv ../home/mguidry/1_Larval_CADO/dDocent_demux.txt .
chmod +x dDocent_demux.txt
```

## Demultiplexing with [`dDocent_demux`](https://github.com/jpuritz/dDocent_demux)
Run from `/RAID_STORAGE3/mguidry/` on KITT

```
#link in fq.gz files from RAID_STORAGE2 


```



### Construct sample file for each index pair
The script automatically detects the demultiplexing mode based on column headers in the tab-delimited sample file. Here, I made a file with the sample name & inline barcode as the data is already split up by index (i7;i5) pairs. 

```
#ensure sample info files is present 


#look at example strucutre of sample info

```

### Run script
**RUN FOR EACH INDEX PAIR**

```
dDocent_demux -r1 <R1.fastq.gz> -r2 <R2.fastq.gz> -s <samples.txt> -o demux
```

________________________________________________________________________________
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