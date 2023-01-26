#%%
import re
import ast
import json 
import time
import openai
from tqdm import tqdm
from copy import deepcopy

openai.api_key_path = '/Users/seacow/School/UPenn/Research/Procedural Reasoning/api_keys/hainiu_api_key.txt'

def text_to_code(s, capitalize=False, lower=False):
    def strip_det(s):
        return s.removeprefix('a ').removeprefix('the ').removeprefix('my ').replace(' a ', ' ').replace(' the ', ' ').replace(' my ', ' ')
    s = s.replace('.','').replace(',','').replace('?','')
    if capitalize:
        return '_'.join([x.capitalize() for x in strip_det(s).split()])
    if lower:
        return '_'.join([x.lower() for x in strip_det(s).split()])
    return '_'.join(strip_det(s).split())

def codex(prompt):
    ind = 1
    while ind:
        try:
            ret = openai.Completion.create(
                engine=f"code-davinci-002",
                prompt=prompt,
                temperature=0,  # 0.7
                max_tokens=1024,
                top_p=1,
                logprobs=5,
                frequency_penalty=0,
                presence_penalty=0,
                stop=['\n']
            )
            ind = 0
            time.sleep(5)
        except:
            time.sleep(5)

    gen_code = ret["choices"][0]["text"]#.strip().split('\n')[0]

    return gen_code

#%%
with open('/Users/seacow/School/UPenn/Research/Procedural Reasoning/v2/data/data_dev_v2.json', 'r') as f:
    data = json.load(f)
f.close()

prompt = open('/Users/seacow/School/UPenn/Research/Procedural Reasoning/v2/predict_entity/hainiu1_1/prompt/entity_prompt.py').read()


for key, dict in tqdm(data.items()):
    steps = []
    events = []
    goal = dict['goal']
    for j, step in enumerate(dict['steps']):
        if j == 0:
            continue
        for entry in step:
            if 'step' in list(entry.keys()):
                steps.append(entry['step'])
            elif 'event' in list(entry.keys()):
                if (cur_event := entry['event']) not in events:
                    events.append(cur_event)

    cur_prompt = deepcopy(prompt)
    cur_prompt += f'class {text_to_code(goal)}():\n'

    cur_proc_entity_bank = {}

    for i, event in enumerate(events):
        event_entity_pred = []
        for j, step in enumerate(steps):
            cur_prompt += f'def {text_to_code(step)}():\n\t\tevent = {event.strip().capitalize()}\n\t\tevent.precondition ='
            pred = codex(cur_prompt)
            event_entity_pred.append(pred.strip())
            cur_prompt += f' {pred.strip()}\n'
        mode_pred = max(set(event_entity_pred), key=event_entity_pred.count)
        cur_proc_entity_bank[event] = mode_pred
    
    data[key]['entity_bank'] = cur_proc_entity_bank
            
        
    
#    ind = 1
#    while ind:
#        try:
#            res = codex(cur_prompt)
#            data[key]['entity_bank'] = parse_entity(res, events)
#            ind = 0
#        except openai.error.RateLimitError:
#            time.sleep(5)
#            pass
#    
#    
#%%
with open('data_dev_v2_entity.json', 'w') as f:
    json.dump(data, f, indent=4)
f.close()
#%%
print(cur_prompt)
# %%
# %%
