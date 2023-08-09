# **NPC**

## **Description**
A friend handed me this map and told me that it will lead me to the flag. 
It is confusing me and I don't know how to read it, can you help me out?


## **Solution**
We are given a file `encrypt.py` as well as `hint.dot`, `secret.age`, and `USACONST.TXT`. 

The encryption is the following:
```py
def encrypt(num_words, secret):
  password = generate_password(num_words)
  hint = generate_hint(password)
  with open('hint.dot', 'w') as hint_file:
    write_hint(hint, hint_file)
  filename = 'secret.age'
  with open(filename, 'wb') as f:
    f.write(passphrase.encrypt(secret, password))
  print(f'Your secret is now inside password-protected file {filename}.')
  print(f'Use the password {password} to access it.')
  print(
      'In case you forgot the password, maybe hint.dot will help your memory.')


if __name__ == '__main__':
  encrypt(num_words=int(sys.argv[1]), secret=sys.argv[2].encode('utf-8'))
```

The user specifies a word length in `sys.argv[1]` and a secret(FLAG assumed) in `sys.argv[2]`. It then will generate a password, generate a hint, and print the encrypted password, as well as the hint.

Lets look at the `generate_password` first:
```
def get_word_list():
  with open('USACONST.TXT', encoding='ISO8859') as f:
    text = f.read()
  return list(set(re.sub('[^a-z]', ' ', text.lower()).split()))


def generate_password(num_words):
  word_list = get_word_list()
  return ''.join(secrets.choice(word_list) for _ in range(num_words))
```
So we know now that the password will just be a series of random words in `USACONST.TXT` concatenated with each other. We can use the `get_word_list()` ourselves to see these words, so thats no problem at all.

Now lets look at the hint generation:
```py
def generate_hint(password):
  random = secrets.SystemRandom()
  id_gen = IdGen()
  graph = Graph([],[])
  for letter in password:
    graph.nodes.append(Node(letter, id_gen.generate_id()))
  for a, b in zip(graph.nodes, graph.nodes[1:]):
    graph.edges.append(Edge(a, b))
  for _ in range(int(len(password)**1.3)):
    a, b = random.sample(graph.nodes, 2)
    graph.edges.append(Edge(a, b))
  random.shuffle(graph.nodes)
  random.shuffle(graph.edges)
  for edge in graph.edges:
    if random.random() % 2:
      edge.a, edge.b = edge.b, edge.a
  return graph
```

Interesting, so the hint is a graph. It first creates edges from each character of the password to the next, it then creates a bunch of random edges to obfuscate the graph. Finally it *seems* does some random swapping of the edges. *Why seems? we shall see later on!*

Looking closer at the hint:
```
graph {
    1051081353 [label=a];
    66849241 [label=a];
    53342583 [label=n];
    213493562 [label=d];
    4385267 [label=i];
    261138725 [label=o];
    51574206 [label=t];
    565468867 [label=e];
    647082638 [label=r];
    177014844 [label=d];
    894978618 [label=e];
    948544779 [label=n];
    572570465 [label=n];
    582531406 [label=r];
    264939475 [label=a];
    415170621 [label=s];
    532012257 [label=t];
    151901859 [label=v];
    346347468 [label=g];
    148496047 [label=g];
    125615053 [label=s];
    723039811 [label=e];
    962878065 [label=i];
    112993293 [label=w];
    748275487 [label=n];
    120330115 [label=s];
    76544105 [label=c];
    186790608 [label=h];
    53342583 -- 565468867;
    582531406 -- 76544105;
    125615053 -- 120330115;
    264939475 -- 572570465;
    53342583 -- 565468867;
    532012257 -- 264939475;
    346347468 -- 532012257;
    125615053 -- 582531406;
    177014844 -- 120330115;
    264939475 -- 962878065;
    647082638 -- 1051081353;
    346347468 -- 112993293;
    120330115 -- 151901859;
    647082638 -- 125615053;
    532012257 -- 66849241;
    582531406 -- 894978618;
    ...
}
```
Wow I mean it seem like quite a revealing hint. Already, we know the character count, and the exact characters that will be present in the final string. We can visualize this [graph](image.png) actually using `dot`. 

Now lets go back to that hint generation. One thing that stuck out was the edge swapping. 
```
random = secrets.SystemRandom()
for edge in graph.edges:
    if random.random() % 2:
      edge.a, edge.b = edge.b, edge.a
```
Doesn't random.random() return a float? I quickly tested this and yes indeed, this doesn't do the intended behavior.

```py
>>> import secrets
>>> random = secrets.SystemRandom()
>>> cnt = 0
>>> for _ in range(200):
...     if random.random() % 2:
...             cnt += 1
... 
>>> print(cnt)
200
```

So then if we think about this, what we were provided with was a undirected graph, however we actually have a *semi* known directional graph (where all the edges are reversed)! This will give us alot more information to try figure out the password. 

My final solution does the following:
1. Construct a graph `G`, with the nodes `node_map` and modified edges `edges`. I actually created two graphs for this, one that maps the node_ids, and one which only maps the characters (NOTE that this does not respect the multiplicities but its useful `(2)`)
    ```py
    G = defaultdict(set)
    Gv = defaultdict(set)
    for src, dst in edges:
        G[node_map[src]].add(node_map[dst])
        Gv[src].add(dst)
    ```

2. Eliminate any words from the dictionary D that cannot possibly be in the graph G. This can be done by trying to traverse each word in D. If a word cannot be travered in this modified graph, then it can't possibly be in the final dictionary.
    ```py
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

    candidate_set = set(candidate)
    ```


3. Build a `Trie` with the candidate words. This purely for time complexity optimizations. With using a Trie, it solves pretty fast so maybe this isn't necessary, but it does work.

    ```py
    # I used a simple Trie implementation from here: 
    # https://stackoverflow.com/questions/11015320/how-to-create-a-trie-in-python

    from trie import Trie
    t = Trie()
    t.build_trie(candidate)
    ```

4. Perform a BFS on the graph G for each possible starting character. This BFS is a bit more complicated as it also keeps track of visited independently in the Queue. It additionally only traverses to a neighbor if the neighbor will satisfy one of the auto_complete suffixes.
    ```py
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
        
    ```

Finally running this program:
```console
abhi@abhi-omen:~/GoogleCTF/NPC$ python3 actualgraph.py | grep "POSSIBLE WORD"
[+] POSSIBLE WORD: standardsignwatergivenchosen
[+] POSSIBLE WORD: standardwatersigngivenchosen
```

And perfect! 2 possible passwords. We now simply try to decrypt the `secret.age` file with both passwords.

```py
from pyrage import passphrase
poss = ["standardsignwatergivenchosen", "standardwatersigngivenchosen"]
with open('secret.age', 'rb') as f:
    encrypted = f.read()
    for p in poss:
        try:
            print(passphrase.decrypt(encrypted, p))
        except:
            pass

> CTF{S3vEn_bR1dg35_0f_K0eN1g5BeRg}
```

Quite a fun programming challenge!

## **Flag**: *CTF{S3vEn_bR1dg35_0f_K0eN1g5BeRg}*
---

