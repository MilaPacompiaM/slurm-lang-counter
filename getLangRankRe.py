import sys
import re
import json

from collections import Counter
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
# currently for 4 processor and 10 rows -> 2, 2, 2, 4
# it should be preferably 3, 3, 3, 1
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
# language_regex = r'("language")\s*(:)(\s*)(("([^"]*)")|\[.*\])(\s*),(\s*)'
langs_regex = r'("langs"|"language")\s*(:)(\s*)(("([^"]*)")|\[\s*"[^"]*"(?:\s*,\s*"[^"]*")*\s*\])(\s*),(\s*)'
string_array_regex = r'\[\s*"[^"]*"(?:\s*,\s*"[^"]*")*\s*\]'
string_regex = r'"([^"]*)"'
# string_array_regex = r''
counter = Counter()

for idx, node_line in enumerate(node_lines):
    # TODO: join match_result and match_result_langs logic
    match_result = re.search(langs_regex, node_line)
    # match_result_langs = re.search(langs_regex, node_line)
    if match_result:
        value = match_result.group(4)
        print('value', value)
        if value:
            array_string_value = re.search(string_array_regex, value)
            string_value = re.search(string_regex, value)
            array_strings = json.loads(value) if array_string_value else [string_value.group(1)]
            # print('string_value', string_value.group(1))
            counter.update(array_strings)
    # elif match_result_langs:
    #     value = match_result_langs.group(4)
    #     if value:
    #         array_strings = json.loads(value)
    #         counter.update(array_strings)
        # print('array_strings', array_strings)


all_counters = comm.gather(counter, root=0)

print('all_counters', all_counters)
if rank == 0:
    global_counter = Counter()
    for iter_counter in all_counters:
        global_counter.update(iter_counter)
    print('ANSWER')
    print(global_counter.most_common(10))
    print('end')
