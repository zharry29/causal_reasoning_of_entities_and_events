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

def parse_prediction(gen_text):
    print(gen_text)
    #raise SystemExit()
    step_changes = []
    current_step_changes = []
    initial = True
    for line in gen_text.split('\n'):
        line = line.strip()
        if line.startswith('I '):
            if not initial:
                step_changes.append(current_step_changes) 
                current_step_changes = []
            initial = False
        elif line.startswith('"'):
            if 'is less likely to happen' in line:
                change = "less"
            elif 'is more likely to happen' in line:
                change = "more"
            elif 'is equally likely to happen' in line:
                continue
            else:
                print(line)
                raise ValueError()
            current_step_changes.append((line.split('"')[1], change))
        #elif not line:
        #    break
    step_changes.append(current_step_changes) 
    print(step_changes)
    return step_changes

def gpt3_prompt1_8_0hop_and_1hop(goal, steps, entities, events, gold_entity_changes):
    prompt = open("prompts/1hop_0hop.txt").read()
    
    prompt += "Goal: " + goal + "\n\n"
    prompt += 'I am interested in the following events:\n'
    for event in events:
        prompt += event + '\n'
    prompt += '\n'
    prediction = ""
    if args.step_by_step:        
        for step, g_e_c in zip(steps, gold_entity_changes):
            step_def = f"I {step[0].lower() + step[1:].strip().strip('.')}. After this, "
            for entity_change in g_e_c:
                be_word = " is" if entity_change["entity"][-1] != 's' else " are"
                if entity_change["change"] == "less likely":
                    be_word += " not"
                step_def += entity_change["entity"] + be_word + " " + entity_change["attribute"] + ", "
            step_def += "\n"
            prompt += step_def
            prediction += step_def
            print(prompt)
            #print('\n\n\n\n')
            step_prediction = gpt3(prompt)
            #print(step_prediction)
            prediction += step_prediction + '\n\n'
            prompt += step_prediction + '\n\n'
    else:
        prediction = gpt3(prompt)  
    #print(prediction)
    #raise SystemExit()
    step_changes = parse_prediction(prediction)
    return step_changes

def gpt3_prompt1_8_1hop_only(goal, steps, entities, events, gold_entity_changes):
    prompt = open("prompts/1hop_only.txt").read()
    
    prompt += "Goal: " + goal + "\n\n"
    prompt += 'I am interested in the following events:\n'
    for event in events:
        prompt += event + '\n'
    prompt += '\n'
    prediction = ""
    if args.step_by_step:        
        for step in steps:
            step_def = f"I {step[0].lower() + step[1:].strip().strip('.')}. After this,\n"
            prompt += step_def
            prediction += step_def
            #print(prompt)
            #print('\n\n\n\n')
            step_prediction = gpt3(prompt)
            #print(step_prediction)
            prediction += step_prediction + '\n\n'
            prompt += step_prediction + '\n\n'
    else:
        prediction = gpt3(prompt)  
    #print(prediction)
    #raise SystemExit()
    step_changes = parse_prediction(prediction)
    return step_changes
    
def gpt3(prompt):
    while True:
        try:
            ret = openai.Completion.create(
                engine=f"text-davinci-002",
                prompt=prompt,
                temperature=0,
                max_tokens=1024,
                top_p=1,
                logprobs=5,
                frequency_penalty=0,
                presence_penalty=0,
                stop=["\n\n"]
            )
            break
        except openai.error.RateLimitError as e:
            print(e)
            print("Retrying in 10 seconds")
            time.sleep(10)

    gen_text = ret["choices"][0]["text"]#.strip().split('\n')[0]

    return gen_text

with open('../../data_dev_v2.json') as f:
    jobj = json.load(f)

all_gold_changes = []
all_pred_changes = []

for id,v in jobj.items():
    goal = v['goal']
    steps = []
    events = []
    entities = []
    gold_event_changes = []
    gold_entity_changes = []
    for w in v['steps'][1:]:
        current_event_changes = []
        current_entity_changes = []
        for u in w:
            if u["type"] == "multihop":
                if u["event"] not in events:
                    events.append(u["event"])
                event_index = events.index(u["event"])
                current_event_changes.append((u["event"], u["change"].split()[0]))
            if u["type"] == "entity":
                if u["entity"] not in entities:
                    entities.append(u["entity"])  
                current_entity_changes.append(u)
            if u["type"] == "step":
                steps.append(u["step"])
        gold_event_changes.append(current_event_changes)
        gold_entity_changes.append(current_entity_changes)

    #print(gold_event_changes)
    pred_changes = eval(args.prompt)(goal, steps, entities, events, gold_entity_changes)
    #print(pred_changes)
    #print(len(gold_event_changes))
    #print(len(pred_changes))
    #assert(len(gold_event_changes) == len(pred_changes))
    if(len(gold_event_changes) < len(pred_changes)):
        print("Pred changes are more than gold, truncating.")
        pred_changes = pred_changes[:len(gold_event_changes)]
    all_gold_changes += gold_event_changes
    all_pred_changes += pred_changes
    #break

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
