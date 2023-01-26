#%% 
import json 

with open('/Users/seacow/Documents/GitHub/procedural-qa/v2/openpi/weiqiu1.0/0hop-pred-test.json', 'r') as f:
    openpi_data = json.load(f)
f.close()
# %%
for key, val in openpi_data.items():
    if key != '1':
        break 
    steps = val['steps']
    for i, step_lst in enumerate(steps):
        visited_entity_state = []
        delete_idx = []
        for j, step_d in enumerate(step_lst):
            if step_d.get('type') == 'openpi_entity':
                cur_entity = step_d['entity']
                if (cur_entity_lst := cur_entity.split())[0].lower() in ['the', 'a']:
                    cur_entity = ' '.join(cur_entity_lst[1:])
                cur_attribute = step_d['attribute']
                cur_combo = tuple((cur_entity, cur_attribute))
                if cur_combo in visited_entity_state:
                    delete_idx.append(j)
                else:
                    visited_entity_state.append(cur_combo)
        step_lst = [x for (i, x) in enumerate(step_lst) if i not in delete_idx]
        openpi_data[key]['steps'][i] = step_lst
# %%
with open('/Users/seacow/Documents/GitHub/procedural-qa/v2/openpi/0hop-test-unique.json', 'w') as f:
    json.dump(openpi_data, f, indent=4)
f.close()


# %%
