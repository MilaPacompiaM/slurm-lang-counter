import sys

from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print("hello from process", rank, "of", size)
# local
#../files/mastodon-small.ndjson
file_path = sys.argv[1]

data = None
lines = []
number_lines = 0
if rank == 0:
    print('Rank 0 executing', file_path)
    with open(file_path) as file_content:
        lines = file_content.readlines()
        print('lines length', len(lines))
        number_lines = len(lines)

number_lines = comm.bcast(number_lines, root=0)
interval_size = int(number_lines / size)

# interval of lines per each node
# TODO: make this calculation in each node and assign more items to first n-1 process by default
intervals = [
    (
        i * interval_size + int(bool(0)),
        number_lines if i == size - 1 else (i + 1) * interval_size
    ) for i in range(size)]

interval_lines = []
if rank == 0:
    for start, end in intervals:
        print('start', start)
        print('end', end)
        interval_lines.append(lines[start:end])

node_lines = comm.scatter(interval_lines, root=0)

# Executing for each node
print('Rank ', rank, ' has ', len(node_lines), 'elems')

if rank == 0:
    print('end')
