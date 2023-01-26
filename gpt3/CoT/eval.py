import pickle
import argparse
from sklearn.metrics import accuracy_score, f1_score

parser = argparse.ArgumentParser()
parser.add_argument(
    '--gt_path', type=str
)
parser.add_argument(
    '--pred_path', type=str
)

def main():
    args = parser.parse_args()

    with open(args.gt_path, 'rb') as f:
        gt = pickle.load(f)
    f.close()

    with open(args.pred_path, 'rb') as f:
        pred = pickle.load(f)
    f.close()

    gt = [lst for sublst in gt for lst in sublst]
    pred = [lst for sublst in pred for lst in sublst]

    f1 = f1_score(gt, pred, average='macro')

    print(f1)


if __name__ == '__main__':
    main()