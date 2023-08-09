from collections import defaultdict
import dataclasses
import re
import secrets
import sys

from pyrage import passphrase

def get_word_list():
  with open('USACONST.TXT', encoding='ISO8859') as f:
    text = f.read()
  return list(set(re.sub('[^a-z]', ' ', text.lower()).split()))


def load_graph(graph_str):
    lines = graph_str.strip().split('\n')
    nodes = {}
    edges = []

    for line in lines:
        line = line.strip()

        if line.startswith('digraph'):
            continue

        if line.startswith('}'):
            break

        if line.endswith('];'):
            node_id, label = line.split('[label=')
            node_id = node_id.strip()
            label = label.strip('];')
            nodes[node_id] = label
        else:
            src, dest = line.split('->')
            edges.append((src.strip(), dest.replace(';','',).strip()))

    return nodes, edges

with open('actualgraph.dot', 'r') as f:
    node_map, edges = load_graph(f.read())

print(node_map)
print(edges)


G = defaultdict(set)
Gv = defaultdict(set)
for src, dst in edges:
    G[node_map[src]].add(node_map[dst])
    Gv[src].add(dst)

D = get_word_list()

candidate = []
for word in D:
    if word[0] not in G:
        continue
    
    suc = True
    cur_s = G[word[0]]
    for c in word[1:]:
        if c not in cur_s:
            suc = False
            break
        cur_s = G[c]
    if suc:
        candidate.append(word)
        
candidate.sort()
print(candidate)

candidate_set = set(candidate)
TARGET_LEN = len(node_map)
print(f"TARGET PASSWORD HAS {len(node_map)} CHARACTERS")
pass_values = list(node_map.values())


from trie import Trie
t = Trie()
t.build_trie(candidate)

from collections import Counter
pass_values_cnt = Counter(pass_values)

print(pass_values_cnt)

prob_start_end = sorted(Gv.keys(), key=lambda key: -len(Gv[key]))
print([(node_map[x], len(Gv[x])) for x in prob_start_end])

START_CHARS = set(c[0] for c in candidate)


from collections import deque

for pos_start_node in Gv:
    print(f"STARTING AT {pos_start_node}: CHAR: {node_map[pos_start_node]}")
    start, start_id = node_map[pos_start_node], pos_start_node

    if len(t.auto_complete(start)) == 0:
        print(f"CHAR IS NOT POSSIBLE START")
        continue

    queue = deque()
    queue.append((start_id, start, [], set()))
    while queue:
        c_id, cur_str, existing_words, visited = queue.popleft()
        print(f"NOW CHECKING {cur_str}...")
        visited.add(c_id)
        pos_continuations = t.auto_complete(cur_str)
        print(pos_continuations)
        for pos in pos_continuations:
            if cur_str == pos:
                    tmp_existing_words = existing_words[::]
                    tmp_existing_words.append(cur_str)
                    print(f"{cur_str} IS A WORD IN THE DICTIONARY")
                    print(f"WORDLIST: {tmp_existing_words}, LEN={len(''.join(tmp_existing_words))}")
                    if len(''.join(tmp_existing_words)) > TARGET_LEN:
                        pass
                    elif len(''.join(tmp_existing_words)) == TARGET_LEN:
                        print(f"[+] POSSIBLE WORD: {''.join(tmp_existing_words)}") 
                    else:
                        # if there is a finishing path, then add new starting paths that havent been visit
                        for neighbor in Gv[c_id]:
                            if neighbor not in visited and node_map[neighbor] in START_CHARS:
                                queue.append((neighbor, node_map[neighbor], tmp_existing_words, visited.copy()))
    

        suffixes = [x[len(cur_str):] for x in pos_continuations]
        suffixes = [x for x in suffixes if x != '']
        for neighbor in Gv[c_id]:
            if neighbor not in visited and any(q[0] == node_map[neighbor] for q in suffixes):
                queue.append((neighbor, cur_str + node_map[neighbor], existing_words[::], visited.copy()))
        

        
   


    


