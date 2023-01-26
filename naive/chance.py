import json
import random
random.seed(29)
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--split', type=str, default='dev', help='Either dev or test set.')

args = parser.parse_args()

with open(f'../data_{args.split}_v2.json') as f:
    jobj = json.load(f)
    jout = jobj.copy()

for id,v in jobj.items():
    goal = v['goal']
    events = []
    for i,w in enumerate(v['steps']):
        if i == 0:
            continue
        for u in w:
            if u["type"] == "event":
                if u["event"] not in events:
                    events.append(u["event"])
    for i,w in enumerate(v['steps']):
        if i == 0:
            continue
        for event in events:
            label = random.choice(["more likely", "less likely", ""])
            if label:
                jout[id]['steps'][i].append({
                "type": "predicted_event",
                "event": event,
                "change": label
            })

outfile = f'data_{args.split}_out_chance.json'
with open(outfile,'w') as fw:
    json.dump(jout, fw, indent=4)