#!/bin/bash

#SBATCH -A b2013064
#SBATCH -p node
#SBATCH -t 2-00:00:00

module add bioinfo-tools
module add bowtie/1.1.0
module add mirdeep2/2.0.0.5
module add gnuplot/4.6.5
module add R/3.0.1

cd $1
perl $2 config.txt -s -t -u -v
