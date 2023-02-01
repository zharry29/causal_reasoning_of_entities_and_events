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
                engine=f"text-davinci-003",
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


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str, required=True, help='path to the CREPE dataset')
    parser.add_argument('--key', type=str, help='path to OpenAI API Key')
    return parser.parse_args()


def main():
    args = get_args()

    openai.api_key_path = args.key

    with open(args.data_path, 'r') as f:
        data = json.load(f)
    f.close()

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

        prompt = open('./prompts.txt', 'r').read()
        prompt += f"\n\nGoal: {' '.join([w.capitalize() for w in cur_goal.split()])}"
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
                cur_prompt += f'Question: {cur_question}\nAnswer:'

                res = gpt3(cur_prompt)
                ans = res.strip().replace('"', '').replace('"', '')
                if 'more' in ans:
                    proc_res[event].append('likely')
                    prev_ans = 'likely'
                elif 'less' in ans:
                    proc_res[event].append('unlikely')
                    prev_ans = 'unlikely'
                else:
                    proc_res[event].append(prev_ans)
                context += ' ' + step.capitalize()

        all_res.append(proc_res)

    if 'dev' in args.data_path:
        fname = 'gpt3_dev_result.pkl'
    else:
        fname = 'gpt3_test_result.pkl'

    with open(f'./results/{fname}', 'wb') as f:
        pickle.dump(all_res, f)                
    f.close()


if __name__ == '__main__':
    main()
