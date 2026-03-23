
## Commands
- Check my jobs' status

```sh
squeue -u mpacompiamac
```

- Copy local files to remote (Spartan)

```sh
# single file
scp /Users/mila/Downloads/course_files_export/bluesky-small.ndjson mpacompiamac@spartan.hpc.unimelb.edu.au:/home/mpacompiamac/t1


scp /Users/mila/comp90024/a1/comp90024_a1_team_11/getLangRank.py mpacompiamac@spartan.hpc.unimelb.edu.au:/home/mpacompiamac/a1
scp /Users/mila/comp90024/a1/comp90024_a1_team_11/getLangRank.slurm mpacompiamac@spartan.hpc.unimelb.edu.au:/home/mpacompiamac/a1



# copies files directory into a1
scp -r /Users/mila/comp90024/a1/files mpacompiamac@spartan.hpc.unimelb.edu.au:/home/mpacompiamac/a1
```

- Send jobs (in Spartan)
```sh
sbatch getLangRank.slurm
## sample output (unique id)
## Submitted batch job 23076094

# In same directory it should displayed the output like slurm-23076094.out
```

## Local commands
- Run mastodon small file
```sh
mpirun -np 2 python3 getLangRank.py ../files/mastodon-small.ndjson
```

