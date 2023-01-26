# %%
import re
import sys
import json
import time
import openai
import pickle
import argparse
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


def goal_to_code(goal):
    if goal[:6].lower() == 'how to':
        goal = goal[6:].strip()
    return '_'.join(goal.capitalize().split())


def parse_codex_prediction(gen_code):
    #print(gen_code)
    step_changes = []
    current_step_changes = []
    for line in gen_code.split('\n')[1:]:
        line = line.strip()
        if line.startswith('def '):
            step_changes.append(current_step_changes) 
            current_step_changes = []
        elif line.startswith('self.event'):
            if " -= " in line:
                change = "less"
            elif " += " in line:
                change = "more"
            current_step_changes.append((line[5:11], change))
        elif not line:
            break
    step_changes.append(current_step_changes) 
    #print(step_changes)
    return step_changes


def parse_01hop_result(res):
    pred = [[] for _ in range(len(res[0]))]
    for i, lst in enumerate(res):
        cur_name = f"event{i}"
        for j, res in enumerate(lst):
            if '0' in res:
                pred[j].append((cur_name, 'more'))
            elif '1' in res:
                pred[j].append((cur_name, 'less'))
    return pred


def parse_01_ver2_0_result(all_pred_changes):
    all_res = []
    for pred_lst in all_pred_changes:
        cur_res = [[] for _ in range(len(pred_lst[0]))]
        for i in range(len(pred_lst[0])):
            for j, lst in enumerate(pred_lst):
                if lst[i] == '"unrelated"':
                    pass
                elif lst[i] == '"likely"':
                    cur_res[i].append(tuple((f"event{j}", "more")))
                else:
                    cur_res[i].append(tuple((f"event{j}", "less")))
        all_res.append(cur_res)
    return all_res


def entity_and_event(goal, steps, entities, events, gold_entity_changes):
    prompt = open('./prompt/0hop_1hop_hainiu_ver2_0.py').read()

    options = '["more likely", "less likely", "equally likely"]'
    goal_entity_changes = []

    prompt += f'Goal = "{goal.capitalize()}"\n\n'

    for event in events:
        cur_prompt = deepcopy(prompt)
        cur_question = f"What is the likelihood that {event.lower().replace('.', '?')}"
        cur_entity_change = []
        
        for i, (step, entity) in enumerate(zip(steps, gold_entity_changes)):
            cur_prompt += f'Context = "I {step.lower().strip()}'
            
            if entity:
                cur_prompt += f' After this, '
                init = 1
                for e in entities:
                    for d in entity:
                        if d['entity'].strip() == e.strip():
                            cur_attr = d['attribute']
                            if d['change'] == 'more likely':
                                likelihood = 'is'
                            else:
                                likelihood = 'is not'
                        if init:
                            cur_prompt += f'{e} {likelihood} {cur_attr}'
                            init = 0
                        else:
                            cur_prompt += f' and {e} {likelihood} {cur_attr}'

                cur_prompt += '."\n'
            else:
                cur_prompt += '"\n'
            
            cur_prompt += f'Question = {cur_question}\nOptions = {options}\nAnswer = '

            ind = 1
            while ind:
                try:
                    prediction = codex(cur_prompt)
                    ind = 0
                    time.sleep(5)
                except openai.error.RateLimitError:
                    time.sleep(10)
                    pass 
            cur_entity_change.append(prediction)
            cur_prompt += f'{prediction}\n\n'
        goal_entity_changes.append(cur_entity_change)
    return goal_entity_changes
    

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

    #time.sleep(8)
    #if 'True' in gen_code:
    #    return 'True'
    #elif 'False' in gen_code:
    #    return 'False'
    #else:
    #    return 'UNK'
    return gen_code


# %%
with open('../../../data_test_v2.json') as f:
        jobj = json.load(f)

for id,v in tqdm(jobj.items()):
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
            if u["type"] == "event":
                if u["event"] not in events:
                    events.append(u["event"])
                event_index = events.index(u["event"])
                current_event_changes.append((f"event{event_index}", u["change"].split()[0]))
            if u["type"] == "entity":
                if u["entity"].strip() not in entities:
                    entities.append(u['entity'])
                current_entity_changes.append(u)
            if u["type"] == "step":
                steps.append(u["step"])
        gold_event_changes.append(current_event_changes)
        gold_entity_changes.append(current_entity_changes)

    pred = entity_and_event(goal, steps, entities, events, gold_entity_changes)

    for pred_lst, event in zip(pred, events):
        for i, res in enumerate(pred_lst):
            if '2' not in res:
                res = 'more likely' if ('0' in res) else 'less likely'
                res_dict = {'type': 'predicted_event', 'event': event, 'change': res}
                jobj[id]['steps'][i].append(res_dict)


with open('../../data_test_v2_entity_and_event.json', 'w') as f:
    json.dump(jobj, f, indent=4) 
f.close()
    
    
#%%

# pred_all, pred_correct, gold_all, gold_correct = 0,0,0,0
# assert(len(all_gold_changes) == len(all_pred_changes))
# for gold_step_changes, pred_step_changes in zip(all_gold_changes, all_pred_changes):
#     for gold_step_change in gold_step_changes:
#         gold_all += 1
#         if gold_step_change in pred_step_changes:
#             gold_correct += 1
#     for pred_step_change in pred_step_changes:
#         pred_all += 1
#         if pred_step_change in gold_step_changes:
#             pred_correct += 1

# precision = pred_correct/pred_all
# recall = gold_correct/gold_all
# f1 = 2 * precision * recall / (precision + recall)
# print("Precision:", precision)
# print("Recall:", recall)
# print("F1:", f1)


# # %%
# run_experiment()




# #
# #    
# #    
# #    
# #    
# # %%
# def decode_prompt2_5(goal_entity_changes):
#     parsed_res = [[] for _ in range(len(steps))]

#     for i, lst in enumerate(goal_entity_changes):
#         prev_state = lst[0]
#         for j in range(1, len(parsed_res)):
#             if lst[j] != prev_state:
#                 if '0' in lst[j]:
#                     parsed_res[j].append(tuple((f"event{i}", "more")))
#                 elif '1' in lst[j]:
#                     parsed_res[j].append(tuple((f"event{i}", "less")))
#                 prev_state = lst[j]    
#     return parsed_res
# # %%
# def test(goal, steps, entities, events, gold_entity_changes):
#     prompt = open('/Users/seacow/School/UPenn/Research/Procedural Reasoning/v2/hainiu_v2/0hop_1hop_hainiu_ver2_5.py').read()

#     options = '["likely", "unlikely", "irrelevant"]'
#     goal_entity_changes = []
#     pred_event_changes = []

#     prompt += f'Goal = "{goal.capitalize()}"\n'

#     for event in events:
#         cur_question = f"What is the likelihood that {event.lower().replace('.', '?')}"
#         cur_entity_change = []
        
#         cur_entity_states = {e: {} for e in entities}
        
#         for i, (step, entity) in enumerate(zip(steps, gold_entity_changes)):
#             cur_prompt = deepcopy(prompt)
#             cur_prompt += f'Context = "I {step.lower().strip()}'
            
#             if entity:
#                 for e in entities:
#                     for d in entity:
#                         if d['entity'].strip() == e.strip():
#                             cur_attr = d['attribute']
#                             if d['change'] == 'more likely':
#                                 likelihood = 'is'
#                             else:
#                                 likelihood = 'is not'

#                             if cur_attr not in cur_entity_states[e].keys():
#                                 cur_entity_states[e][cur_attr] = likelihood
#                             elif cur_entity_states[e][cur_attr] != likelihood:
#                                 cur_entity_states[e][cur_attr] = likelihood
                    
#             for key, val in cur_entity_states.items():
#                 if not val:
#                     cur_prompt += f''
#                 else:
#                     cur_state = key
#                     for attr, lik in val.items():
#                         cur_state += f' {lik} {attr}'
#                         cur_state += ' and'
#                     cur_prompt += f' After this, {cur_state[:-4]}.'
#             cur_prompt += '"\n'
            
#             cur_prompt += f'Question = {cur_question}\nOptions = {options}\nAnswer = '

#             ind = 1
#             while ind:
#                 try:
#                     prediction = codex(cur_prompt)
#                     ind = 0
#                     time.sleep(5)
#                 except openai.error.RateLimitError:
#                     time.sleep(10)
#                     pass 
#             cur_entity_change.append(prediction)
#         goal_entity_changes.append(cur_entity_change)
#         pred_event_changes.append(decode_prompt2_5(goal_entity_changes))
#     return pred_event_changes

# # %%


        

# # %%
