#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 23:26:50 2017

el uso tendria que ser igual que getorf
agregar edicion de header adecuada

pero por ahora es:
    
./this.py input_fasta.fna output_fasta.faa minsize

"""

import sys
import subprocess
#import argparse
import time
from Bio import SeqIO

'''
parser = argparse.ArgumentParser( description = "Correr getorf de forma mas util")





'''


minsize = sys.argv[3]
maxsize = sys.argv[4]
inputFasta = sys.argv[1]

inSeqs = {}

print("Reading input fasta...")
for sequence in SeqIO.parse( inputFasta , "fasta" ):              #cargar secuencias a diccionario
    inSeqs[sequence.id] = sequence.seq                        


with open(sys.argv[2], 'w') as output:                           #abrir archivo de output final
    
    for entry in inSeqs:                                         #para cada seq de input
    
        seqid = entry.split("|")[0].replace( ">", "" )
        annotation = "|".join( entry.split( "|" )[1:] )
        
        
        with open("temporary_fasta.fna.tmp", 'w') as temp:       #escribir secuencia en archivo temporal
            temp.write( ">{0}\n".format(entry) )
            temp.write( str(inSeqs[entry]) + "\n" )
            
        run_getorf = ['getorf', "-find", "1" , "-reverse", "0" , "-minsize" ,minsize ,"-maxsize", maxsize ,"-sequence", "temporary_fasta.fna.tmp", "-outseq",  \
                     "getorf_temp.tmp" ]                                            #definir comando
        subprocess.call(run_getorf)                                                #correr getorf
        time.sleep(0.3)
        
        subprocess.call( ["rm", "temporary_fasta.fna.tmp" ])
        subprocess.call( ["sed" ,"-i" ,'s/ /_/g', "getorf_temp.tmp" ] )
        
        getorf_dict = {}
        for sequence in SeqIO.parse( "getorf_temp.tmp", "fasta"):                   #cargar output de getorf a diccionario
            getorf_dict[sequence.id] = sequence.seq
        
        subprocess.call( ["rm", "getorf_temp.tmp" ] )
        
        orf_counter = 0
        for orf in getorf_dict:
            orf_counter += 1
            
            coordinates = orf.split("[")[1].replace("_", "").replace("]", "")
            
            output.write( ">{0}_ORF{1}|{2}\n".format( seqid, str(orf_counter), coordinates ) )       #le agrego que orf es
            output.write( str(getorf_dict[orf]) + "\n" )
            


            
            
            
            
    
