#!/bin/bash
awk '
NR == 1 {
    # Print the original header and add the new column header "IS_SUM"
    print $1"\t"$2"\t"$3"\tIS_SUM"
    next
}
{
    # Initialize an array to hold the sums
    split($4, sum, ":")
    
    # Loop through the remaining fields and sum the colon-separated values
    for (i = 5; i <= NF; i++) {
        split($i, current, ":")
        for (j = 1; j <= length(current); j++) {
            sum[j] += current[j]
        }
    }

    # Print the first three columns (CHROM, POS, REF)
    printf "%s\t%s\t%s\t", $1, $2, $3
    
    # Print the sum of the colon-separated fields
    for (j = 1; j <= length(sum); j++) {
        printf "%d", sum[j]
        if (j < length(sum)) {
            printf ":"
        }
    }
    print ""  # Newline after the sum
}' "$1"

