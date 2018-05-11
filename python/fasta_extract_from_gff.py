#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 11:23:25 2017

@author: gaston
"""

'''message = """ 

This script extracts subsequences from a fasta file and  writes them to a
new fasta files with modified headers including annotation

A fasta file is provided as first input

Sequence name, subsequence coordinates, and subsequence annotation are 
provided as second input:

.gff is provided as second input

An output filename is provided as third input

Usage: <this>.py genome.fa annotation.gff output.fa


"""
'''
#print(message)

from Bio import SeqIO
import sys

inputFasta = sys.argv[1]
inputGFF = sys.argv[2]
output_name = sys.argv[3]

all_ids = []
extracted_ids = []


contigs = {}


print("Loading genome...")

for seq in SeqIO.parse( inputFasta , "fasta" ):
    contigs[seq.id] = seq.seq
    
with open(inputGFF, 'r') as gff, open(output_name , 'w') as output:
    
     print("Extracting sequences...")
     for line in gff:
                
         contig = line.split()[0]
         strand = line.split()[6]
         seq_id = line.split()[8].split(";")[0].split("=")[1]
         start_coord = int(line.split()[3]) - 1
         end_coord = int(line.split()[4])
         annotation = line.split()[8].split(";")[1].split("=")[1]
         complete_header = ">{0}\n".format(seq_id)
                           
         all_ids.append(seq_id)
         
         for contig_name in contigs:
             
             if  contig_name == contig:
                 
                  subsequence = contigs[contig_name][start_coord:end_coord]
                 
                  if strand == "-":
                      rev_sequence = subsequence.reverse_complement()
                      output.write( complete_header )
                      output.write( str(rev_sequence) + "\n" )
                      extracted_ids.append(seq_id)
                  
                      
                  else:
	                  output.write( complete_header )
        	          output.write( str(subsequence) + "\n" )
                	  extracted_ids.append(seq_id) 
                  
         
