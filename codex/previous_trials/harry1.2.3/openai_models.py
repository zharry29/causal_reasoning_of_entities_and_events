import openai
import json
import time
import argparse

openai.api_key = "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" # Harry
#openai.api_key = "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" # Shuyan

parser = argparse.ArgumentParser()
parser.add_argument('--prompt', type=str, default='')
parser.add_argument('--at_once', action='store_true')
parser.add_argument('--gold_entity', action='store_true')

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
    #raise SystemExit()
    step_changes = []
    current_step_changes = []
    current_variables = []
    initial = True
    for line in gen_code.split('\n'):
        line = line.strip()
        if line.startswith('def '):
            if not initial:
                step_changes.append(current_step_changes) 
                current_step_changes = []
            initial = False
        elif line.startswith('self.') and not line.startswith('self.event'):
            line = line.replace('.','_')
            variable = line.split(' = ')[0]
            try:
                variable_value = eval(line.split(' = ')[1])
            except (NameError, IndexError) as e:
                print(e)
                continue
            if isinstance(variable_value, str):
                variable_value = '"' + variable_value + '"'
            #elif isinstance(variable_value, bool):
            else:
                variable_value = str(variable_value)
            current_variables.append((variable,variable_value))
            #current_step_changes.append((line.split('.')[1], line.split('.')[2].split(' = ')[0], line.split(' = ')[1].strip('"')))
        elif line.startswith('self.event'):
            line = line.replace('.','_').split('#')[0]
            for variable, variable_value in current_variables:
                line = line.replace(variable, variable_value)
            try:
                change = "more likely" if eval(line.split(' = ')[1]) else "less likely"
            except NameError:
                continue
            current_step_changes.append((line[5:11], change))
        elif not line:
            break
    step_changes.append(current_step_changes) 
    #print(step_changes)
    return step_changes

def entity_and_event(goal, steps, entities, events, gold_entity_changes):
    prompt = open("prompts/1hop_0hop.py").read()
    prompt_addition = "class " + text_to_code(goal, capitalize=True) + ":\n"
    prompt_addition += "  # Init\n"
    prompt_addition += '\n'.join([f"  # {s}" for s in steps]) + '\n'
    prompt_addition += '  def init(self, '
    #prompt += ', '.join(entities) + ', '
    prompt_addition += ', '.join([f"event{i}" for i in range(len(events))]) + "):\n"
    for i, entity in enumerate(entities):
        prompt_addition += f"    self.{text_to_code(entity)} = {text_to_code(entity, capitalize=True)}()\n"
    for i, event in enumerate(events):
        prompt_addition += f"    self.event{i} = event{i} # {event}\n"
    
    #print(prompt_addition)
    #raise SystemExit()
    prompt += prompt_addition
    prediction = ""
    if not args.at_once:        
        for step, entity_changes in zip(steps, gold_entity_changes):
            step_def = f"  def {text_to_code(step,lower=True)}(self):\n"
            for entity_change in entity_changes:
                if args.gold_entity:
                    change_code = "self." + text_to_code(entity_change["entity"]) + '.' + text_to_code(entity_change["attribute"])
                    if entity_change["change"] == "more likely":
                        change_code += " = True\n"
                    elif entity_change["change"] == "less likely":
                        change_code += " = False\n"
                    step_def += "    " + change_code
            prompt += step_def
            #print(prompt)
            #raise SystemExit()
            prediction += step_def
            step_prediction = codex(prompt).split('  def')[0]
            #print(step_prediction)
            prediction += step_prediction
            prompt += step_prediction
    else:
        prediction = codex(prompt)
    step_changes = parse_codex_prediction(prediction)
    return step_changes

def event_only(goal, steps, entities, events, gold_entity_changes):
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
    if not args.at_once:        
        for step in steps:
            step_def = f"  def {text_to_code(step,lower=True)}(self):\n"
            prompt += step_def
            prediction += step_def
            #print(prompt)
            #print('\n\n\n\n')
            step_prediction = codex(prompt).split('  def')[0]
            print(step_prediction)
            prediction += step_prediction
            prompt += step_prediction
    else:
        prediction = codex(prompt)  
    #print(prediction)
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
                stop=["\n\n"]
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

with open('../../data_dev_v2.json') as f:
    jobj = json.load(f)
    jout = jobj.copy()

all_gold_changes = []
all_pred_changes = []

for id,v in jobj.items():
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
    pred_changes = eval(args.prompt)(goal, steps, entities, events, gold_entity_changes)
    #print(pred_changes)
    for i,x in enumerate(pred_changes):
        for y in x:
            if len(y) == 2:
                jout[id]["steps"][i+1].append({
                                "type": "predicted_event",
                                "event": events[int(y[0][-1])],
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

outfile = f'data_dev_out_{args.prompt}.json' if not args.gold_entity else f'data_dev_out_gold_{args.prompt}.json'
with open(outfile,'w') as fw:
    json.dump(jout, fw, indent=4)

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