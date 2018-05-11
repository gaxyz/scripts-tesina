#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 16:37:57 2017

@author: grijo

Usage: this.py <blastout_file> <gff_outfile> <element_name> <strain> <cov_thold> <idn_thold>
"""

import sys

element = sys.argv[3]
strain = sys.argv[4]

cov_thold = float(sys.argv[5])
idn_thold = float(sys.argv[6])


with open( sys.argv[1] , 'r' ) as blastout, open( sys.argv[2], 'w' ) as gff:
   
    counter = 0
    for line in blastout:
        
        qseqid, sseqid, qstart, qend, sstart, send, length, pident, qcovhsp, sstrand, evalue = line.split()
        
        if float(qcovhsp) >= cov_thold and float(pident) >= idn_thold:             #write gff
            
            counter += 1
            
            seqname = sseqid
            source = "blastn"
            feature = "retrotransposable_element"
            start = min( int(sstart), int(send) )
            end = max( int(sstart), int(send) )
            score = evalue

            if sstrand=="minus":
		strand="-"
	    elif sstrand=="plus":
		strand="+"
	    else:
		strand="."

            frame = "."
                        
            seq_id = "{0}_{1}_{2}".format(element, strain, counter)
            name = seq_id
            annot = element + "|" + strain 
            
            attributes = "id={0};annot={1};source_id={2};length={3};qcovhsp={4},pident={5}".format( name, annot,seqname ,length, qcovhsp, pident)            
            
            gff_line = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\n".format(seqname, source, feature, start, end, score, strand, frame, attributes)
            
            gff.write(gff_line)
            
