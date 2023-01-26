from json.tool import main
from mimetypes import init
import openai
import json
import sys
import pickle
import time
import argparse

openai.api_key = "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" # Harry
#openai.api_key = "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" # Shuyan

parser = argparse.ArgumentParser()
parser.add_argument('--prompt', type=str, default='')
parser.add_argument('--step_by_step', action='store_true')

args = parser.parse_args()

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
        elif line.startswith('self.event'):
            #if " -= " in line:
            #    change = "less"
            #elif " += " in line:
            #    change = "more"
            if " = False" in line:
                change = "less"
            elif " = True" in line:
                change = "more"
            current_step_changes.append((line[5:11], change))
        elif not line:
            break
    step_changes.append(current_step_changes) 
    #print(step_changes)
    return step_changes

def codex_prompt1_3_0hop_and_1hop(goal, steps, entities, events):
    prompt = open("prompts/1hop_0hop.py").read()
    prompt_addition = "class " + text_to_code(goal, capitalize=True) + ":\n"
    prompt_addition += "  # Init\n"
    prompt_addition += '\n'.join([f"  # {s}" for s in steps]) + '\n'
    prompt_addition += '  def init(self, '
    #prompt += ', '.join(entities) + ', '
    prompt_addition += ', '.join([f"event{i}" for i in range(len(events))]) + "):\n"
    for i, event in enumerate(events):
        prompt_addition += f"    self.event{i} = event{i} # {event}\n"
    #for i, entity in enumerate(entities):
    #    prompt += f"    self.{text_to_code(entity)} = {text_to_code(entity, capitalize=True)}()\n"
    
    print(prompt_addition)
    #raise SystemExit()

    prompt += prompt_addition
    prediction = codex(prompt)  
    step_changes = parse_codex_prediction(prediction)
    #print(step_changes) 
    return step_changes

def codex_prompt1_3_1hop_only(goal, steps, entities, events):
    prompt = open("prompts/1hop_only.py").read()
    
    prompt += "class " + text_to_code(goal, capitalize=True) + ":\n"
    prompt += "  # Init\n"
    prompt += '\n'.join([f"  # {s}" for s in steps]) + '\n'
    prompt += '  def init(self, ' + ', '.join([f"event{i}" for i in range(len(events))]) + "):\n"
    for i, event in enumerate(events):
        prompt += f"    self.event{i} = event{i} # {event}\n"
    #print(prompt)
    #raise SystemExit()
    prediction = ""
    if args.step_by_step:        
        for step in steps:
            step_def = f"  def {text_to_code(step,lower=True)}(self):\n"
            prompt += step_def
            prediction += step_def
            step_prediction = codex(prompt).split('  def')[0]
            #print(step_prediction)
            prediction += step_prediction
            prompt += step_prediction
    else:
        prediction = codex(prompt)  
    print(prediction)
    #raise SystemExit()
    step_changes = parse_codex_prediction(prediction)
    return step_changes
    
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
                stop=['\n\n']
            )
            break
        except openai.error.RateLimitError as e:
            print(e)
            print("Retrying in 10 seconds")
            time.sleep(10)

    gen_code = ret["choices"][0]["text"]#.strip().split('\n')[0]

    #time.sleep(8)
    #if 'True' in gen_code:
    #    return 'True'
    #elif 'False' in gen_code:
    #    return 'False'
    #else:
    #    return 'UNK'
    return gen_code

with open('data_dev_v2.json') as f:
    jobj = json.load(f)

all_gold_changes = []
all_pred_changes = []

for id,v in jobj.items():
    goal = v['goal']
    steps = []
    events = []
    entities = []
    gold_changes = []
    for w in v['steps'][1:]:
        current_changes = []
        for u in w:
            if u["type"] == "multihop":
                if u["event"] not in events:
                    events.append(u["event"])
                event_index = events.index(u["event"])
                current_changes.append((f"event{event_index}", u["change"].split()[0]))
            if u["type"] == "entity":
                if u["entity"] not in entities:
                    entities.append(u["entity"])  
            if u["type"] == "step":
                steps.append(u["step"])
        gold_changes.append(current_changes)

    print(gold_changes)
    pred_changes = eval(args.prompt)(goal, steps, entities, events)
    print(pred_changes)
    #print(len(gold_changes))
    #print(len(pred_changes))
    #assert(len(gold_changes) == len(pred_changes))
    if(len(gold_changes) < len(pred_changes)):
        print("Pred changes are more than gold, truncating.")
        pred_changes = pred_changes[:len(gold_changes)]
    all_gold_changes += gold_changes
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
