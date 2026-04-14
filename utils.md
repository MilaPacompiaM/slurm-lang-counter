
## Commands
- Run everything
```sh
# prerequisite: symbolic links must be made
# copy and paste next items
scp -r /{PATH_TO_DIRECTORY}/team-11-scripts {YOUR_USERNAME}@spartan.hpc.unimelb.edu.au:/home/{YOUR_USERNAME}

# next lines should be executed in SPARTAN
cd team-11-scripts
sbatch --job-name=M_L_c11 getLangRankRe11.slurm ../mastodon-large.ndjson
sbatch --job-name=M_L_c18 getLangRankRe18.slurm ../mastodon-large.ndjson
sbatch --job-name=M_L_c24 getLangRankRe24.slurm ../mastodon-large.ndjson
sbatch --job-name=B_L_c11 getLangRankRe11.slurm ../bluesky-large.ndjson
sbatch --job-name=B_L_c18 getLangRankRe18.slurm ../bluesky-large.ndjson
sbatch --job-name=B_L_c24 getLangRankRe24.slurm ../bluesky-large.ndjson
```

- Check my jobs' status

```sh
squeue -u mpacompiamac
```

- Copy local files to remote (Spartan)

```sh
# single file
scp /Users/mila/Downloads/course_files_export/bluesky-small.ndjson mpacompiamac@spartan.hpc.unimelb.edu.au:/home/mpacompiamac/t1


scp /Users/mila/comp90024/a1/comp90024_a1_team_11/getLangRank.py mpacompiamac@spartan.hpc.unimelb.edu.au:/home/mpacompiamac/a1
scp /Users/mila/comp90024/a1/comp90024_a1_team_11/getLangRankRe.slurm mpacompiamac@spartan.hpc.unimelb.edu.au:/home/mpacompiamac/a1


# copies files directory into a1
scp -r /Users/mila/comp90024/a1/files mpacompiamac@spartan.hpc.unimelb.edu.au:/home/mpacompiamac/a1
```

- Send jobs (in Spartan)
```sh
sbatch getLangRank.slurm

sbatch getLangRankRe.slurm
## sample output (unique id)
## Submitted batch job 23076094

# In same directory it should displayed the output like slurm-23076094.out
```

## Execution in SPARTAN

### Pre-requisites

1. Copy the scripts from local to remote as follows

```sh
scp /Users/mila/comp90024/a1/comp90024_a1_team_11/slurm-scripts/getLangRankRe11.slurm mpacompiamac@spartan.hpc.unimelb.edu.au:/home/mpacompiamac/a1
scp /Users/mila/comp90024/a1/comp90024_a1_team_11/slurm-scripts/getLangRankRe18.slurm mpacompiamac@spartan.hpc.unimelb.edu.au:/home/mpacompiamac/a1
scp /Users/mila/comp90024/a1/comp90024_a1_team_11/slurm-scripts/getLangRankRe24.slurm mpacompiamac@spartan.hpc.unimelb.edu.au:/home/mpacompiamac/a1
scp /Users/mila/comp90024/a1/comp90024_a1_team_11/getLangRankRe.py mpacompiamac@spartan.hpc.unimelb.edu.au:/home/mpacompiamac/a1
```

2. Create symbolic links as detailed in the assignment specification.

3. Execute next commands to send jobs

```sh
# Job name format is {DATASET}_{SIZE}_c{CONFIG}
# DATASET: M (mastodon) or B (bluesky)
# SIZE: S, M, L
# CONFIG: 11 (1 node, 1 core), 18 (1 node, 8 core), 24 (2 node, 8 core)

# Mastodon small file
sbatch --job-name=M_S_c11 getLangRankRe11.slurm mastodon-small.ndjson
sbatch --job-name=M_S_c18 getLangRankRe18.slurm mastodon-small.ndjson
sbatch --job-name=M_S_c24 getLangRankRe24.slurm mastodon-small.ndjson
# Mastodon medium file
sbatch --job-name=M_M_c11 getLangRankRe11.slurm mastodon-medium.ndjson
sbatch --job-name=M_M_c18 getLangRankRe18.slurm mastodon-medium.ndjson
sbatch --job-name=M_M_c24 getLangRankRe24.slurm mastodon-medium.ndjson
# Mastodon large file
sbatch --job-name=M_L_c11 getLangRankRe11.slurm mastodon-large.ndjson
sbatch --job-name=M_L_c18 getLangRankRe18.slurm mastodon-large.ndjson
sbatch --job-name=M_L_c24 getLangRankRe24.slurm mastodon-large.ndjson

# Bluesky small file
sbatch --job-name=B_S_c11 getLangRankRe11.slurm bluesky-small.ndjson
sbatch --job-name=B_S_c18 getLangRankRe18.slurm bluesky-small.ndjson
sbatch --job-name=B_S_c24 getLangRankRe24.slurm bluesky-small.ndjson
# Bluesky medium file
sbatch --job-name=B_M_c11 getLangRankRe11.slurm bluesky-medium.ndjson
sbatch --job-name=B_M_c18 getLangRankRe18.slurm bluesky-medium.ndjson
sbatch --job-name=B_M_c24 getLangRankRe24.slurm bluesky-medium.ndjson
# Bluesky large file
sbatch --job-name=B_L_c11 getLangRankRe11.slurm bluesky-large.ndjson
sbatch --job-name=B_L_c18 getLangRankRe18.slurm bluesky-large.ndjson
sbatch --job-name=B_L_c24 getLangRankRe24.slurm bluesky-large.ndjson
```
4. Write all ids
```sh
23477343, 23477366, 23477367, 23477368, 23477369, 23477373, # then large files
23477380, 23477381, 23477382, 23477384, 23477385, 23477386 # then large files

# inline
23477343,23477366,23477367,23477368,23477369,23477373,23477380,23477381,23477382,23477384,23477385,23477386
```
5. Save statistic information in `test_sm_results.txt`
```sh
sacct -j 23477343,23477366,23477367,23477368,23477369,23477373,23477380,23477381,23477382,23477384,23477385,23477386 --format=JobName,Elapsed,CPUTime,MaxRSS,State --noheader > test_sm_results.txt
```

6. Plot results

7. Run large files
```sh
sacct -j 23478499 --format=JobName,Elapsed,CPUTime,MaxRSS,State
```
8. Final
```sh
# mastodon
23574414
23574416
23574418

23574419
23574420
23574421

23574422
23574423
23575565

#bluesky
23575571
23575572
23575574

23575692
23575693
23575694

23575725
23575726
23575771
## then
sacct -j  23574414,23574416,23574418,23574419,23574420,23574421,23574422,23574423,23575565,23575571,23575572,23575574,23575692,23575693,23575694,23575725,23575726,23575771 --format=JobName,Elapsed,CPUTime,MaxRSS,State --noheader > final_results.txt
```

Results
```
-rw-rw-r-- 1 mpacompiamac COMP90024  115 Apr  3 17:34 slurm-23574414.out
-rw-rw-r-- 1 mpacompiamac COMP90024  115 Apr  3 17:34 slurm-23574416.out
-rw-rw-r-- 1 mpacompiamac COMP90024  115 Apr  3 17:34 slurm-23574418.out
-rw-rw-r-- 1 mpacompiamac COMP90024  125 Apr  3 17:34 slurm-23574419.out
-rw-rw-r-- 1 mpacompiamac COMP90024  125 Apr  3 17:35 slurm-23574420.out
-rw-rw-r-- 1 mpacompiamac COMP90024  125 Apr  3 17:34 slurm-23574421.out
-rw-rw-r-- 1 mpacompiamac COMP90024  160 Apr  3 17:38 slurm-23574422.out
-rw-rw-r-- 1 mpacompiamac COMP90024  160 Apr  3 17:36 slurm-23574423.out
```

## Local commands
- Run mastodon small file
```sh
mpirun -np 2 python3 getLangRank.py ../files/mastodon-small.ndjson
```

## Executions
- Test of Small files

```sh
# mastodon
# small
Submitted batch job 23304920
# medium
Submitted batch job 23305143

```

```sh
# bluesky
# small
Submitted batch job 23304921
# medium
Submitted batch job 23305088

```

- Get stats about jobs
```sh
sacct -j <JOB_ID> -l
# save it
sacct -j <JOB_ID> -l > stats-<JOB_ID>.txt

```

## TODO

- Check language data is not corrupted e.g. 'ENGLL', 'franch'.
