#%%
import os 
import sys
import json
import time
import openai
import pickle
import argparse
from tqdm import tqdm
from copy import deepcopy
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix, ConfusionMatrixDisplay


def gpt3(prompt):
    while True:
        try:
            ret = openai.Completion.create(
                engine=f"text-curie-001",
                prompt=prompt,
                temperature=0,
                max_tokens=128,
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

    gen_text = ret["choices"][0]["text"]#.strip().split('\n')[0]

    return gen_text
# %%
parser = argparse.ArgumentParser()
parser.add_argument('--data_path', type=str, required=True, help='path to the CREPE dataset')
parser.add_argument('--key', type=str, help='path to OpenAI API Key')
args = parser.parse_args()

openai.api_key_path = args.key

with open(args.data_path, 'r') as f:
    data = json.load(f)
f.close()

num_call = 0
all_res = []
for key, val in tqdm(data.items()):
    cur_goal = val['goal']
    cur_steps = []
    cur_events = []
    for step_lst in val['steps']:
        for lst in step_lst:
            if 'event' in lst.keys():
                if (event := lst['event']) not in cur_events:
                    cur_events.append(event)
            elif 'step' in lst.keys():
                cur_steps.append(lst['step'])

    prompt = open('./prompt/prompt.txt', 'r').read()
    prompt += f"Goal: {' '.join([w.capitalize() for w in cur_goal.split()])}"
    if prompt[-1] != '.':
        prompt += '.'
    prompt += '\n'
    
    proc_res = {e: [] for e in cur_events}
    for i, event in enumerate(cur_events):
        cur_question = f'What is the likelihood that {event.replace(".", "")}?'
        prev_ans = 'unrelated'
        context = "Start."
        for j, step in enumerate(cur_steps):
            if j == 0:
                continue
            if j == 2:
                context = cur_steps[1].capitalize()
                
            cur_prompt = deepcopy(prompt)
            cur_prompt += f'Context: {context}\nStep: {step.capitalize()}\n'
            cur_prompt += f'Question: {cur_question}'
            
            res = gpt3(cur_prompt)
            res_lst = res.split('\n')
            ans = res_lst[-1]
            try:
                res = ans.split(':')[-1].strip().split()[0]
            except:
                res = prev_ans

            if res == 'likely':
                proc_res[event].append('likely')
                prev_ans = 'likely'
            elif res == 'unlikely':
                proc_res[event].append('unlikely')
                prev_ans = 'unlikely'
            else:
                proc_res[event].append(prev_ans)
            context += ' ' + step.capitalize()

    all_res.append(proc_res)

#%%
with open('gpt3_dev_result_dict.pkl', 'wb') as f:
    pickle.dump(all_res, f)                
f.close()

# %%
y_true = []
y_pred = []
for pred_proc, proc_dict in zip(all_res, data.values()):
    steps = proc_dict['steps']
    events = list(pred_proc.keys())
    
    for event in events:
        for step_lst in steps[1:]:
            cur_ans = 0
            for lst in step_lst:
                if 'event' in lst.keys() and lst['event'] == event:
                    cur_ans = 1 if 'more' in lst['change'] else 2
            y_true.append(cur_ans)
        
        pred_ans = pred_proc[event]
        assert len(steps[1:]) == len(pred_ans)
        cur_ans = 0
        prev_lab = pred_ans[0]
        y_pred.append(cur_ans)
        for lab in pred_ans[1:]:
            cur_ans = 0
            if lab != prev_lab:
                prev_lab = lab
                cur_ans = 1 if lab == 'likely' else 2
            y_pred.append(cur_ans)


# %%
f1 = f1_score(y_true, y_pred, average='macro')
acc = accuracy_score(y_true, y_pred)
print(f"f1: {f1}")
print(f"acc: {acc}")

conf_mtx = confusion_matrix(y_true, y_pred)
ConfusionMatrixDisplay(conf_mtx, display_labels=['equally', 'more', 'less']).plot()
cur_dir = os.getcwd()
plt.savefig(os.path.join(cur_dir, 'conf_mtx.png'))
# %%
