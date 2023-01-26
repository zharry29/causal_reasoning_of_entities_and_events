#%%
import json
import numpy as np
from sklearn.metrics import f1_score, accuracy_score

#%%
with open('../../codex/v1.2/data_dev_out_entity_and_event_atonce.json', 'r') as f:
    data = json.load(f)
f.close()

step_len = []
for key, val in data.items():
    steps = val['steps']
    for step_lst in steps[1:]:
        step_len.append(len(step_lst[0]['step'].split()))

# average step length = 7
print(avg_len := np.mean(step_len))

y_true_long, y_pred_long, y_true_short, y_pred_short = [], [], [], []
for i, a in data.items():
    events = []
    for b in a['steps'][1:]:
        for c in b:
            if c["type"] == "event" and c["event"] not in events:
                events.append(c["event"])
    for b in a['steps'][1:]:
        cur_len = len(b[0]['step'].split())
        for event in events:
            gold_change = 0
            pred_change = 0
            for c in b:
                if c["type"] == "event" and c["event"] == event:
                    gold_change = 1 if c["change"] == "less likely" else 2
                if c["type"] == "predicted_event" and c["event"] == event:
                    pred_change = 1 if c["change"] == "less likely" else 2
        
            if cur_len > avg_len:
                y_true_long.append(gold_change)
                y_pred_long.append(pred_change)
            else:
                y_true_short.append(gold_change)
                y_pred_short.append(pred_change)

assert len(y_true_long) == len(y_pred_long)
assert len(y_true_short) == len(y_pred_short)

# %%
print(f1_score(y_true_long, y_pred_long, average='macro'))
print(accuracy_score(y_true_long, y_pred_long))
# %%
print(f1_score(y_true_short, y_pred_short, average='macro'))
print(accuracy_score(y_true_short, y_pred_short))

# %%
