library(tidyverse)
setwd("~/projects/tesis/results/2018-02-06")

elements <- c( "L1Tc", "CZAR" )
basicpath<- "./info_tables/basic_info/tables/"
proxpath <- "./info_tables/annotation_proximity/tables/"
actpath <- "./info_tables/activity/tables/"
output_dir <- "./full_tables/"

for ( element in elements ) {
  
  
  basic_table_tcc <- read.table( paste(basicpath,
                                       element, "_" ,
                                       "tcc_basic_info.tsv", sep = ""), header = TRUE )
  prox_table_tcc <- read.table( paste(proxpath,
                                      element, "_" ,
                                      "tcc_proximity.tsv", sep = ""), header = TRUE )
  
  act_table_tcc <- read.table( paste( actpath, 
                                      element, "_",
                                      "tcc_activity.tsv", sep = ""), header = TRUE )
  
  full1_tcc <- full_join( basic_table_tcc , prox_table_tcc, by = "seqid" )

  full_table_tcc <- full_join( full1_tcc, act_table_tcc, by = "seqid" )
  
  basic_table_dm28c <- read.table( paste(basicpath,
                                         element, "_" ,
                                         "dm28c_basic_info.tsv", sep = ""), header = TRUE )
  prox_table_dm28c <- read.table( paste(proxpath,
                                        element, "_" ,
                                        "dm28c_proximity.tsv", sep = ""), header = TRUE )
  act_table_dm28c <- read.table( paste( actpath, 
                                      element, "_",
                                      "dm28c_activity.tsv", sep = ""), header = TRUE )
  full1_dm28c <- full_join( basic_table_dm28c , prox_table_dm28c, by = "seqid" )
  
  full_table_dm28c <- full_join ( full1_dm28c, act_table_dm28c , by = "seqid")
  
  full_table <- full_join(  full_table_tcc, full_table_dm28c   )
  
  output_name <- paste( element, "fulltable.tsv" , sep = "_" )
  
  write.table( full_table , 
               file = paste( output_dir, output_name , sep = "") ,
               na = "NA", 
               sep = "\t", 
               col.names = TRUE, 
               quote = FALSE, 
               row.names = FALSE )
  
}



elements <- c( "NARTc", "VIPER", "SIRE" )
basicpath<- "./info_tables/basic_info/tables/"
proxpath <- "./info_tables/annotation_proximity/tables/"
actpath <- "./info_tables/activity/tables/"
output_dir <- "./full_tables/"

for ( element in elements ) {
  
  
  basic_table_tcc <- read.table( paste(basicpath,
                                       element, "_" ,
                                       "tcc_basic_info.tsv", sep = ""), header = TRUE )
  prox_table_tcc <- read.table( paste(proxpath,
                                      element, "_" ,
                                      "tcc_proximity.tsv", sep = ""), header = TRUE )
  
  full_table_tcc <- full_join( basic_table_tcc , prox_table_tcc, by = "seqid" )
  
  basic_table_dm28c <- read.table( paste(basicpath,
                                         element, "_" ,
                                         "dm28c_basic_info.tsv", sep = ""), header = TRUE )
  prox_table_dm28c <- read.table( paste(proxpath,
                                        element, "_" ,
                                        "dm28c_proximity.tsv", sep = ""), header = TRUE )
  
  full_table_dm28c <- full_join ( basic_table_dm28c , prox_table_dm28c, by = "seqid")
  
  full_table <- full_join(  full_table_tcc, full_table_dm28c   )
  
  output_name <- paste( element, "fulltable.tsv" , sep = "_" )
  
  write.table( full_table , 
               file = paste( output_dir, output_name , sep = "") ,
               na = "NA", 
               sep = "\t", 
               col.names = TRUE, 
               quote = FALSE, 
               row.names = FALSE )
  
}

