#!/bin/bash

for i in `seq 0 35000 190000`
do
    j=`echo $i+35000 | bc -l`
    echo "/home/xh/work/for_singh/rna_seq/microarray_cluster-c $1 $2 $i $j > $i\_out.txt"
done
