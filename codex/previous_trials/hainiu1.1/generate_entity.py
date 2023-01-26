#%%
import re
import ast
import json 
import time
import openai
from tqdm import tqdm
from copy import deepcopy

openai.api_key_path = '/Users/seacow/School/UPenn/Research/Procedural Reasoning/api_keys/shuyan_api_key.txt'

def text_to_code(goal):
    return '_'.join([c.lower() for c in goal.split()])


def parse_entity(res):
    res_lst = res.split('\n')
    event_tuple = [re.search(r"\([\",\w\s]+\)", l).group().replace("'", "") for l in res_lst]
    event_dict = {f'event{i}': ast.literal_eval(l) for i, l in enumerate(event_tuple)}
    return event_dict


def codex(prompt):
    ret = openai.Completion.create(
        engine=f"code-davinci-002",
        prompt=prompt,
        temperature=0,  # 0.7
        max_tokens=1024,
        top_p=1,
        logprobs=5,
        frequency_penalty=0,
        presence_penalty=0,
        stop=['\n\n']
    )
    gen_code = ret["choices"][0]["text"]#.strip().split('\n')[0]

    return gen_code

#%%
with open('/Users/seacow/School/UPenn/Research/Procedural Reasoning/v2/data/data_dev_v2.json', 'r') as f:
    data = json.load(f)
f.close()

prompt = open('/Users/seacow/School/UPenn/Research/Procedural Reasoning/v2/predict_entity/prompt/entity_prompt.py').read()


for key, dict in tqdm(data.items()):
    steps = ["Init"]
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


    cur_prompt += f'def {text_to_code(goal)}():\n\tsteps = [\n'
    for step in steps:
        cur_prompt += f'\t"{step.capitalize()}",\n'
    cur_prompt += '\t]\n\n'

    for j, event in enumerate(events):
        cur_prompt += f'\tevent{j} = "{event.capitalize().replace(".", "")}"\n' 
    
    cur_prompt += '\tevent0.precondition ='
    
    ind = 1
    while ind:
        try:
            res = codex(cur_prompt)
            data[key]['entity_bank'] = parse_entity(res)
            ind = 0
        except openai.error.RateLimitError:
            time.sleep(5)
            pass
    
    

with open('data_dev_v2_entity.json', 'w') as f:
    json.dump(data, f, indent=4)
f.close()
# %%
# %%
