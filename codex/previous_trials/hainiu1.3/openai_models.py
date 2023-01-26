#%%jjjjjjj
from copy import deepcopy
import openai
import json
import time
from tqdm import tqdm
import argparse

#openai.api_key = "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" # Harry
#openai.api_key = "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" # Shuyan
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

def parse_codex_prediction(gen_code):
    print(gen_code)
    step_changes = []
    current_step_changes = []
    initial = True
    for line in gen_code.split('\n'):
        line = line.strip()
        if line.startswith('def '):
            if not initial:
                step_changes.append(current_step_changes) 
                current_step_changes = []
            initial = False
        elif line.startswith('self.') and not line.startswith('self.event'):
            if ' = False' in line:
                change = "less likely"
            elif ' = True' in line:
                change = "more likely"
            else:
                continue
            current_step_changes.append((line.split('.')[1], line.split('.')[2].split(' = ')[0], line.split(' = ')[1].strip('"')))
        elif line.startswith('self.event'):
            if '.change = "less likely"' in line:
                change = "less likely"
            elif '.change = "more likely"' in line:
                change = "more likely"
            elif '.change = "equally likely"' in line:
                continue
            else:
                print(line)
                raise ValueError()
            current_step_changes.append((line[5:10], change))
        elif not line:
            break
    step_changes.append(current_step_changes) 
    #print(step_changes)
    return step_changes

def entity_and_event(goal, steps, events):
    prompt = open("prompts/1hop_0hop.py").read()
    event_dict = {e: None for e in events}
    for event in events:
        cur_prompt = deepcopy(prompt)
        prompt_addition = "\nclass " + text_to_code(goal, capitalize=True) + ":\n"
        prompt_addition += "  # Init\n"
        prompt_addition += '\n'.join([f"  # {s}" for s in steps]) + '\n'
        prompt_addition += '  def __init__(self, event):\n'
        #prompt += ', '.join(entities) + ', '
        cur_prompt += prompt_addition
        res = codex_init(cur_prompt)
        cur_prompt += res + '\n'
        cur_prompt += f'    self.event = event # {event}\n'
        
        prediction = ""
        for step in steps:
            step_def = f"  def {text_to_code(step,lower=True)}(self):\n"
            cur_prompt += step_def
            #print(cur_prompt)
            #raise SystemExit()
            prediction += step_def
            step_prediction = codex(cur_prompt).split('  def')[0]
            #print(step_prediction)
            prediction += step_prediction
            cur_prompt += step_prediction
        event_dict[event] = parse_codex_prediction(prediction)
    return event_dict

def codex_init(prompt):
    while True:
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
                stop=["\n"]
            )
            break
        except openai.error.RateLimitError as e:
            #print(e)
            #print("Retrying in 10 seconds")
            time.sleep(10)

    gen_code = ret["choices"][0]["text"]#.strip().split('\n')[0]

    return gen_code
    
def codex(prompt):
    while True:
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
                stop=["\n\n"]
            )
            break
        except openai.error.RateLimitError as e:
            #print(e)
            #print("Retrying in 10 seconds")
            time.sleep(10)

    gen_code = ret["choices"][0]["text"]#.strip().split('\n')[0]

    return gen_code

#%%
with open('../../data_dev_v2.json') as f:
    jobj = json.load(f)
    jout = jobj.copy()

all_gold_changes = []
all_pred_changes = []

for id,v in tqdm(jobj.items()):
    goal = v['goal']
    steps = []
    events = []
    entities = []
    gold_event_changes = []
    gold_entity_changes = []
    for i,w in enumerate(v['steps']):
        if i == 0:
            continue
        current_event_changes = []
        current_entity_changes = []
        for u in w:
            if u["type"] == "event":
                if u["event"] not in events:
                    events.append(u["event"])
                event_index = events.index(u["event"])
                current_event_changes.append((f"event{event_index}", u["change"].split()[0]))
            if u["type"] == "entity":
                if u["entity"] not in entities:
                    entities.append(u["entity"])  
                current_entity_changes.append(u)
            if u["type"] == "step":
                steps.append(u["step"])
        gold_event_changes.append(current_event_changes)
        gold_entity_changes.append(current_entity_changes)

    #print(gold_event_changes)
    pred_changes = entity_and_event(goal, steps, events)
    #print(pred_changes)
    for i,(event, pred_lst) in enumerate(pred_changes.items()):
        for y in pred_lst:
            if len(y) == 2:
                jout[id]["steps"][i+1].append({
                                "type": "predicted_event",
                                "event": event,
                                "change": y[1]
                            })
            if len(y) == 3:
                jout[id]["steps"][i+1].append({
                                "type": "predicted_entity",
                                "entity": y[0],
                                "attribute": y[1],
                                "change": y[2]
                            })
    #print(len(gold_event_changes))
    #print(len(pred_changes))
    #assert(len(gold_event_changes) == len(pred_changes))
    if(len(gold_event_changes) < len(pred_changes)):
        print("Pred changes are more than gold, truncating.")
        pred_changes = pred_changes[:len(gold_event_changes)]
    #break

outfile = f'data_dev_out_entity_and_event.json'
with open(outfile,'w') as fw:
    json.dump(jout, fw, indent=4)
# %%
