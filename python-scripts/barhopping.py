#!/usr/bin/env python

import argparse
import matplotlib
import matplotlib.pyplot as plt


def get_arguments():
    parser = argparse.ArgumentParser(description="This script reads through a \
fastq file and generates per base quality scores and average quality score graphs.")
    parser.add_argument("-i", "--infile", help="Takes a .fa file in",\
                        required=True, type=argparse.FileType('r'))
    parser.add_argument("-o", "--outfile", help="Name of the output file",\
                        required=True, type=str)
    parser.add_argument("-p", "--outfile2", help="Name of the output file",\
                        required=True, type=str)
    parser.add_argument("-r", "--rname", help="Name/Number of the read",\
                        required=True, type=str)
    return parser.parse_args()

args=get_arguments()

def convert_phred(base):
    '''Converts ASCII character to Phred score. Phred score = ASCII-33'''
    return ord(base)-33

# Read through file and add quality scores to array by bp
# Also append average quality score for the line to 
with args.infile as fh:
    NR = 0
    allmeans=[]
    for line in fh:
        meanline=0
        NR += 1
        line=line.strip("\n")
        if NR == 2:
            mean_scores=[0.0]*len(line)
        if NR % 4 == 0:
            for j in range(len(line)):
                mean_scores[j]+=convert_phred(line[j])
                meanline+=convert_phred(line[j])
            meanline=meanline/len(line)
            allmeans.append(meanline)
        if NR % 1000000 == 0:
            print("Processing line: ", NR, sep="")

for i in range(len(mean_scores)):
    mean_scores[i]=mean_scores[i]/(NR/4)

# Make phred score/bp plot and output to file
plt.title("Avg Phred Score per base position, " + args.rname)
plt.xlabel("Base position", size="large")
plt.ylabel("Phred Score", size="large")
plt.ylim(15,42)
plt.plot(mean_scores)
plt.savefig(args.outfile)
plt.clf()

# Make quality score histogram and output to file
# use log scale on Y-axis
plt.title("Histogram of read quality, " + args.rname)
plt.xlabel("Average quality score across read", size="large")
plt.ylabel("# of reads", size="large")
plt.ylim(1000,400000000)
plt.xlim(10,42)
plt.hist(allmeans)
plt.yscale("log", nonposy="clip")
plt.savefig(args.outfile2)
plt.clf()
