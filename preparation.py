# !/usr/bin/env python 
# coding=utf-8
# Python script to search a reference for PAM motif and saves target sequence,
# desired pattern and amount of mismatches as one txt file per chromosome, splits file into multiple ones per
# chromosome for further analysis with Cas-offinder
# Usage: ./preparation.py --motif GG --pam NGG --reference_file /path/to/fasta/file --ref_name GRCh38 --mismatches 4
from Bio import SeqIO
from Bio.Seq import Seq
import re
import csv
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Preparation Script to find CRISPR-targets")
    parser.add_argument("--motif", type=str, help="Motif (E.g.: GG for NGG)", required=True)
    parser.add_argument("--pam", type=str, help="PAM sequence(E.g.: NGG)", required=True)
    parser.add_argument("--reference_file", type=str, help="path/to/fasta/reference/file", required=True)
    parser.add_argument("--ref_name", type=str, help="Reference name for naming files E.G.: GRCh38", required=True)
    parser.add_argument("--mismatches", type=str, help="Number of mismatches", required=True)

    args = parser.parse_args()

    reference = args.reference_file
    ref_name = args.ref_name
    motif = args.motif
    pam = args.pam
    mismatches = args.mismatches
    # TODO: Change target length if using different PAM
    target_length = len(pam) + 20  # only for PAM with 'NGG'
    reverse_motif = (Seq(motif).complement())
    # Dictionary to find corresponding chromosomes in reference file
    # TODO: Change dictionary when using other reference than GRCh38
    dictionary = {
        "chr1": "NC_000001.11",
        "chr2": "NC_000002.12",
        "chr3": "NC_000003.12",
        "chr4": "NC_000004.12",
        "chr5": "NC_000005.10",
        "chr6": "NC_000006.12",
        "chr7": "NC_000007.14",
        "chr8": "NC_000008.11",
        "chr9": "NC_000009.12",
        "chr10": "NC_000010.11",
        "chr11": "NC_000011.10",
        "chr12": "NC_000012.12",
        "chr13": "NC_000013.11",
        "chr14": "NC_000014.9",
        "chr15": "NC_000015.10",
        "chr16": "NC_000016.10",
        "chr17": "NC_000017.11",
        "chr18": "NC_000018.10",
        "chr19": "NC_000019.10",
        "chr20": "NC_000020.11",
        "chr21": "NC_000021.9",
        "chr22": "NC_000022.11",
        "chrX": "NC_000023.11",
        "chrY": "NC_000024.10",
    }
    dict_keys = dictionary.keys()
    fasta = SeqIO.to_dict(SeqIO.parse(reference, "fasta"))
    # TODO: Change pattern according to chosen PAM
    pattern = "NNNNNNNNNNNNNNNNNNNNNGG"  # desired pattern including PAM sequence
    direction_list = ["forward", "reverse"]
    # Execute tasks for forward and reverse direction
    for direction in direction_list:
        # for chromosome in dictionary get sequence of fasta reference:
        for chromosome in dict_keys:
            chromosome_key = dictionary[chromosome]
            sequence = str(fasta[chromosome_key].seq)
            if direction == "forward":
                with open(chromosome + '.' + pam + '.' + ref_name + '.' + direction + '.txt', mode='w') as \
                        chromosome_file:
                    chromosome_forward_writer = csv.writer(chromosome_file, delimiter='\t', quotechar='"',
                                                           quoting=csv.QUOTE_MINIMAL)
                    for pam_motif in re.finditer(str(motif), sequence):
                        target_index = pam_motif.start() - 21  # TODO: Change value 21 if using different PAM length
                        stop = pam_motif.end()
                        target_sequence = sequence[target_index:stop].upper()
                        if len(target_sequence) >= 23:
                            chromosome_forward_writer.writerow([target_sequence, mismatches])

            else:
                # Search on reverse strand
                with open(chromosome + '.' + pam + '.' + ref_name + '.' + direction + '.txt',
                          mode='w') as chromosome_file:
                    chromosome_writer = csv.writer(chromosome_file, delimiter='\t', quotechar='"',
                                                   quoting=csv.QUOTE_MINIMAL)
                    for pam_motif in re.finditer(str(reverse_motif), sequence):
                        target_index = pam_motif.start()
                        stop = pam_motif.start() + target_length
                        target_sequence = (Seq(sequence[target_index:stop]).reverse_complement()).upper()
                        if len(target_sequence) >= 23:
                            chromosome_writer.writerow([target_sequence, mismatches])

        # Split chromosome files into smaller files and add header information(path/tp/reference/file and pattern)
        # on top of each file for cas-offinder
        for chromosome in dict_keys:
            smallfile = None
            num_lines = sum(1 for line in open(chromosome + '.' + pam + '.' + ref_name + '.' + direction + '.txt'))
            lines_per_file = int(num_lines / 99)
            with open(chromosome + '.' + pam + '.' + ref_name + '.' + direction + '.txt') as bigfile:
                first_counter = 0
                second_counter = 0
                for lineno, line in enumerate(bigfile):
                    if lineno % lines_per_file == 0:
                        if smallfile:
                            smallfile.close()
                        if first_counter > 9:
                            first_counter = 0
                            second_counter += 1
                        small_filename = chromosome + '.' + pam + '.' + ref_name + '.' + direction + '.' + str(
                            second_counter) + '.' + str(first_counter) + '.txt'
                        first_counter += 1
                        smallfile = open(small_filename, "w")
                        smallfile.write(reference + '\n')
                        smallfile.write(pattern + '\n')
                    smallfile.write(line)
                if smallfile:
                    smallfile.close()
