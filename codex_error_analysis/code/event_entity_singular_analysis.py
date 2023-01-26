#%% 
import json 
from sklearn.metrics import f1_score, accuracy_score


#%%
with open('/Users/seacow/Documents/GitHub/procedural-qa/v2/codex/v1.2/data_dev_out_entity_and_event_atonce.json', 'r') as f:
    pred_data = json.load(f)
f.close()

with open('/Users/seacow/Documents/GitHub/procedural-qa/v2/codex_error_analysis/data/data_dev_v2_eoi.json', 'r') as f:
    eoi_data = json.load(f)
f.close()

#%%
y_true_single, y_pred_single, y_true_multi, y_pred_multi = [], [] ,[],[]
y_true_eoi_yes, y_pred_eoi_yes, y_true_eoi_no, y_pred_eoi_no = [], [], [], []
for pred_entry, eoi_entry in zip(pred_data.values(), eoi_data.values()):
    events = []
    for b in eoi_entry['steps'][1:]:
        for c in b:
            if c["type"] == "event" and c["event"] not in [t[0] for t in events]:
                events.append((c["event"], c['Singular'], c['EOI']))

    for b in pred_entry['steps'][1:]:
        for event in events:
            gold_change = 0
            pred_change = 0
            for c in b:
                if c["type"] == "event" and c["event"] == event[0]:
                    gold_change = 1 if c["change"] == "less likely" else 2
                if c["type"] == "predicted_event" and c["event"] == event[0]:
                    pred_change = 1 if c["change"] == "less likely" else 2
                
                if event[1] == 'True':
                    y_true_single.append(gold_change)
                    y_pred_single.append(pred_change)
                else:
                    y_true_multi.append(gold_change)
                    y_pred_multi.append(pred_change)
                    
                if event[2] == 'True':
                    y_true_eoi_yes.append(gold_change)
                    y_pred_eoi_yes.append(pred_change)
                else:
                    y_true_eoi_no.append(gold_change)
                    y_pred_eoi_no.append(pred_change)

assert len(y_true_single) == len(y_pred_single)
assert len(y_true_eoi_yes) == len(y_pred_eoi_yes)

#%%
print('Result for event answerable with current event')
print(f1_score(y_true_single, y_pred_single, average='macro'))
print(accuracy_score(y_true_single, y_pred_single))
print(' ')
print('Result for event NOT answerable with current event')
print(f1_score(y_true_multi, y_pred_multi, average='macro'))
print(accuracy_score(y_true_multi, y_pred_multi))

# %%
print('Result for event where related entity is mentioned in the step')
print(f1_score(y_true_eoi_yes, y_pred_eoi_yes, average='macro'))
print(accuracy_score(y_true_eoi_yes, y_pred_eoi_yes))
print(' ')
print('Result for event where related entity is NOT mentioned in the step')
print(f1_score(y_true_eoi_no, y_pred_eoi_no, average='macro'))
print(accuracy_score(y_true_eoi_no, y_pred_eoi_no))

# %%
print(sum([i for i in y_true_single if i != 0]))
print(sum([i for i in y_true_multi if i != 0]))
print(sum([i for i in y_true_eoi_yes if i != 0]))
print(sum([i for i in y_true_eoi_no if i != 0]))
# %%
