#!/bin/bash
#SBATCH --job-name=getLangRank
#SBATCH --partition=sapphire
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=00:10:00
#SBATCH --output=slurm-%j.out

# when running it you should run: sbatch getLangRank.slurm name of file so we can test different files
module load OpenMPI/4.1.4
module load mpi4py/3.1.4

mpirun -np 1 python3 getLangRank.py "$1"
