library(dplyr)
library(ggplot2)
library(ape)
library(ggtree)
library(RColorBrewer)
#build two strain trees
setwd("~/projects/tesis/results/2018-02-26/other_strains")
element <- "CZAR"
treepath <- "./msa/msa/curated/"
tablepath <- "./tables_for_allalign/"
treefilename <- paste(treepath,"all_",element,".dnd", sep = "")
tablefilename <- paste(tablepath, element, "_all_basic_info.tsv", sep = "" )
image_output_name <- paste("all_", element,".svg", sep = "")
tree_file <- read.tree(treefilename)
table <- read.table( tablefilename, header = TRUE )

# Plotting trees----
tree <- ggtree(tree_file, layout = "unrooted" )
palette <- c('#f781bf','#ff7f00','#4daf4a','#984ea3','#e41a1c','#ffff33','#a65628','#377eb8')
#corresponde ( bug    ,     clbe,     clbne,    clbx  ,  dm28c  ,   esme   ,  sylvio  ,  tcc    )



(image <- tree %<+% table +
    geom_tippoint( aes(color = strain ) ) + 
    scale_color_manual(values = palette) +
    geom_treescale( x = -0.625 , y = -0.21, width = 0.01, offset = 0.01) +
    ggtitle(element) + 
    theme(legend.position = "right") 
    )

#Guardando imagen----
ggsave(file=image_output_name, plot = image, width = 10, height = 8 )
