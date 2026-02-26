# Demultiplexing Chapter 1 & 2 Larval EecSeq data

Easy Guide to tmux

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


For now, I will only demultiplex and focus on the **captured libraries**. 
Each of the captured library files (ex. i506_i706) contains 4-5 samples. These are identified down to the sample with the addition of an adapter sequence. 

Inside of each of these directories is set of fwd and rev read fastq files labeled with 1 and 2 to indicate the read. I will run demultiplexing on each one of these directories with the adapter info to parse out fastq data by sample. 

> for example: 
> i506_i706_WKDL250004555-1A_22W7JGLT4_L7_1.fq.gz
> i506_i706_WKDL250004555-1A_22W7JGLT4_L7_2.fq.gz

### Download script to working directory and make executable
```
cd /RAID_STORAGE3/mguidry/
mv ../home/mguidry/1_Larval_CADO/dDocent_demux.txt .
chmod +x dDocent_demux.txt
```

## Demultiplexing with [`dDocent_demux`](https://github.com/jpuritz/dDocent_demux)
Running from `/RAID_STORAGE3/mguidry/` on KITT

### Construct sample file for each index pair
The script automatically detects the demultiplexing mode based on column headers in the tab-delimited sample file. Here, I made files with the sample name & inline adapter barcode for each index (i7;i5) pair. 

To construct those files, I followed the following steps:

Assign adapter seq (barcode) to sample_ID
```
awk -F'\t' 'NR==FNR {if (FNR>1) b[$1]=$2; next} 
FNR==1 {print $0 "\tBARCODE"; next} 
{print $0 "\t" b[$3]}' \
adapter_barcodes.txt all_samples_demux.txt \
> all_samples_demux_with_barcodes.txt
```

Check that all barcodes were pulled correctly
```
awk -F'\t' '
NR==FNR {
    if (FNR>1) ref[$1]=$2
    next
}
FNR==1 {
    for (i=1; i<=NF; i++) {
        if ($i=="Adapter") adapter_col=i
        if ($i=="BARCODE") barcode_col=i
    }
    next
}
{
    adapter=$adapter_col
    observed=$barcode_col
    expected=ref[adapter]

    if (observed != expected) {
        print "Mismatch on line " FNR ": Adapter=" adapter \
              " Expected=" expected \
              " Observed=" observed
        mismatch=1
    }
}
END {
    if (!mismatch)
        print "All adapter-barcode pairs match reference table ✔"
}
' adapter_barcodes.txt all_samples_demux_with_barcodes.txt
```

Split table into index pair sample files
```
awk -F'\t' '
FNR==1 {
    for (i=1; i<=NF; i++) {
        if ($i=="Index_pairs") idx_col=i
    }
    header=$0
    next
}
{
    pair=$idx_col
    gsub(";", "_", pair)
    file=pair "_samples.txt"

    if (!(file in seen)) {
        print header > file
        seen[file]=1
    }
    print >> file
}
' all_samples_demux_with_barcodes.txt
```

Clean up files to only have Sample_ID and BARCODE columns
```
mkdir ../cleaned_sample_info

for f in *_samples.txt; do
  awk -F'\t' '
  FNR==1 {
      for (i=1; i<=NF; i++) {
          if ($i=="Sample_ID") sid=i
          if ($i=="BARCODE") bc=i
      }
      print "Sample_ID\tBARCODE"
      next
  }
  { print $sid "\t" $bc }
  ' "$f" > ../cleaned_sample_info/"$f"
done
```

```
cd ../cleaned_sample_info 
ls | wc -l #should have 20 files (I removed the _samples.txt file with the header info from original big table)
```


Rename BARCODE to Barcode_R1 and duplicate it to make Barcode_R2 column too 
```
for f in *_samples.txt; do
  awk -F'\t' 'BEGIN{OFS="\t"}
  FNR==1 {
      print "Sample_ID","Barcode_R1","Barcode_R2"
      next
  }
  {
      print $1,$2,$2
  }' "$f" > tmp && mv tmp "$f"
done
```

Check spacing and formating
```
head 506_706_samples.txt | cat -A
```
```
for f in *_samples.txt; do
  awk '
  NF != 3 {
      print "Column count issue in", FILENAME, "line", NR, "- has", NF, "columns"
      bad=1
  }
  END {
      if (!bad)
          print FILENAME, "OK"
  }' "$f"
done
```

Little bit of bug fixing
```
#fix issue with tab delimiters in _sample.txt files
tr -d '\r' < 506_706_samples.txt > 506_706_samples_fixed.txt

#check to make sure all ^M occurances are gone!
cat -A 506_706_samples_fixed.txt | head

#Confirm field structure (should return 3)
awk -F'\t' '{print NF}' 506_706_samples_fixed.txt | sort -nu
```

example structure of sample info
```
(base) head 506_706_samples.txt 
Sample_ID       Barcode_R1      Barcode_R2
ARC2_CB1ATCACG  ATCACG
NEH2_T0_TGGCCA  TGGCCA
MV3_SB2 ACAGTG
MV3_T0_2        CTTGCA  CTTGCA
MV3_STR_GATCAG  GATCAG
```

### Set up directory for each set of index pair fastq files
```
#move sample info files to appropriate directories - do this for each index pair
mkdir 506_706
cd 506_706/
cp cleaned_sample_info/506_706_samples.txt 

#link in fastq files 
ln -s /RAID_STORAGE2/Raw_Data/ASMFC_EECSEQ/01.RawData/i506_i706/*.fq.gz .
```

### Run script
**RUN FOR EACH INDEX PAIR**
```
#start new tmux session and activate conda environment
tmux new -s demux
conda activate larvae
```
```
#run dDocent_demux
dDocent_demux -r1 <R1.fastq.gz> -r2 <R2.fastq.gz> -s <samples.txt> -o demux
```
|----------------------------|-----------------------------|----------------------------|
|----------------------------|-----------------------------|----------------------------|
|✅ 506_706 - started 2:00pm | ✅ 508_706 - started 9:20am | ✅ 509_706 - started 4:43pm|
|✅ 506_707 - started 6:30pm | ✅ 508_707 - started 9:30am | ✅ 509_707 - started 4:46pm|
|✅ 506_708 - started 6:42pm | ✅ 508_708 - started 9:40am | ✅ 509_708 - started 4:51pm|
|✅ 506_712 - started 6:55pm | ✅ 508_712 - started 9:50am | ✅ 509_712 - started 4:56pm|
|----------------------------|-----------------------------|
|✅ 511_706 - started 5:45pm | ✅ 512_706 - started 9:36pm |
|✅ 511_707 - started 5:52pm | ✅ 512_707 - started 9:41pm |
|✅ 511_708 - started 5:55pm | ✅ 512_708 - started 9:46pm |
|✅ 511_712 - started 6:00pm | ✅ 512_712 - started 9:53pm |
|----------------------------|-----------------------------|

### Move sample fastqc files to one directory
Check files in the index-pair folders & move sample fastq files into one central folder

> NOTE:
> I identified some messiness here (of my own making). I have two sets of Vibrio samples (with duplicate sample names) that were captured with different probe sets. 
>
> Thankfully, they have distinct indexing and adapters so identifying them is not the issue, however fastq files will have to be renamed so I can differentiate between them!!
> 
> Vibrio samples in Vibrio_1 and Vibrio_2 (pools 8&9) were captured with larval CADO AND Vibrio probe sets. 
> 
> Vibrio samples in Vibrio_3 and Vibrio_4 (pools 10&11) were only captured with Vibrio probe sets. 
> 
> Thus, samples from Vibrio_1 and _2 are named with _CombinedProbed
> 
> And samples from Vibrio_3 and _4 are named with _VibrioProbed
> 
> Samples in 511_712 index pair directory had to be re-demultiplexed after renaming the vibrio samples due this oversight
> 
> Thus, `/RAIDSTORAGE3/mguidry/511_712_take2` directory contains the correct Vibrio sample reads properly named.

| Chapter & Experiment       | Population |  Number of samples          | Number of fastq (Fwd/Rev)  | Check |
|----------------------------|------------|-----------------------------|----------------------------|-------|
|  CH 1 - Larval CADO        |    ARC2    |              9              |           18               |   ✅  |
|  CH 1 - Larval CADO        |    NEH1    |              9              |           18               |   ✅  |
|  CH 1 - Larval CADO        |    NEH2    |              9              |           18               |   ✅  |
|  CH 1 - Larval CADO        |    NEH3    |              9              |           18               |   ✅  |
|  CH 1 - Larval CADO        |    MV1     |              9              |           18               |   ✅  |
|  CH 1 - Larval CADO        |    MV2     |              9              |           18               |   ✅  |
|  CH 1 - Larval CADO        |    MV3     |              9              |           18               |   ✅  |
|  CH 2 - Vibrio (Combined)  |    MV3     |              14             |           28               |   ✅  |
|  CH 2 - Vibrio (Vibrio)    |    MV3     |              14             |           28               |   ✅  |
________________________________________________________________________________
There are 182 fastq files total: 91 samples x 2 reads per sample.

*Total CH 1 - Larval CADO files = **126***

*Total CH 2 - Vibrio files = **56***

**ALL FILES ARE THERE!** ✅


### Count raw reads for each file - optional
```{bash}
for fq in *.fq.gz
do
echo $fq
zcat $fq | echo $((`wc -l`/4))
done
```