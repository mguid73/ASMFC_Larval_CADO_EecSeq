## Assign adapter seq (barcode) to sample_ID
```
awk -F'\t' 'NR==FNR {if (FNR>1) b[$1]=$2; next} 
FNR==1 {print $0 "\tBARCODE"; next} 
{print $0 "\t" b[$3]}' \
adapter_barcodes.txt all_samples_demux.txt \
> all_samples_demux_with_barcodes.txt
```



## Check that all barcodes were pulled correctly
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

## Split table into index pair sample files
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

## Clean up files to only have Sample_ID and BARCODE columns
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


## Rename BARCODE to Barcode_R1 and duplicate it to make Barcode_R2 column too 
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

## Check spacing and formating
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

YAY! Now I've got all the samples with barcode info I should need to start demultiplexing!

## Little bit of bug fixing
fix issue with tab delimiters in _sample.txt files
```
tr -d '\r' < 506_706_samples.txt > 506_706_samples_fixed.txt
```

check to make sure all ^M occurances are gone!
```
cat -A 506_706_samples_fixed.txt | head
```

Confirm field structure (should return 3)
```
awk -F'\t' '{print NF}' 506_706_samples_fixed.txt | sort -nu
```


## Made that fix into a for loop...
```
for f in *_samples.txt; do
    echo "Processing $f ..."

    fixed="${f%.txt}_fixed.txt"

    # Remove all carriage returns
    tr -d '\r' < "$f" > "$fixed"

    # Check for remaining ^M characters
    if cat -A "$fixed" | grep -q '\^M'; then
        echo "  ❌ WARNING: ^M still present in $fixed"
    else
        echo "  ✅ No ^M characters remain"
    fi

    # Check field structure
    echo -n "  Field counts: "
    awk -F'\t' '{print NF}' "$fixed" | sort -nu

    echo "-----------------------------------"
done
```

for a properly formatted file this should be the output:
```
Processing 506_706_samples.txt ...
  ✅ No ^M characters remain
  Field counts: 3
-----------------------------------
```