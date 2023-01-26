#%%
from copy import deepcopy
import openai
import json
import time
import argparse
from tqdm import tqdm

#openai.api_key = "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" # Harry
openai.api_key = "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" # Shuyan

#parser = argparse.ArgumentParser()
#parser.add_argument('--prompt', type=str, default='')
#parser.add_argument('--step_by_step', action='store_true')
#
#args = parser.parse_args()

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
            current_step_changes.append((line[5:11], change))
        elif not line:
            break
    step_changes.append(current_step_changes) 
    #print(step_changes)
    return step_changes

def entity_and_event(goal, steps, events, entity_bank):
    prompt = open("./prompt/1hop_0hop.py").read()
    prompt_addition = "class " + text_to_code(goal, capitalize=True) + ":\n"
    prompt_addition += "  # Init\n"
    prompt_addition += '\n'.join([f"  # {s}" for s in steps]) + '\n'
    prompt_addition += '  def init(self, '
    #prompt += ', '.join(entities) + ', '
    prompt_addition += ', '.join([f"event{i}" for i in range(len(events))]) + "):\n"

    entities = []
    for lst in entity_bank.values():
        entities.append(text_to_code(lst[0]))

    entity_visited = []
    for i, entity in enumerate(entities):
        if entity.lower() in entity_visited:
            continue 
        entity_visited.append(entity.lower())
        prompt_addition += f"    self.{text_to_code(entity)} = {text_to_code(entity, capitalize=True)}()\n"
    for i, event in enumerate(events):
        prompt_addition += f"    self.event{i} = event{i} # {event}\n"
    
    #print(prompt_addition)
    #raise SystemExit()
    prompt += prompt_addition
    prediction = ""
    pred_res = []

    for step in steps:
        pred_step = []
        step_def = f"  def {text_to_code(step,lower=True)}(self):\n"
        cur_prompt = deepcopy(prompt)
        cur_prompt += step_def
        entity_def = ''
        for lst in entity_bank.values():
            entity_def += f"    self.{text_to_code(lst[0])}.{text_to_code(lst[1])} ="
            cur_prompt += entity_def

            state = codex_entity(cur_prompt)

            if 'true' in state.strip().lower():
                entity_def += ' True\n'
                pred_step.append((lst[0], lst[1], 'more likely'))
            elif 'false' in state.strip().lower():
                entity_def += ' False\n'
                pred_step.append((lst[0], lst[1], 'less likely'))
            else:
                entity_def += " None\n"
                pred_step.append([])
        prompt += step_def
        prompt += entity_def
        for i, event in enumerate(events):
            prompt += f"    self.event{i}.change ="
            step_prediction = codex_event(prompt)
            prompt += step_prediction + '\n'
            if 'more likely' in step_prediction.lower():
                pred_step.append((f'event{i}', 'more likely'))
            elif 'less likely' in step_prediction.lower():
                pred_step.append((f'event{i}', 'less likely'))
            else:
                pred_step.append([])

            prediction += step_prediction
        #print(prompt)
        pred_res.append(pred_step)

    #step_changes = parse_codex_prediction(prediction)
    return pred_res

    
def codex_entity(prompt):
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


def codex_event(prompt):
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
        except (openai.error.RateLimitError, openai.error.APIConnectionError) as e:
            #print(e)
            #print("Retrying in 10 seconds")
            time.sleep(10)

    gen_code = ret["choices"][0]["text"]#.strip().split('\n')[0]

    return gen_code
#%%
with open('/Users/seacow/School/UPenn/Research/Procedural Reasoning/v2/predict_entity/data_dev_v2_entity.json') as f:
    jobj = json.load(f)
    jout = jobj.copy()

all_gold_changes = []
all_pred_changes = []

for id,v in tqdm(jobj.items()):
    goal = v['goal']
    entity_bank = v['entity_bank']
    steps = []
    events = []
    gold_event_changes = []
    for i,w in enumerate(v['steps']):
        if i == 0:
            continue
        current_event_changes = []
        for u in w:
            if u["type"] == "multihop":
                if u["event"] not in events:
                    events.append(u["event"])
                event_index = events.index(u["event"])
                current_event_changes.append((f"event{event_index}", u["change"].split()[0]))
            if u["type"] == "step":
                steps.append(u["step"])
        gold_event_changes.append(current_event_changes)

    pred_proc = entity_and_event(goal, steps, events, entity_bank)
    all_pred_changes.append(pred_proc)

    for i,x in enumerate(pred_proc):
        for y in x:
            if len(y) == 2:
                jout[id]["steps"][i+1].append({
                                "type": "predicted_event",
                                "event": y[0],
                                "change": y[1]
                            })
            elif len(y) == 3:
                jout[id]["steps"][i+1].append({
                                "type": "predicted_entity",
                                "entity": y[0],
                                "attribute": y[1],
                                "change": y[2]
                            })
#    #print(len(gold_event_changes))
#    #print(len(pred_changes))
    #assert(len(gold_event_changes) == len(pred_changes))
    if(len(gold_event_changes) < len(pred_proc)):
        print("Pred changes are more than gold, truncating.")
        pred_changes = pred_changes[:len(gold_event_changes)]
#    #break
#    
jout_test = deepcopy(jout)
for id,v in tqdm(jout_test.items()):
    steps = []
    events = []
    for i,w in enumerate(v['steps']):
        if i == 0:
            continue
        for u in w:
            if u["type"] == "multihop":
                if u["event"] not in events:
                    events.append(u["event"])
    for i, w in enumerate(v['steps']):
        if i==0:
            continue 
        for j, u in enumerate(w):
            if u['type'] == 'predicted_event':
                jout_test[id]['steps'][i][j]['event'] = events[int(u['event'][-1])]



with open(f'data_dev_out_hainiu.json','w') as fw:
    json.dump(jout_test, fw, indent=4)

"""
    all_gold_changes += gold_event_changes
    all_pred_changes += pred_changes

pred_all, pred_correct, gold_all, gold_correct = 0,0,0,0
assert(len(all_gold_changes) == len(all_pred_changes))
for gold_step_changes, pred_step_changes in zip(all_gold_changes, all_pred_changes):
    for gold_step_change in gold_step_changes:
        gold_all += 1
        if gold_step_change in pred_step_changes:
            gold_correct += 1
    for pred_step_change in pred_step_changes:
        pred_all += 1
        if pred_step_change in gold_step_changes:
            pred_correct += 1

precision = pred_correct/pred_all
recall = gold_correct/gold_all
f1 = 2 * precision * recall / (precision + recall)
print("Precision:", precision)
print("Recall:", recall)
print("F1:", f1)
"""


#%%
