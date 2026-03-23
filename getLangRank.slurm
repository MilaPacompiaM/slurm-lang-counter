#!/bin/bash
#SBATCH --ntasks=2

module load OpenMPI/4.1.4
module load mpi4py/3.1.4

mpirun -np 2 python3 getLangRank.py

my-job-stats -a -n -s