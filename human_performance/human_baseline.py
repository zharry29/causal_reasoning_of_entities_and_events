#%%
import json

with open('/Users/seacow/School/UPenn/Research/Procedural Reasoning/v2/data/data_dev_v2.json', 'r') as f:
    data = json.load(f)
f.close()
# %%
for dict in data.values():
    steps = dict['steps']
    all_events = []
    for step in steps:
        for lst in step:
            if 'event' in lst.keys():
                lst['type'] = 'event'
                if lst['event'] not in all_events:
                    all_events.append(lst['event'])
    
    for step in steps:
        for event in all_events:
            event_dict = {'type': 'predicted_event', 'event': event, 'change': ''}
            step.append(event_dict)
# %%
with open('dev_data_human_labeled.json', 'w') as f:
    json.dump(data, f, indent=4)
f.close()
# %%
all_events
# %%
