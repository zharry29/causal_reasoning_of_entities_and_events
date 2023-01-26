import json
import sys
from sklearn.metrics import f1_score, accuracy_score

outfile = sys.argv[1]

with open(outfile) as f:
    jobj = json.load(f)

y_true = []
y_pred = []

for i, a in jobj.items():
    events = []
    for b in a['steps'][1:]:
        for c in b:
            if c["type"] == "multihop" and c["event"] not in events:
                events.append(c["event"])
    for b in a['steps'][1:]:
        for event in events:
            gold_change = 0
            pred_change = 0
            for c in b:
                if c["type"] == "multihop" and c["event"] == event:
                    gold_change = 1 if c["change"] == "less likely" else 2
                if c["type"] == "predicted_event" and c["event"] == event:
                    pred_change = 1 if c["change"] == "less likely" else 2
            y_true.append(gold_change)
            y_pred.append(pred_change)

f1 = f1_score(y_true, y_pred, average='macro')
print(y_true)
print(y_pred)
print(f'Acc: {accuracy_score(y_pred, y_true)}')
print(f"F1: {f1}")