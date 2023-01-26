#%%
import json 
from sklearn.metrics import f1_score, confusion_matrix, ConfusionMatrixDisplay

#%%
with open('/Users/seacow/Documents/GitHub/procedural-qa/v2/codex_error_analysis/data/data_dev_entity_event_inference_labeled_hainiu.json', 'r') as f:
    data = json.load(f)
f.close()

total_entail, total_contradict = 0, 0
y_true_entail, y_pred_entail, y_true_contradict, y_pred_contradict = [], [], [], []
for val in data.values():
    steps = val['steps']
    for step_lst in steps:
        cur_types = [e.get('type') for e in step_lst]
        if 'predicted_event' in cur_types and 'predicted_entity' in cur_types:
            pred_event_idx = [i for (i, x) in enumerate(cur_types) if x == 'predicted_event']
            event_idx = [i for (i, x) in enumerate(cur_types) if x == 'event']
            for idx in pred_event_idx:
                cur_pred = step_lst[idx]
                cur_pred_event = cur_pred['event']
                cur_relation = cur_pred['event_entity_inference'][-1]

                # get gold label
                gold_label = 0
                if event_idx:
                    for idx in event_idx:
                        if (cur_event := step_lst[idx])['event'] == cur_pred_event:
                            gold_label = 1 if cur_event['change'] == 'less likely' else 2
                
                cur_pred_label = 1 if cur_pred['change'] == 'less likely' else 2

                if cur_relation == 'entailment':
                    y_true_entail.append(gold_label)
                    y_pred_entail.append(cur_pred_label)
                    total_entail += 1
                elif cur_relation == 'contradiction':
                    y_true_contradict.append(gold_label)
                    y_pred_contradict.append(cur_pred_label)
                    total_contradict += 1
                    
                
# %%
print(f1_score(y_true_entail, y_pred_entail, average = 'macro'))
conf_mtx = confusion_matrix(y_true_entail, y_pred_entail)
ConfusionMatrixDisplay(conf_mtx, display_labels= ['equally', 'less', 'more']).plot()
# %%
print(f1_score(y_true_contradict, y_pred_contradict, average = 'macro'))
conf_mtx = confusion_matrix(y_true_contradict, y_pred_contradict)
ConfusionMatrixDisplay(conf_mtx, display_labels= ['equally', 'less', 'more']).plot()

# %%
print(total_entail)
print(total_contradict)
print(total_entail + total_contradict)

# %%
