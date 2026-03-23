import sys

from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print("hello from process", rank, "of", size)
# local
#../files/mastodon-small.ndjson
file_path = sys.argv[1]

if rank == 0:
    print('Rank 0 executing', file_path)
    with open(file_path) as file_content: 
        while True:
            lines = file_content.readlines()
            if not lines:
                break
            s = 0
            print('lines length', len(lines))
            number_lines = len(lines)
            interval_size = int(number_lines / size)

            # interval of lines per each node
            intervals = [
                (
                    i * interval_size + int(bool(0)),
                    number_lines if i == size - 1 else (i + 1) * interval_size
                ) for i in range(size)]
            interval_lines = []
            for start, end in intervals:
                print('start', start)
                print('end', end)
                interval_lines.append(lines[start:end])
            total_lines = 0
            for line in interval_lines:
                print('length interval', len(line))
                total_lines += len(line)
            print('check total number of lines', total_lines
                  )



