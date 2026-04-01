import sys
import json
import time
from collections import Counter
from mpi4py import MPI

start_time = time.time()
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size() 

print("hello from process", rank, "of", size)

#handle IndexError if no filename is passed
if len(sys.argv) < 2:
    if rank == 0:
        print("Usage: python3 getLangRank.py <file_path>")
    sys.exit(1)

file_path = sys.argv[1]

lines = []
number_lines = 0

if rank == 0:
    print('Rank 0 executing', file_path)
    with open(file_path) as file_content:
        lines = file_content.readlines()
        print('lines length', len(lines))
        number_lines = len(lines)

number_lines = comm.bcast(number_lines, root=0)

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
    scatter_data = interval_lines
else:
    scatter_data = None

node_lines = comm.scatter(scatter_data, root=0)


# Executing for each node
print('Rank ', rank, ' has ', len(node_lines), 'elems')

counter = Counter()
for idx, node_line in enumerate(node_lines):
    try:
        post = json.loads(node_line)
    except json.JSONDecodeError:
        # Skip bad JSON lines safely
        continue

    # Check both possible field names
    lang_value = None

    # Top-level first 
    for key in ["langauge", "lang", "langs"]:
        if key in post: 
            lang_value = post[key]
            break

    #Nested record (Mastodon)
    if lang_value is None and "doc" in post:
        doc = post["doc"]
        if isinstance(doc, dict):
            for key in ["language", "lang", "langs"]:
                if key in doc:
                    lang_value = doc[key]
                    break

    #Check nested reocrd (BlueSky)
    if lang_value is None and "record" in post: 
        record = post["record"]
        if isinstance(record, dict): 
            for key in ["langauge", "lang", "langs"]: 
                if key in record:
                    lang_value = record[key]
                    break

    
    if idx < 5: 
        print("POST KEYS:", post.keys())
        print("LANG VALUE:" , lang_value)


    # Skip missing or null values
    if lang_value is None:
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

end_time = time.time()

# Any other format is ignored safely
all_counters = comm.gather(counter, root=0)

#all_counters = comm.gather(counter, root=0)
if rank == 0:
    print('all_counters', all_counters)
    global_counter = Counter()
    for iter_counter in all_counters:
        global_counter.update(iter_counter)

    print('ANSWER')
    most_common_lang = global_counter.most_common(10)
    print('Language Used', 'Frequency of occurence (#posts)')
    for i in most_common_lang:
        print('{}, {}'.format(i[0], i[1]))
    print('end')
    
    print("Excution time: ", end_time - start_time)
    

