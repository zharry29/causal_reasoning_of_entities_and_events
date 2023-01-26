#%%
import os
import json
import numpy as np
from sklearn.metrics import f1_score, confusion_matrix, ConfusionMatrixDisplay


#%%
with open('/Users/seacow/Documents/GitHub/procedural-qa/v2/codex_error_analysis/data/data_dev_out_entity_labeled_hainiu.json', 'r') as f:
    data = json.load(f)
f.close()


# Analysis on Entity States
steps_no_entity = {}
pred_event, pred_entity = 0, 0
num_entities = []
num_true_entities = []
for val in data.values():
    goal = val['goal']
    steps = val['steps']

#    for step_lst in steps:
#        cur_keys = [d.get('type') for d in step_lst]
#        step_content.append(step_lst[0]['step'])
#        if 'event' in cur_keys:
#            if (cur_event := step_lst[cur_keys.index('event')]['event']) not in true_events:
#                true_events.append(cur_event)

    
    for step_lst in steps:
        cur_keys = [d.get('type') for d in step_lst]
        if 'predicted_event' in cur_keys and 'event' in cur_keys:

            event_idx = [i for i, x in enumerate(cur_keys) if x == 'predicted_event']
            true_event_idx = [i for i, x in enumerate(cur_keys) if x == 'event']
            true_entity_idx = [i for i, x in enumerate(cur_keys) if x == 'entity']

            num_event = cur_keys.count('predicted_event')
            num_pred_entity = cur_keys.count('predicted_entity')
            num_true_entity = cur_keys.count('entity')

            pred_event += num_event
            pred_entity += min(num_event, num_pred_entity)

            if 'predicted_entity' in cur_keys:
                num_entities.append(num_pred_entity)
            
            if 'entity' in cur_keys:
                num_true_entities.append(num_true_entity)

            if num_event > num_pred_entity:
                print(f"Goal: ({goal})")
                print(f"Current Step: ({step_lst[0]['step']})")
                events = '\n'.join([str((e['event'], e['change'])) for e in [step_lst[idx] for idx in event_idx]])
                true_events = '\n'.join([str((e['event'], e['change'])) for e in [step_lst[idx] for idx in true_event_idx]])
                true_entities = [step_lst[idx] for idx in true_entity_idx]
                true_entities = '\n'.join([str((e['entity'], e['attribute'], e['change'])) for e in true_entities])
                print(f"True Events:\n{true_events}")
                print(f"Predicted Events:\n{events}")
                print(f"True Entities:\n{true_entities}")
                if num_pred_entity != 0:
                    entity_idx = [i for i, x in enumerate(cur_keys) if x == 'predicted_entity']
                    entities = [step_lst[idx] for idx in entity_idx]
                    entity_states = '\n'.join([str((e['entity'], e['attribute'], e['change'])) for e in entities])
                    print(f"Predicted Entities:\n{entity_states}")
                print('\n\n')
                    
#            for step_d in step_lst:
#                if step_d['type'] == 'predicted_event':
#            pred_event += 1
#            if 'predicted_entity' in cur_keys:
#                pred_entity += 1

print(f"Percentage of events with entity: {pred_entity / pred_event:.2f}")
print(f"Average number of entity states predicted for key steps: {np.mean(num_entities):.2f}")
print(f"Average number of ground truth entity state for key steps: {np.mean(num_true_entities):.2f}")


# %%
# Analysis on Coverage Probability
num_events, num_true_events = [], []
for val in data.values():
    goal = val['goal']
    steps = val['steps']

    for step_lst in steps:
        cur_keys = [d.get('type') for d in step_lst]
        
        num_event = cur_keys.count('predicted_event')
        num_true_event = cur_keys.count('event')

        num_events.append(num_event)
        num_true_events.append(num_true_event)

numerator = sum([a != b for (a, b) in zip(num_events, num_true_events)])
denominator = len(num_events)
print(f"Converage Probability: {1 - numerator / denominator:.2f}")

num_events_bin = [1 if e > 0 else 0 for e in num_events]
num_true_events_bin = [1 if e > 0 else 0 for e in num_true_events]
numerator = sum([a != b for (a, b) in zip(num_events_bin, num_true_events_bin)])
denominator = len(num_events)
print(f"Binary converage Probability: {1 - numerator / denominator:.2f}")


# %%
# Analysis on correlation between event number and accuracy
y_true_single, y_pred_single, y_true_multi, y_pred_multi = [], [], [], []
for val in data.values():
    steps = val['steps']
    for step_lst in steps:
        cur_types = [e.get('type') for e in step_lst]
        event_count = cur_types.count('event')
        if event_count == 1:
            event_dict = step_lst[cur_types.index('event')]
            event = event_dict['event']

            change = 1 if event_dict['change'] == 'less likely' else 2
            y_true_single.append(change)

            pred_change = 0
            if 'predicted_event' in cur_types:
                pred_event_idx = [i for i, x in enumerate(cur_types) if x == 'predicted_event']
                for idx in pred_event_idx:
                    if (pred_event_dict := step_lst[idx])['event'] == event:
                        pred_change = 1 if pred_event_dict['change'] == 'less likely' else 2
            y_pred_single.append(pred_change)
        
        elif event_count > 1:
            event_idx = [i for i, x in enumerate(cur_types) if x == 'event']
            event_dicts = [step_lst[idx] for idx in event_idx]
            events = [d['event'] for d in event_dicts]

            for event_dict in event_dicts:
                change = 1 if event_dict['change'] == 'less likely' else 2
                y_true_multi.append(change)
                
                pred_change = 0
                if 'predicted_event' in cur_types:
                    pred_event_idx = [i for i, x in enumerate(cur_types) if x == 'predicted_event']
                    for idx in pred_event_idx:
                        if (pred_event_dict := step_lst[idx])['event'] in events:
                            pred_change = 1 if pred_event_dict['change'] == 'less likely' else 2
                y_pred_multi.append(pred_change)
                    

assert len(y_true_single) == len(y_pred_single)
assert len(y_true_multi) == len(y_pred_multi)



        

# %%

print(f"F1 Score for steps with single event: {f1_score(y_true_single, y_pred_single, average='macro'):.2f}")
print(f"F1 Score for steps with multiple events: {f1_score(y_true_multi, y_pred_multi, average='macro'):.2f}")


# %%
conf_mtx = confusion_matrix(y_true_multi, y_pred_multi)
ConfusionMatrixDisplay(conf_mtx, display_labels = ['equally', 'less', 'more']).plot()





# %%
# Comparions of prediction acc between event only VS pred entity-state
#c = 0
#y_true_entity, y_pred_entity = [], []
#y_true_no_entity, y_pred_no_entity = [], []
#for val in data.values():
#    steps = val['steps']
#    for step_lst in steps:
#        cur_types = [e.get('type') for e in step_lst]
#        if cur_types.count('event') == 1:
#            cur_event = step_lst[cur_types.index('event')]
#            content = cur_event['event']
#            true_ans = 1 if cur_event['change'] == 'less likely' else 2
#
#            ind = 0
#            if 'predicted_entity' in cur_types:
#                y_true_entity.append(true_ans)
#                ind = 1
#            else:
#                y_true_no_entity.append(true_ans)
#            
#            pred_ans = 0
#            if 'predicted_event' in cur_types:
#                cur_pred_event = step_lst[cur_types.index('predicted_event')]
#                pred_ans = 1 if cur_pred_event['change'] == 'less likely' else 2 
#            if ind:
#                y_pred_entity.append(pred_ans)
#            else:
#                y_pred_no_entity.append(pred_ans)
#                
#                
#print(f"F1 Score for steps with entity state prediction: {f1_score(y_true_entity, y_pred_entity, average='macro'):.2f}")
#print(f"F1 Score for steps without entity state prediction: {f1_score(y_true_no_entity, y_pred_no_entity, average='macro'):.2f}")
#
#
## %%
#conf_mtx = confusion_matrix(y_true_entity, y_pred_entity)
#ConfusionMatrixDisplay(conf_mtx, display_labels = ['equally', 'less', 'more']).plot()
#
## %%
#conf_mtx = confusion_matrix(y_true_no_entity, y_pred_no_entity)
#ConfusionMatrixDisplay(conf_mtx, display_labels = ['equally', 'less', 'more']).plot()
#
#
## %%
#