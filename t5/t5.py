import json
import sys
import pickle
import time
import argparse
import torch
from tqdm import tqdm
import numpy as np
import copy
import os

from transformers import T5Tokenizer, T5ForConditionalGeneration

def t5(prompt, tokenizer, model):
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to("cuda:0")
    losses = []
    for answer in ["yes", "no"]:
        labels = tokenizer(answer, return_tensors="pt").input_ids.to("cuda:0")
        loss = model(input_ids=input_ids, labels=labels).loss
        losses.append(loss.item())
    return ["yes", "no"][np.argmin(losses)]

def parse_codex_res(res: list) -> list:
    out = []
    prev_state = None
    for state in res:
        if not prev_state:
            prev_state = state 
        
        if state == prev_state:
            out.append('equally likely')
        else:
            prev_state = state 
            if state == 'yes':
                out.append('more likely')
            else:
                out.append('less likely')
    assert len(out) == len(res)
    return out

def main(model_name, split):

    if model_name == "t0":
        tokenizer = T5Tokenizer.from_pretrained("bigscience/T0pp")
        model = T5ForConditionalGeneration.from_pretrained("bigscience/T0pp", torch_dtype=torch.float16).to("cuda:0")

    elif model_name == "t5":
        tokenizer = T5Tokenizer.from_pretrained("t5-3b")
        model = T5ForConditionalGeneration.from_pretrained("t5-3b", torch_dtype=torch.float16).to("cuda:0")

    if split == "dev":
        with open('../data_dev_v2.json') as f:
            jobj = json.load(f)
            jout = jobj.copy()

    elif split == "test":
        with open('../data_test_v2.json') as f:
            jobj = json.load(f)
            jout = jobj.copy()

    for id,v in tqdm(jobj.items()):
        goal = v['goal']
        events = []
        steps = ["Start."]
        for i,w in enumerate(v['steps']):
            for u in w:
                if i == 0: continue
                if u["type"] == "event":
                    if u["event"] not in events:
                        events.append(u["event"])
                elif u["type"] == "step":
                    steps.append(u['step'])
        
        for event in events:
            question = "Is it okay that {}".format(event)
            raw_predictions = []
            for i,w in enumerate(v['steps']):
                if i == 0: continue
                past_steps = steps[:i]
                current_step = steps[i]        
            
                current_prompt = "Goal: {}\nContext: {}\nStep: {}\nQuestion: {}\nAnswer: ".format(goal, " ".join(past_steps), current_step, question)
                raw_predictions.append(t5(current_prompt, tokenizer, model))

            predictions = [None] + parse_codex_res(raw_predictions)
            for i, label in enumerate(predictions):
                if i == 0 or label == "equally likely": continue

                jout[id]['steps'][i].append({
                    "type": "predicted_event",
                    "event": event,
                    "change": label
                    })

    outfile = f'data_{split}_out_{model_name}.json'
    with open(outfile,'w') as fw:
        json.dump(jout, fw, indent=4)
                
if __name__ == "__main__":
    model_name, split = sys.argv[1:]
    main(model_name, split)