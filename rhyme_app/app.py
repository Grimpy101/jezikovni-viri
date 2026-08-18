import csv
import dataclasses

import flask

import icu
collator = icu.Collator.createInstance()  # pyright: ignore


@dataclasses.dataclass
class Entry:
    lemma: str
    pos: str
    word: str
    ending: str


app = flask.Flask("rime")

all_rhymes: dict[str, list[Entry]] = {}
pos_set: set[str] = set()
with open("rime_tabela.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    _ = next(reader)    # Skip header
    for row in reader:
        lemma = row[0]
        pos = row[1]
        word = row[2]
        ending = row[3]

        entry = Entry(lemma, pos, word, ending)
        if ending in all_rhymes:
            all_rhymes[ending].append(entry)
        else:
            all_rhymes[ending] = [entry]
        
        pos_set.add(pos)

pos_list = list(pos_set)
pos_list.sort(key=lambda i: collator.getSortKey(i[0]))


@app.route("/")
def index():
    ending = flask.request.args.get('search')
    filter_pos = flask.request.args.get('filterpos')

    if ending is not None and ending in all_rhymes:
        rhymes = all_rhymes[ending]
    else:
        rhymes = []
    
    if filter_pos:
        rhymes = list(filter(lambda el: el.pos == filter_pos, rhymes))
    
    rhymes.sort(key=lambda i: collator.getSortKey(i.word[0]))
    
    payload = {
        'rhymes': rhymes,
        'pos_list': pos_list
    }
    return flask.render_template("index.html", **payload)