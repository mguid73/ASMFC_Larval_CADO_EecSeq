import pandas as pd
import sys
from concurrent.futures import ProcessPoolExecutor
import random

def process_line(line, total_alleles, seed):
    # Initialize a separate random generator for this task
    rng = random.Random(seed)

    # Split the line into columns (tabs or spaces)
    cols = line.strip().split('\t')

    # Extract allele count pools (skip first 3 columns: chrom, basepair, placeholder)
    pools = cols[3:]

    new_pools = []

    # For each pool, subsample the allele counts
    for pool in pools:
        # Split the allele counts into an array
        counts = pool.split(':')

        # Create a weighted list of alleles, where each index is repeated by its count
        alleles = []
        for i, count in enumerate(counts):
            alleles.extend([i] * int(count))

        # Sample `total_alleles` alleles from the shuffled list
        sampled_alleles = rng.choices(alleles, k=total_alleles)

        # Count occurrences of each allele after sampling
        sampled_count = [sampled_alleles.count(i) for i in range(len(counts))]

        # Create the new counts string in the format "a:b:c..."
        new_pool = ':'.join(map(str, sampled_count))
        new_pools.append(new_pool)

    # Return the updated line with new allele counts
    return '\t'.join([cols[0], cols[1], cols[2]] + new_pools)

def main(cov_file, input_file, output_file):
    SEED = 42  # Hardcoded seed value

    # Read the coverage file
    cov_df = pd.read_csv(cov_file, sep="\t", header=0)
    cov_df.columns = cov_df.columns.str.strip()
    last_column_name = cov_df.columns[-1]
    target_cov = pd.to_numeric(cov_df[last_column_name], errors='coerce')

    # Read the input file
    with open(input_file, 'r') as f_in:
        lines = f_in.readlines()
        total_alleles_list = target_cov.astype(int).tolist()

    # Validate allele counts
    for idx, (line, total_alleles) in enumerate(zip(lines, total_alleles_list)):
        pools = line.strip().split('\t')[3:]
        for pool in pools:
            counts = list(map(int, pool.split(':')))
            if total_alleles > sum(counts):
                raise ValueError("Error on line {}: total_alleles ({}) exceeds the sum of original counts ({}) in pool: {}. Line content: {}".format(idx + 1, total_alleles, sum(counts), pool, line.strip()))

    # Generate seeds for each task
    seeds = [SEED + i*42 for i in range(len(lines))]

    # Process lines in parallel
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(process_line, lines, total_alleles_list, seeds))

    # Write the results to the output file
    with open(output_file, 'w') as f_out:
        f_out.writelines(line + '\n' for line in results)

    print("Processing complete. Output written to {}".format(output_file))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python subsample.py <cov_file> <input_file> <output_file>")
        sys.exit(1)
    
    main(sys.argv[1], sys.argv[2], sys.argv[3])