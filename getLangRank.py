import sys
import json
from collections import Counter
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size() 

start_time = MPI.Wtime()


#check command-line argument
if len(sys.argv) < 2 or not sys.argv[1].strip():
    if rank == 0:
        print("Usage: python3 getLangRank.py <file_path>")
    sys.exit(1)

file_path = sys.argv[1]

lines = None
number_lines = 0

 # rank 0 reads the whole file
if rank == 0: 
    try:
        with open(file_path, "r", encoding="utf-8") as file_content: 
            lines = file_content.readlines()
            number_lines = len(lines)
    except FileNotFoundError:
        print(f"Error: file not found: {file_path}")
        number_lines = -1
    except Exception as e:
        print(f"Error opening file {e}")
        number_lines = -1

#Brodcats number of lines
number_lines = comm.bcast(number_lines, root=0)

if number_lines == -1: 
    sys.exit(1)

#Split lines evenly across processes
interval_size = number_lines // size
remainder = number_lines % size

intervals = []
start = 0
for i in range(size): 
    extra = 1 if i < remainder else 0
    end = start + interval_size + extra
    intervals.append((start, end))
    start = end

#prepare chunks on ranks 0
if  rank == 0: 
    scatter_data = [lines[start:end] for start, end in intervals]

else: 
    scatter_data = None

#scatter line chunks
node_lines =  comm.scatter(scatter_data, root=0)

# Local counting
counter = Counter()

for node_line in node_lines:
    try:
        post = json.loads(node_line)
    except json.JSONDecodeError:
        # Skip bad JSON lines safely
        continue
    # Check both possible field names
    lang_value = None

    # Top-level fields 
    for key in ["language", "lang", "langs"]:
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
            for key in ["language", "lang", "langs"]: 
                if key in record:
                    lang_value = record[key]
                    break
    
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

#Gather all counters at rank 0
all_counters = comm.gather(counter, root=0)

#synchronize all ranks
comm.Barrier()
end_time = MPI.Wtime()

if rank == 0:
    global_counter = Counter()
    for iter_counter in all_counters:
        global_counter.update(iter_counter)

    most_common_lang = global_counter.most_common()
    print("Language Used, Frequency of occurrence (#posts)")
    for lang, count in most_common_lang:
        print(f"{lang}, {count}")
    
    print(f"Execution time: {end_time - start_time:.6f} seconds")
    
    
    
