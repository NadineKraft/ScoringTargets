#!/usr/bin/env python
import csv
import pickle
import argparse
import numpy
import re
import time


# Enter command to run the script: ./score_offinder_files.py
# --off /path/to/the/offinder/file --output /path/to/the/output/file

# Reverse complements a given string
def revcom(s):
    basecomp = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'U': 'A'}
    letters = list(s[::-1])
    letters = [basecomp[base] for base in letters]
    return ''.join(letters)


# Unpickle mismatch scores and PAM scores
def get_mm_pam_scores():
    try:
        mm_scores = pickle.load(open('mismatch_score.pkl', 'rb'))
        pam_scores = pickle.load(open('pam_scores.pkl', 'rb'))
        return mm_scores, pam_scores
    except:
        raise Exception("Could not find file with mismatch scores or PAM scores")


# Calculates CFD score
def calc_cfd(wt, sg, pam):
    mm_scores, pam_scores = get_mm_pam_scores()
    score = 1
    sg = sg.replace('T', 'U')
    wt = wt.replace('T', 'U')
    s_list = list(sg)
    wt_list = list(wt)
    for i, sl in enumerate(s_list):
        if wt_list[i] == sl:
            score *= 1
        else:
            key = 'r' + wt_list[i] + ':d' + revcom(sl) + ',' + str(i + 1)
            score *= mm_scores[key]
    score *= pam_scores[pam]
    return score


def calc_score(first_seq, second_seq):
    pam = second_seq[-2:]
    sg = second_seq[:-3]
    m_wt = re.search('[^ATCG]', first_seq)
    m_off = re.search('[^ATCG]', second_seq)
    if (m_wt is None) and (m_off is None):
        score = calc_cfd(first_seq, sg, pam)
    else:
        score = 0.0
    return score


def get_parser():
    parser = argparse.ArgumentParser(description='Calculates overall CFD score for single files')
    parser.add_argument('--off',
                        type=str,
                        help='--off /path/to/the/offinder/file')
    parser.add_argument('--output',
                        type=str,
                        help='--output /path/to/the/output/file')
    return parser


if __name__ == '__main__':
    args = get_parser().parse_args()
    off = args.off
    output = args.output
    mm_scores, pam_scores = get_mm_pam_scores()
    temp_list = []
    final_list = []
    score = []
    prev_seq = ''

    with open(off, mode='r') as offinder_file:
        reader = csv.reader(offinder_file, delimiter='\t')
        for offinder_row in reader:
            offinder_target_sequence = offinder_row[0].upper()
            if prev_seq == '':
                # first case
                temp_list.append(offinder_row)
            elif prev_seq == offinder_target_sequence:
                # sequencens are equal: append to temp list
                temp_list.append(offinder_row)
            elif prev_seq != offinder_target_sequence and len(temp_list) > 1:
                # sequences differ, multiple items in temp list, calculate mean for items and save
                for list_row in temp_list[1:]:
                    score.append(calc_score(list_row[0], list_row[3].upper()))
                final_list.append([temp_list[0][2], temp_list[0][0], numpy.mean(score)])
                # Set current line as first item
                temp_list = [offinder_row]
                score = []
            elif prev_seq != offinder_target_sequence and len(temp_list) == 1:
                # sequences differ, one entry in templist
                final_list.append([offinder_row[2], offinder_row[0], 0.0])
                temp_list = [offinder_row]
                score = []
            else:
                print('first iteration')
            prev_seq = offinder_target_sequence

        # last iteration
        if len(temp_list) > 1:
            for list_row in temp_list[1:]:
                score.append(calc_score(list_row[0], list_row[3].upper()))
            final_list.append([temp_list[0][2], temp_list[0][0], numpy.mean(score)])
        else:
            final_list.append([offinder_row[2], offinder_row[0], 0.0])

    offinder_file.close()

    with open(output, mode='w') as output:
        # Write output file
        writer = csv.writer(output, lineterminator='\n')
        for result_row in final_list:
            writer.writerow(result_row)

