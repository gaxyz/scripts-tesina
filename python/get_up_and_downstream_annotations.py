#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 14:22:29 2018

@author: grijo
"""

"""

This script gets annotations at the 5' and 3' ends of a set of annotations

This script is meant to parse two gff files

First input should be a .gff file containing a series of annotations which knowing what's upstream and downstream matters.

Second input should be the whole genome .gff

Third input should be the output's desired name

------------------------------------------------
The output should be an R parseable file like:

name    5'   3'

CZAR_1  annot annot 
-------------------------------------------------


The script works parsing the .gff files and getting 
the first annotation upstream and downstream 
relative to the annotation of interest


Obviously it's very important for the sense to be specified in the seqs of interest .gff files


The N/A values can be the result of either of these two things:
    
-no sense was specified
-there are no annotations up/downstream


"""

import sys

#-------------------------------------
#Define a function that calculates nearest 5' and 3' annotation given
#5' coordinate
#3' coordinate
#sense
#
#every annotation is in the same contig in a dict

def close_annot(five_coord, three_coord, gene_sense, ids_dict):
    #dict must be:
    # ids_dict[geneid] = [start, end]   containing all annotations for a given contig 
    #get closest to five_coord
    
    
    if not ids_dict:                                                #si el diccionario esta vacio
        return("NA", "NA", "NA", "NA")
        
    
    if gene_sense == "+":                                                         #aclarar el sentido xq de esto depende el signo de las cuentas
        
        closest_to_five = float("inf")                                             # asignar infinito para que cualquier numero sea menor que el que contiene la variable
        closest_to_three = float("inf")
                
        for key in ids_dict:                                                       #para cada gen del mismo contig
            
                dist_to_five = five_coord - max( ids_dict[key][0], ids_dict[key][1] )       #calcular distancia tomando 5' como ref  (solo me interesan valores positivos)
                dist_to_three = min( ids_dict[key][0], ids_dict[key][1] ) - three_coord     #calcular distancia tomando gen como ref (solo me interesan valores positivos)
                
                if dist_to_five < closest_to_five and dist_to_five > 0:                     #si la nueva distancia calculada es menor a la distancia calculada previamente, quedarse con la nueva
                    closest_to_five = dist_to_five
                    gene_upstream = key                                                     # quedarse con el id del gen tambien
                else:
                    pass
                if dist_to_three < closest_to_three and dist_to_three > 0:                  #lo mismo pero para 3'
                    closest_to_three = dist_to_three
                    gene_downstream = key
                else: 
                    pass
        
        if closest_to_five == float("inf"):
            gene_upstream = "NA"
            closest_to_five = "NA"
        if closest_to_three == float("inf"):
            gene_downstream = "NA"
            closest_to_three = "NA"
        
        return( gene_upstream , gene_downstream, closest_to_five, closest_to_three)        
    elif gene_sense == "-":                                                             #como los signos cambian si el sentido es otro, le meto un elif
                                                                                        #y todo lo demas es basicamente lo mismo
        closest_to_five = float("inf")
        closest_to_three = float("inf")
                
        for key in ids_dict:
            
                dist_to_five = max( ids_dict[key][0], ids_dict[key][1] ) - five_coord
                dist_to_three = three_coord - min( ids_dict[key][0], ids_dict[key][1] )
                
                if dist_to_five < closest_to_five and dist_to_five > 0:
                    closest_to_five = dist_to_five
                    gene_upstream = key
                else:
                    pass
                if dist_to_three < closest_to_three and dist_to_three > 0:
                    closest_to_three = dist_to_three
                    gene_downstream = key
                else: 
                    pass
                
        if closest_to_five == float("inf"):
            gene_upstream = "NA"
            closest_to_five = "NA"
        if closest_to_three == float("inf"):
            gene_downstream = "NA"
            closest_to_three = "NA"
                
        return( gene_upstream , gene_downstream , closest_to_five, closest_to_three)
    elif gene_sense == ".":
        return( "NA", "NA", "NA", "NA" )

#----------------------------------------------------------------

gene_gff = sys.argv[1]
genome_gff = sys.argv[2]
outfile = sys.argv[3]

gene_dict = {}
genome_dict = {}

#Load gene .gff into a dictionary
#--------------------------------------------------------

with open( gene_gff, 'r' ) as gene_annot:
    
    print("Loading {0}...".format(gene_gff))    
    
    for line in gene_annot:
        
        contig, source, feature, start, end, score, strand, frame, attribute = line.split()
        geneid = attribute.split(";")[0].replace("id=", "")
        
        if strand == "-":
            five_prime = int(end)
            three_prime = int(start)
        elif strand == "+":
            five_prime = int(start)
            three_prime = int(end)
        else:
            pass
        

        gene_dict[geneid] = [contig, five_prime, three_prime, strand]
               
        
        
#Load genome .gff into a dictionary       
with open( genome_gff , 'r' ) as genome_annot:
    
    print( "Loading {0}".format(genome_gff) )
    for line in genome_annot:

        contig, source, feature, start, end, score, strand, frame, attribute = line.split()

        geneid = attribute.split(";")[0].replace("id=", "")

        genome_dict[geneid] = [ contig, int(start), int(end), strand, attribute ]
        

#--------------------------------------


with open( outfile, 'w' ) as output:
    

    output.write('seqid\tupstream_closest_id\tdownstream_closest_id\tupstream_annot\tdownstream_annot\tup_dist\tdown_dist\n')

    

    for gene in gene_dict:                                                                       # para cada gen de interes

        gene_contig = gene_dict[gene][0]                                                        # esclarecer todas las variables que voy a usar
        five_coord = gene_dict[gene][1]
        three_coord = gene_dict[gene][2]
        sense = gene_dict[gene][3]
    
        genome_coords_dict = {}                                                               #crear diccionario para almacenar coordenadas de gff genoma, y luego parsear con close_annot
  
        for genome in genome_dict:                                                              #para cada anotacion del genoma
        
            genome_contig = genome_dict[genome][0]                                                      #esclarecer contig
        
            if genome_contig == gene_contig:                                                    # si gen y anotacion estan en el mismo contig
                        
                        start = genome_dict[genome][1]  
                        end = genome_dict[genome][2]                       
                        genome_coords_dict[genome] = [start, end]                               # almacenar informacion en el diccionario de coordenadas de gff del genoma
            
            
        closest = close_annot( five_coord,  three_coord, sense, genome_coords_dict )            #calcular anotaciones mas cercanas        
    
        seqid = gene

                       
                                                              
        upstream = closest[0]
        downstream = closest[1]
        up_dist = closest[2]
        down_dist = closest[3]
        try:
            try:
                up_annot = genome_dict[upstream][4].split("prod=")[1].split(";")[0]
            except IndexError:
                up_annot = genome_dict[upstream][4].split("id=")[1]
        except KeyError:
            up_annot = "NA"
        try:
            try:
                down_annot = genome_dict[downstream][4].split("prod=")[1].split(";")[0]
            except IndexError:
                down_annot = genome_dict[downstream][4].split("id=")[1]
        except KeyError:
            down_annot = "NA"
        
        output.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n".format( seqid, upstream, downstream, up_annot, down_annot, up_dist, down_dist ))
    







