import sys
import re
import json
import os

from collections import Counter
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

file_path = sys.argv[1]
file_size = os.path.getsize(file_path)

# Each rank is responsible for a byte range of the file
start_byte = rank * file_size // size
end_byte = (rank + 1) * file_size // size

langs_regex = r'("langs"|"language")\s*(:)(\s*)(("([^"]*)")|\[\s*"[^"]*"(?:\s*,\s*"[^"]*")*\s*\])(\s*),(\s*)'
string_array_regex = r'\[\s*"[^"]*"(?:\s*,\s*"[^"]*")*\s*\]'
string_regex = r'"([^"]*)"'
counter = Counter()

with open(file_path, 'rb') as f:
    # If not rank 0, skip the partial line at the boundary to avoid double-counting
    if start_byte > 0:
        f.seek(start_byte - 1)
        f.readline()  # advance to the start of the next complete line

    while True:
        pos = f.tell()
        if pos >= end_byte:
            break
        line_bytes = f.readline()
        if not line_bytes:
            break
        line = line_bytes.decode('utf-8', errors='replace')

        match_result = re.search(langs_regex, line)
        if match_result:
            value = match_result.group(4)
            if value:
                array_string_value = re.search(string_array_regex, value)
                string_value = re.search(string_regex, value)
                array_strings = json.loads(value) if array_string_value else [string_value.group(1)]
                counter.update(array_strings)

all_counters = comm.gather(counter, root=0)

if rank == 0:
    global_counter = Counter()
    for iter_counter in all_counters:
        global_counter.update(iter_counter)
    most_common_lang = global_counter.most_common(10)
    print('Language Used, Frequency of occurence (#posts)')
    for i in most_common_lang:
        print('{}, {}'.format(i[0], i[1]))
