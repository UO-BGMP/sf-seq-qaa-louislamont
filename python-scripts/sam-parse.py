#!/usr/bin/env python

import argparse
import re

def get_arguments():
    parser = argparse.ArgumentParser(description="This script takes a SAM \
    file and reports the number of mapped and unmapped reads.")
    parser.add_argument("-i", "--samfile", help="Takes a sam file in", \
                        required=True, type=argparse.FileType('r'))
    return parser.parse_args()

args=get_arguments()

# Initialize the mapped/unmapped counts
mapped = 0
unmapped = 0

# Read through SAM file
with args.samfile as file:
    for line in file:
        # Exclude the headers with regex
        if not re.search("^@", line):
            # Split line and save flag
            splitline = line.strip().split("\t")
            flag = int(splitline[1])
            
            # if flag&4 is 4, read is unmapped
            if (flag&4)==4:
                unmapped+=1
                
            # if flag&4 is 0, read is mapped
            # if flag&256 is 0, the read is a primary alignment
            # (exclude secondary alignments/duplicates)
            if (flag&4)==0 and (flag&256)==0:
                mapped+=1
                
#Print our stuff:
print("Unmapped:", unmapped)
print("Mapped:", mapped)
print("% Mapped:", mapped/(unmapped+mapped)*100)
