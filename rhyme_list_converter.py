import csv
import re
import icu

regex = re.compile(r"(?P<word>[\w ]*)(\((?P<lemma>[\w ]*)\))?, (?P<pos>[\w ]*)")


with open("rime.txt", "r") as f:
    content = f.read()


words: dict[tuple[str, str], set[tuple[str, str]]] = {}

suffix = ""
for line in content.split('\n'):
    line = line.strip()
    if len(line) == 0:
        continue
    
    if line.startswith("#"):
        suffix = line.replace("#", "").strip()
        continue

    res = re.match(regex, line)
    if res is not None:
        word = res.group('word')
        lemma = res.group('lemma')
        pos = res.group('pos')

        if word:
            word = word.strip()
        if lemma:
            lemma = lemma.strip()
        if pos:
            pos = pos.strip()

        if not lemma:
            lemma = word

        key = (lemma, pos)
        val = (word, suffix)
        if key in words:
            words[key].add(val)
        else:
            words[key] = set([val])


table = []
for key, val in words.items():
    for v in val:
        row = (key[0], key[1], v[0], v[1])
        table.append(row)

collator = icu.Collator.createInstance()
table.sort(key=lambda i: collator.getSortKey(i[0]))

with open("rime_tabela.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(('Lemma', 'POS', 'Word', 'RhymeGroup'))
    for row in table:
        writer.writerow(row)

