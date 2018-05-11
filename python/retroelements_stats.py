#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 14:49:20 2017

@author: gaston
"""

import sys
from Bio import SeqIO
from Bio.SeqUtils import GC
import numpy
import subprocess
import os


inputFasta = sys.argv[1]
element = sys.argv[2]
strain = sys.argv[3]




if os.stat(inputFasta).st_size == 0:
    print( "{0}\t{1}\t0\t-\t-\t-\t-\t-\t-\t".format( element, strain ) )
    sys.exit(0)



seq_dict = {}

headers_list = []

for seq in SeqIO.parse( inputFasta , "fasta" ):
    seq_dict[seq.id] = seq.seq
    header = seq.id
    headers_list.append( header )    


#---------/calcular gc y length/-------

gc_cont = []
lengths = []

for seqid in seq_dict:
    gc = GC( seq_dict[seqid] )
    gc_cont.append( gc )
    length = len( seq_dict[seqid] )
    lengths.append( length )
        
#-------------------------------------


num_seqs = len(headers_list)  

command = [ "blastn" , "-query" , sys.argv[1], "-subject" , sys.argv[1], "-outfmt",
           "6 qseqid sseqid pident", "-out", "blast_out.tmp" ]
subprocess.call(command)

pident_list = []


with open("blast_out.tmp" , 'r' ) as blastout:
    
    for line in blastout:
        pident = float(line.split()[2])
        pident_list.append(pident)
        


for i in range(1 , num_seqs, 1):
    
    sliced_id = pident_list[ i : num_seqs + 1 ]
    pident_list = pident_list + sliced_id
    
    
rm_comm = [ "rm", "blast_out.tmp" ]
subprocess.call(rm_comm)






mean_gc = numpy.mean( gc_cont )
stdev_gc = numpy.std( gc_cont )
mean_length = numpy.mean( lengths )
stdev_length = numpy.std( lengths )
mean_idn = numpy.mean( pident_list )
stdev_idn = numpy.std( pident_list )

output = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t".format( element, strain, num_seqs,
                                                                 mean_length, stdev_length,
                                                                 mean_idn, stdev_idn,
                                                                 mean_gc, stdev_gc)
print(output)

