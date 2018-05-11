library(tidyverse)
element <- "SIRE"
cepa <- "tcc"
#------load tables


full_table <- read.table(file = paste("./full_tables/" , element, "_fulltable.tsv" , sep = ""),
                         header = TRUE)

#-----Thresholds and filtering-----
dist_thold <- 1000


#----Tabla----

up_filtered_tcc <- filter( full_table , 
                       up_dist < dist_thold, strain == "tcc"  )
down_filtered_tcc <- filter( full_table , 
                       down_dist < dist_thold, strain == "tcc" )

up_count_tcc <- as.data.frame(table(up_filtered_tcc$upstream_annot))
colnames(up_count_tcc) <- c("annot", "count")
up_count_tcc <- filter(up_count_tcc, count > 0 )


down_count_tcc <- as.data.frame(table(down_filtered_tcc$downstream_annot))
colnames(down_count_tcc) <- c("annot", "count")
down_count_tcc <- filter(down_count_tcc , count > 0)

#----Tabla tcc----

up_filtered_tcc <- filter( full_table , 
                           up_dist < dist_thold, strain == "tcc"  )
down_filtered_tcc <- filter( full_table , 
                             down_dist < dist_thold, strain == "tcc" )

up_count_tcc <- as.data.frame(table(up_filtered_tcc$upstream_annot))
colnames(up_count_tcc) <- c("annot", "count")
up_count_tcc <- filter(up_count_tcc, count > 0 )


down_count_tcc <- as.data.frame(table(down_filtered_tcc$downstream_annot))
colnames(down_count_tcc) <- c("annot", "count")
down_count_tcc <- filter(down_count_tcc , count > 0)


up_count_tcc$strain <- rep("tcc", times = length(up_count_tcc$annot))
up_count_tcc$stream <- rep("upstream", times = length(up_count_tcc$annot))
down_count_tcc$strain <- rep("tcc", times = length(down_count_tcc$annot))
down_count_tcc$stream <- rep("downstream", times = length(down_count_tcc$annot))


tcc_annotations <- full_join(up_count_tcc, down_count_tcc)


#----Tabla dm28c----

up_filtered_dm28c <- filter( full_table , 
                           up_dist < dist_thold, strain == "dm28c"  )
down_filtered_dm28c <- filter( full_table , 
                             down_dist < dist_thold, strain == "dm28c" )

up_count_dm28c <- as.data.frame(table(up_filtered_dm28c$upstream_annot))
colnames(up_count_dm28c) <- c("annot", "count")
up_count_dm28c <- filter(up_count_dm28c, count > 0 )


down_count_dm28c <- as.data.frame(table(down_filtered_dm28c$downstream_annot))
colnames(down_count_dm28c) <- c("annot", "count")
down_count_dm28c <- filter(down_count_dm28c , count > 0)


up_count_dm28c$strain <- rep("dm28c", times = length(up_count_dm28c$annot))
up_count_dm28c$stream <- rep("upstream", times = length(up_count_dm28c$annot))
down_count_dm28c$strain <- rep("dm28c", times = length(down_count_dm28c$annot))
down_count_dm28c$stream <- rep("downstream", times = length(down_count_dm28c$annot))


dm28c_annotations <- full_join(up_count_dm28c, down_count_dm28c)



#----Write tables-----

both_annotations <- full_join( tcc_annotations , dm28c_annotations)

write.table(both_annotations, 
            file = paste("info_tables/", element, "_cis_annotations.tsv", sep =""), 
            sep = "\t", 
            col.names = TRUE,
            quote = FALSE,
            row.names = FALSE)













