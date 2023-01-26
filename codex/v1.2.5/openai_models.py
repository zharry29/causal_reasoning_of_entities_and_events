import openai
import json
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--prompt', type=str, default='', help='Either predict events only, or predict entities and events.')
parser.add_argument('--split', type=str, default='dev', help='Either dev or test set.')
parser.add_argument('--at_once', action='store_true', help='Whether predict events for all steps at once, or one step at a time.')
parser.add_argument('--gold_entity', action='store_true', help='Whether provide gold entities. When at_once is set, only the involved entities are given. Otherwise, the entity-attribute-value tuples are given for each step.')
parser.add_argument('--key', type=str, default='harry', help='The name of the OpenAI API key file.')

args = parser.parse_args()
openai.api_key = open(f'../../api_keys/{args.key}.key').read()

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
        elif line.startswith('event'):
            if '.change = "less likely"' in line:
                change = "less likely"
            elif '.change = "more likely"' in line:
                change = "more likely"
            elif '.change = "equally likely"' in line:
                continue
            else:
                print(line)
                continue
                #raise ValueError()
            current_step_changes.append((line[0:6], change))
        elif not line:
            break
    step_changes.append(current_step_changes) 
    #print(step_changes)
    return step_changes

def event_only(goal, steps, entities, events, gold_entity_changes):
    prompt = open("prompts/1hop_only.py").read()
    
    prompt += "def " + text_to_code(goal) + "(" + ', '.join([f"event{i}" for i in range(len(events))]) + "):\n"
    prompt += "  # Init\n"
    prompt += '\n'.join([f"  # {s}" for s in steps]) + '\n'
    for i, event in enumerate(events):
        prompt += f"  event{i} = event{i} # {event}\n"
    #print(prompt)
    #raise SystemExit()
    prediction = ""
    if not args.at_once:        
        for step in steps:
            step_def = f"  def {text_to_code(step,lower=True)}():\n"
            prompt += step_def
            prediction += step_def
            #print(prompt)
            #print('\n\n\n\n')
            step_prediction = codex(prompt).split('  def')[0]
            print(step_prediction)
            prediction += step_prediction
            prompt += step_prediction
    else:
        #print(prompt)
        #raise SystemExit()
        prediction = codex(prompt)  
    #print(prediction)
    #raise SystemExit()
    step_changes = parse_codex_prediction(prediction)
    return step_changes
 
def entity_and_event(goal, steps, entities, events, gold_entity_changes):
    prompt = open("prompts/1hop_0hop.py").read()
    prompt_addition = "class " + text_to_code(goal, capitalize=True) + ":\n"
    prompt_addition += "  # Init\n"
    prompt_addition += '\n'.join([f"  # {s}" for s in steps]) + '\n'
    prompt_addition += '  def __init__(self, '
    #prompt += ', '.join(entities) + ', '
    prompt_addition += ', '.join([f"event{i}, subevent{i}" for i in range(len(events))]) + "):\n"
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
            prediction += step_def
            step_prediction = codex(prompt).split('  def')[0]
            #print(step_prediction)
            prediction += step_prediction
            prompt += step_prediction
    else:
        #print(prompt)
        #raise SystemExit()
        prediction = codex(prompt)
    step_changes = parse_codex_prediction(prediction)
    return step_changes
   
def codex(prompt):
    while True:
        try:
            ret = openai.Completion.create(
                engine=f"code-davinci-002",
                prompt=prompt,
                temperature=0,  # 0.7
                max_tokens=2000,
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

    gen_code = ret["choices"][0]["text"]
    return gen_code

with open(f'../../data_{args.split}_v2.json') as f:
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

    pred_changes = eval(args.prompt)(goal, steps, entities, events, gold_entity_changes)
    for i,x in enumerate(pred_changes):
        for y in x:
            try:
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
            except IndexError:
                continue
    if(len(gold_event_changes) < len(pred_changes)):
        print("Pred changes are more than gold, truncating.")
        pred_changes = pred_changes[:len(gold_event_changes)]

outfile = f'data_{args.split}_out_{args.prompt}'
if args.gold_entity:
    outfile += '_gold'
if args.at_once:
    outfile += '_atonce'
outfile += '.json'

with open(outfile,'w') as fw:
    json.dump(jout, fw, indent=4)