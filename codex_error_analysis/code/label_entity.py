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


    annotator = input("Name of the annotator:")
    os.system('clear')

    total_pred_event, total_pred_entity = 0, 0

    for key, val in data.items():
        all_events = []
        for i, step_lst in enumerate(val['steps']):
            for dict in step_lst:
                if dict.get('type') == 'event':
                    if dict['event'] not in all_events:
                        all_events.append(dict['event'])
                    
        for i, step_lst in enumerate(val['steps']):
            step_types = [d.get('type') for d in step_lst]
            if 'predicted_event' in step_types and 'event' in step_types:
                total_pred_event += 1
                if 'predicted_entity' in step_types:
                    total_pred_entity += 1
                    for j, dict in enumerate(step_lst):
                        if dict.get('type') == 'step':
                            cur_step = f"Current Step:\n{dict['step']}"
                        if dict.get('type') == 'predicted_entity':
                            print(cur_step)
                            print(f'Events:')
                            for event in all_events:
                                print(event)
                            print(f"({dict['entity']}, {dict['attribute']}, {dict['change']})\nrelateded [y/n]")
                            lab1 = input()
                            lab1 = 'related' if lab1 == 'y' else 'unrelated'
                            print("correct [y/n]")
                            lab2 = input()
                            os.system('clear')
                            lab2 = 'correct' if lab2 == 'y' else 'incorrect'
                            data[key]['steps'][i][j]['label'] = [lab1, lab2]


    with open(f'./data/data_dev_out_entity_labeled_{annotator}.json', 'w') as f:
        json.dump(data, f, indent=4)
    f.close()

    print(f'Fraction of Event Prediction that Goes with Entity Prediction: {total_pred_entity / total_pred_event:.2f}')

if __name__ == '__main__':
    main()