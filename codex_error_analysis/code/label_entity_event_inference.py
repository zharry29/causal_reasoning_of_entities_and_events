import os
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--output_path', type=str, required=True)

args = parser.parse_args()

def main():
    
    with open(args.output_path, 'r') as f:
        data = json.load(f)
    f.close()


    annotator = input("Name of the annotator:\n")
    os.system('clear')

    total_event, total_entity = 0, 0
    for key, val in data.items():
        steps = val['steps']
        for step_idx, step_lst in enumerate(steps):
            cur_types = [d.get('type') for d in step_lst]
            if 'predicted_event' in cur_types and 'predicted_entity' in cur_types:
                event_idx = [i for i, x in enumerate(cur_types) if x == 'predicted_event']
                entity_idx = [i for i, x in enumerate(cur_types) if x == 'predicted_entity']
                for i in event_idx:
                    cur_event = step_lst[i]['event']
                    for j in entity_idx:
                        entity_dict = step_lst[j]
                        entity_attr = tuple((entity_dict['entity'], entity_dict['attribute']))
                        print(cur_event)
                        print(entity_attr)
                        inf_lab = input("e (entailment); c (contradiction); u (unrelated):\n")
                        if inf_lab.lower() == 'e':
                            inf_lab = 'entailment'
                        elif inf_lab.lower() == 'c':
                            inf_lab = 'contradiction'
                        else:
                            inf_lab = 'unrelated'
                        data[key]['steps'][step_idx][i]["event_entity_inference"] = (*entity_attr, inf_lab)
                        os.system('clear')
                        
                
    


    with open(f'./data/data_dev_entity_event_inference_labeled_{annotator}.json', 'w') as f:
        json.dump(data, f, indent=4)
    f.close()

if __name__ == '__main__':
    main()