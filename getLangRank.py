import sys
import json
import time
import os
from collections import Counter
from mpi4py import MPI

start_time = time.time()
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size() 

#handle IndexError if no filename is passed
if len(sys.argv) < 2:
    if rank == 0:
        print("Usage: python3 getLangRank.py <file_path>")
    sys.exit(1)

file_path = sys.argv[1]

file_size = os.path.getsize(file_path)

# Each rank is responsible for a byte range of the file
start_byte = rank * file_size // size
end_byte = (rank + 1) * file_size // size

counter = Counter()
node_lines = []
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
        node_lines.append(line_bytes.decode('utf-8', errors='replace'))

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
        pass 
        # print("POST KEYS:", post.keys())
        # print("LANG VALUE:" , lang_value)


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
    # print('all_counters', all_counters)
    global_counter = Counter()
    for iter_counter in all_counters:
        global_counter.update(iter_counter)

    # print('ANSWER')
    most_common_lang = global_counter.most_common(10)
    print('Language Used, Frequency of occurence (#posts)')
    for i in most_common_lang:
        print('{}, {}'.format(i[0], i[1]))
    # print('end')
    
    # print("Excution time: ", end_time - start_time)
    
