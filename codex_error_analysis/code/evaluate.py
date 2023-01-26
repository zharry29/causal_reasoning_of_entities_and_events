#%%
import os
import json
import argparse
from sklearn.metrics import f1_score, confusion_matrix, ConfusionMatrixDisplay

parser = argparse.ArgumentParser()

parser.add_argument('--data_path', type=str, required=True)

args = parser.parse_args()

def main():
    with open(args.data_path, 'r') as f:
        data = json.load(f)
    f.close()

    # relatedness
    event_r_pred = []
    event_r_true = []
    event_ur_pred = []
    event_ur_true = []

    for val in data.values():
        steps = val['steps']
        for step_lst in steps:
            cur_types = [d.get('type') for d in step_lst]
            if 'predicted_event' in cur_types and 'event' in cur_types and 'predicted_entity' in cur_types:
                ind = 0
                for d in step_lst:
                    if d['type'] == 'predicted_entity':
                        if d['label'][0] == 'related':
                            ind = 1
                    if d['type'] == 'event':
                        true_change = 0 if d['change'] == 'less likely' else 1
                    if d['type'] == 'predicted_event':
                        pred_change = 0 if d['change'] == 'less likely' else 1
            
                if ind:
                    event_r_pred.append(pred_change)
                    event_r_true.append(true_change)
                else:
                    event_ur_pred.append(pred_change)
                    event_ur_true.append(true_change)

    assert len(event_r_pred) == len(event_r_true)                    
    print('\n')        
    print(f"There are {len(event_r_pred)} event predictions come with a RELATED (entity state).")
    print(f"There are {len(event_ur_pred)} event predictions come with an UN-RELATED (entity state).")
    print('\n')
    print(f"F1 Score for Event with RELATED Entity States: {f1_score(event_r_true, event_r_pred):.2f}")
    print(f"F1 Score for Event with UNRELATED Entity States: {f1_score(event_ur_true, event_ur_pred):.2f}")


if __name__ == '__main__':
    main()
