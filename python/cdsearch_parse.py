#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 18:18:52 2018

@author: gaston
"""
import sys

cd_out = sys.argv[1]
dom_list = sys.argv[2]
outfile = sys.argv[3]

with open( cd_out , 'r' ) as cdout, open( dom_list, 'r' ) as domlist:
    doms = []           #inicializar lista vacia para grupos de dominios
    seqid_dict = {}     #inicializar diccionario para seqids
    
    for line in domlist:        #agregar una lista de dominios a lista de grupos
        dom = set(line.split())
        doms.append(dom)
        
    for line in cdout:
        
        complete = line.split(">")[1].split()[9]        
               
        seqid = line.split(">")[1].split()[0].split("_ORF")[0]       #extraer seqid
        domname = line.split(">")[1].split()[8]                         #extraer nombre corto de dominio
            
        if seqid not in seqid_dict:                                 #si seqid no fue leida ya, inicializar lista vacia en diccionario
            seqid_dict[seqid] = []             
            if complete != "C" and complete != "N" and complete != "NC":      
                seqid_dict[seqid].append(domname)              #agregar dominio a lista asociada a seqid
        else:
            if complete != "C" and complete != "N" and complete != "NC": 
                seqid_dict[seqid].append(domname)              
            
                
with open( outfile, 'w' ) as output:

    output.write("seqid" + "\t" + "active" + "\n" )                
    
    #for i in doms: print(str(i) + "\n" )
    for seqid in seqid_dict:
        
        domlist = set(seqid_dict[seqid])
        activity = []                         #lista logica, la idea es que sea activo solo si todos los elementos de esta lista son true
        
        
        for grupo in doms:                      #para cada grupo de dominios relevante
            overlap = list(domlist.intersection(grupo))     #calcular la interseccion entre los dos grupos
            
            if len(overlap) >= 2:                          #si mas de un domimnio es compartido entre grupo relevante y domiinos de seqid
                activity.append(True)         
            else:
                activity.append(False)                                                #agregar true para activity
            
        #print( str(len(activity)) + " " + str(activity.count( True )))       
        if len(activity) == activity.count( True ):     #si todos los elementos de activity son verdaderos 
            output.write( seqid + "\t" + "TRUE" + "\n" )
        else:
            output.write( seqid + "\t" + "FALSE" + "\n" )
            













