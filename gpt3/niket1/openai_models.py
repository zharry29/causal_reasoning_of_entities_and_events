from json.tool import main
from mimetypes import init
import openai
import json
import sys
import pickle
import time
import argparse

openai.api_key = "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" # Harry

parser = argparse.ArgumentParser()
parser.add_argument('--zeroshot', action='store_true')

args = parser.parse_args()

def parse_gen(ret):
    preds = []
    prev_option = ""
    for i,line in enumerate(ret.split('\n')):
        if not line.startswith(f"Step {i+1}: ("):
            preds.append("unknown")
        else:
            option = line.strip(f"Step {i+1}: (")[0]
            if not prev_option:
                preds.append("equal")
            else:
                if option > prev_option:
                    preds.append("less")
                elif option < prev_option:
                    preds.append("more")
                else:
                    preds.append("equal")
            prev_option = option
    return preds

def gpt3_prompt(goal, steps, entities, events, gold_entity_changes):
    if args.zeroshot:
        prompt = ""
    else:
        prompt = open("prompts/1hop_only.txt").read()
    prediction = [[] for i in range(len(steps))]
    for event in events:
        prompt_add = ""
        prompt_add += f'"{goal.lower().capitalize()}" involves the followings steps:\n'
        for i, step in enumerate(steps):
            prompt_add += f"{i+1}: {step}\n"
        prompt_add += f"\nFor every step, find out how likely it is that {event.strip('.')}. Answer as (A) very likely (B) likely (C) not very likely (D) unlikely.\n\nStep 1: ("

        ret = gpt3(prompt + prompt_add)
        print(prompt_add, ret, sep='')
        print('\n')
        preds = parse_gen("Step 1: (" + ret)
        #print(preds)
        #print(steps)
        #print("\n\n\n")
        #raise SystemExit
        for i,pred in enumerate(preds):
            if pred in ["more","less"]:
                prediction[i].append((event,pred))
    
    return prediction
    
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

count = 0
for id,v in jobj.items():
    #if count == 5:
    #    break
    count += 1
    goal = v['goal']
    print(goal)
    steps = []
    events = []
    entities = []
    gold_event_changes = []
    gold_entity_changes = []
    for w in v['steps'][1:]:
        current_event_changes = []
        current_entity_changes = []
        for u in w:
            if u["type"] == "event":
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
    pred_changes = gpt3_prompt(goal, steps, entities, events, gold_entity_changes)
    print("Gold event changes:", gold_event_changes)
    print("Pred event changes::", pred_changes)
    print('\n#####\n')
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
