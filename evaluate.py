"""
Usage: python evaluate.py PATH_TO_OUTPUT_FILE
Calculates the macro F1 among 3 classes: more, less, equally likely
"""

import os
import json
import sys
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score, confusion_matrix, ConfusionMatrixDisplay

outfile = sys.argv[1]

with open(outfile) as f:
    jobj = json.load(f)

y_true = []
y_pred = []

for i, a in jobj.items():
    events = []
    #proc_y_true = []
    #proc_y_pred = []
    for b in a['steps'][1:]:
        for c in b:
            if c["type"] == "event" and c["event"] not in events:
                events.append(c["event"])
    for b in a['steps'][1:]:
        for event in events:
            gold_change = 0
            pred_change = 0
            gold_entity = []
            pred_entity = []
            for i,c in enumerate(b):
                if c["type"] == "event" and c["event"] == event:
                    gold_change = 1 if c["change"] == "less likely" else 2
                    for j in range(i-1, 0, -1):
                        if b[j]["type"] == "entity":
                            gold_entity.append((b[j]["entity"], b[j]["attribute"], b[j]["change"]))
                        else:
                            break
                if c["type"] == "predicted_event" and c["event"] == event:
                    pred_change = 1 if c["change"] == "less likely" else 2
                    for j in range(i-1, 0, -1):
                        if b[j]["type"] == "predicted_entity":
                            pred_entity.append((b[j]["entity"], b[j]["attribute"], b[j]["change"]))
                        else:
                            break
            #proc_y_true.append(gold_change)
            #proc_y_pred.append(pred_change)
            #print(c)
            print(a["goal"], b[0]["step"], event, gold_change, gold_entity, pred_change, pred_entity, sep='\t')
            y_true.append(gold_change)
            y_pred.append(pred_change)
    

f1_overall = f1_score(y_true, y_pred, average='macro')
f1_sep = f1_score(y_true, y_pred, average=None)
#print(y_true)
#print(y_pred)
print("0: Equally Likely, 1: Less Likely, 2: More Likely")
print(f"F1 Scores: {f1_sep}\n")
print(f"Overall F1 Score: {f1_overall}")

conf_mtx = confusion_matrix(y_true, y_pred)
ConfusionMatrixDisplay(conf_mtx, display_labels = ['equally', 'less', 'more']).plot()
outpath = '/'.join((outfile_lst := outfile.split('/'))[:-1])
outname = outfile_lst[-1].split('.')[0] + '_confusion_matrix.png'
plt.savefig(os.path.join(outpath, outname))

