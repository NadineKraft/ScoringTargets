# !/usr/bin/env python
# Script to merge scored cas-offinder-files
# Usage: ./merge_all.py --input /path/to/scored/input/files/directory --output /path/to/output/files/directory
# --name NGG.GRCh38

import csv
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Merge scored files")
    parser.add_argument("--input", type=str, help="Path/to/scored/input/files/directory", required=True)
    parser.add_argument("--output", type=str, help="Path/to/merged/and/scored/output/files/directory", required=True)
    parser.add_argument("--name", type=str, help="File naming convention: E.g.: NGG.GRCh38", required=True)
    args = parser.parse_args()
    input_directory = args.input
    output_directory = args.output
    name = args.name

    chromosomes = {'chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9', 'chr10', 'chr11', 'chr12',
                   'chr13', 'chr14', 'chr15', 'chr16', 'chr17', 'chr18', 'chr19', 'chr20', 'chr21', 'chrX', 'chrY',
                   'chr24'}

    direction_list = ['forward', 'reverse']

    for direction in direction_list:
        for chromosome in chromosomes:
            with open(output_directory + chromosome + '.' + name + '.' + direction + '.csv',
                      "w") as forward_csv_file:
                first_counter = 0
                second_counter = 0
                while first_counter <= 9 and second_counter <= 9:
                    with open(input_directory + chromosome + '.' + name + '.' + direction + '.' + str(
                            second_counter) + '.' + str(
                            first_counter) + '.score.txt', mode='r') as forward_input:
                        first_counter += 1
                        if first_counter > 9:
                            first_counter = 0
                            second_counter += 1
                        input_file = csv.reader(forward_input, delimiter=',')
                        output_writer = csv.writer(forward_csv_file, lineterminator='\n')
                        for row in input_file:
                            output_writer.writerow(row)
