import os
import json 
import pickle 
import argparse
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix, ConfusionMatrixDisplay


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--data_path', type=str, required=True, help='path to the CREPE dataset'
    )
    parser.add_argument(
        '--predictions', type=str, required=True, help='path to the pickle file that stores the predictions'
    )
    return parser.parse_args()


def main():
    args = get_args()
    
    with open(args.data_path, 'r') as f:
        data = json.load(f)
    f.close()

    with open(args.predictions, 'rb') as f:
        all_res = pickle.load(f)
    f.close()

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

    f1 = f1_score(y_true, y_pred, average='macro')
    acc = accuracy_score(y_true, y_pred)
    print(f"f1: {f1}")
    print(f"acc: {acc}")

    conf_mtx = confusion_matrix(y_true, y_pred)
    ConfusionMatrixDisplay(conf_mtx, display_labels=['equally', 'more', 'less']).plot()
    cur_dir = os.getcwd()
    plt.savefig(os.path.join(cur_dir, 'conf_mtx.png'))


if __name__ == '__main__':
    main()