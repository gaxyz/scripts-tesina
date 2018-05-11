library(dplyr)
library(ggplot2)
library(ape)
library(ggtree)
#build two strain trees
setwd("~/projects/tesis/results/2018-02-06/")

#elements <- c("CZAR", "L1Tc", "NARTc", "SIRE", "VIPER" ) 
# Loading files ----
element <- "SIRE"
treefilename <- paste("both_",element,".dnd", sep = "")
tablefilename <- paste(element, "_fulltable.tsv", sep = "" )
image_output_name <- paste("both_", element,".svg", sep = "")
outpath <- "./plots/"
tree_file <- read.tree(paste("./msa/both/curated/" , treefilename , sep = "" ) )
table <- read.table( paste( "./full_tables/", tablefilename , sep = "" ), header = TRUE )

# Plotting trees----


tree <- ggtree(tree_file, layout = "unrooted" )
tree <- tree %<+% table + geom_tippoint( aes(color =  strain)  ) + scale_color_manual(values=c("#A70F01", "#151599"))
tree <- tree + theme(legend.position = "right")
(image <- tree + geom_treescale( x = -37 , y = -16.3, width = 0.02, offset = 0.03) + 
    ggtitle(element)) 

#Guardando imagen----
ggsave(file=paste(outpath,image_output_name, sep = ""), plot = image, width = 10, height = 10 )
