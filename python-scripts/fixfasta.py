#!/usr/bin/env python

import argparse

def get_arguments():
    parser = argparse.ArgumentParser(description="This script takes a fasta file \
        with sequences on multiple lines and combines them into a single line \
        for easier parsing.")
    parser.add_argument("-i", "--infile1", help="Takes a .fa file in",\
                        required=True, type=argparse.FileType('r'))
    parser.add_argument("-o", "--outfile", help="Name of the output file",\
                        required=True, type=argparse.FileType('w'))
    return parser.parse_args()

args=get_arguments()

# Open our fasta file for reading
with args.infile1 as fh:
    # open our outfile for writing
    with args.outfile as outfile:
        # Make a bool to tell us we're on the first line
        firsttime=True
        # read through file line by line
        for line in fh:
            # If the first char of line is ">" (we're on a name line)
            if line[0] == '>':
                # If we're not on the first entry, we've got sequence in
                # the line before, so print a newline, then the next name
                if firsttime==False:
                    print("\n", line.strip(), sep="", file=outfile)
                # Otherwise, we are on the first entry, so just print it
                else:
                    print(line.strip(), file=outfile)
                    firsttime=False
            # If the first char isn't a ">", we're on a sequence line
            else:
                # so strip the newline character and print that out
                print(line.strip(), end="", file=outfile)
        # Add a newline character at the end of the file
        print("\n", end="", file=outfile)
