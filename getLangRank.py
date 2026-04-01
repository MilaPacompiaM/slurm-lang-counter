import sys
import re
import json
#We should use json and not regex based on assignment description
import time
from collections import Counter
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print("hello from process", rank, "of", size)
# local
#../files/mastodon-small.ndjson

#handle IndexError if no filename is passed
if len(sys.argv) < 2:
    if rank == 0:
        print("Usage: python3 getLangRank.py <file_path>")
    sys.exit(1)

file_path = sys.argv[1]


data = None
lines = []
number_lines = 0
interval_lines = None

if rank == 0:
    print('Rank 0 executing', file_path)
    with open(file_path) as file_content:
        lines = file_content.readlines()
        print('lines length', len(lines))
        number_lines = len(lines)

number_lines = comm.bcast(number_lines, root=0)


#interval_size = int(number_lines / size)

# interval of lines per each node
# TODO: make this calculation in each node and assign more items to first n-1 process by default
# currently for 4 processor and 10 rows -> 2, 2, 2, 4
# it should be preferably 3, 3, 3, 1
#intervals = [
#    (
#        i * interval_size + int(bool(0)),
#        number_lines if i == size - 1 else (i + 1) * interval_size
#    ) for i in range(size)]

#spread leftovers more evenly
interval_size = number_lines // size
remainder = number_lines % size

intervals = []
start = 0
for i in range(size):
    extra = 1 if i < remainder else 0
    end = start + interval_size + extra
    intervals.append((start, end))
    start = end


if rank == 0:
    interval_lines = [lines[start:end] for start, end in intervals]
    # for start, end in intervals:
    #     print('start', start)
    #     print('end', end)
    #     interval_lines.append(lines[start:end])

#node_lines = comm.scatter(interval_lines, root=0)
if rank == 0:
    scatter_data = interval_lines
else:
    scatter_data = None

node_lines = comm.scatter(scatter_data, root=0)


# Executing for each node
print('Rank ', rank, ' has ', len(node_lines), 'elems')

# have to use json

#language_regex = r'("language")\s*(:)(\s*)(("([^"]*)")|\[.*\])(\s*),(\s*)'
#string_regex = r'"([^"]*)"'


counter = Counter()
for idx, node_line in enumerate(node_lines):
    try:
        post = json.loads(node_line)
    except json.JSONDecodeError:
        # Skip bad JSON lines safely
        continue

    # Check both possible field names
    lang_value = None

    # Mastodon / possible top-level fields
    if "language" in post:
        lang_value = post["language"]
    elif "lang" in post:
        lang_value = post["lang"]
    elif "langs" in post:
        lang_value = post["langs"]

    # BlueSky nested fields
    elif "record" in post and isinstance(post["record"], dict):
        record = post["record"]
        if "language" in record:
            lang_value = record["language"]
        elif "lang" in record:
            lang_value = record["lang"]
        elif "langs" in record:
            lang_value = record["langs"]
    # Skip missing or null values
    if not lang_value:
        continue
    # Case 1: single language string
    if isinstance(lang_value, str):
        lang_value = lang_value.strip()
        if lang_value:
            counter.update([lang_value])

    # Case 2: list of languages
    elif isinstance(lang_value, list):
        valid_langs = []
        for item in lang_value:
            if isinstance(item, str):
                item = item.strip()
                if item:
                    valid_langs.append(item)
        counter.update(valid_langs)

    # Any other format is ignored safely
all_counters = comm.gather(counter, root=0)

#for idx, node_line in enumerate(node_lines):
#    match_result = re.search(language_regex, node_line)
#    if match_result:
#        value = match_result.group(4)
#        print('value', value)
#        if value:
#            string_value = re.search(string_regex, value)
#            print('string_value', string_value.group(1))
#            counter.update([string_value.group(1)])


#all_counters = comm.gather(counter, root=0)
if rank == 0:
    print('all_counters', all_counters)
    
if rank == 0:
    global_counter = Counter()
    for iter_counter in all_counters:
        global_counter.update(iter_counter)
    print('ANSWER')
    most_common_lang = global_counter.most_common(10)
    print('Language Used', 'Frequency of occurence (#posts)')
    for i in most_common_lang:
        print('{}, {}'.format(i[0], i[1]))
    print('end')
