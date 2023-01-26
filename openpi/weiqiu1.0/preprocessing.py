import argparse
import json
import jsonlines

import os
import torch
import random
import numpy as np

import pdb
from tqdm import tqdm


# import nltk
# nltk.data.path.append('/nlp/data/weiqiuy/nltk_data')

def parse_args():
    parser = argparse.ArgumentParser()

    # paths and info
    parser.add_argument('--input-file', type=str, default='v2/data_dev_v2.json',
                        help='input dir')
    parser.add_argument('--output-file', type=str, default='v2/openpi/weiqiu1.0/0hop_questions.jsonl',
                        help='output dir')  # ehs = easy hard split
    parser.add_argument('--seed', type=int, default=42, help='random seed')

    return parser


if __name__ == '__main__':
    parser = parse_args()
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    if args.seed != -1:
        # Torch RNG
        torch.manual_seed(args.seed)
        torch.cuda.manual_seed(args.seed)
        torch.cuda.manual_seed_all(args.seed)
        # Python RNG
        np.random.seed(args.seed)
        random.seed(args.seed)

    with open(args.input_file, 'rt') as input_file:
        input_json = json.load(input_file)

    entries = []

    for idx in input_json.keys():
        for step_i in range(1, len(input_json[idx]['steps'])):
            step = input_json[idx]['steps'][step_i]
            question = ''
            for i in range(step_i + 1):
                for item in input_json[idx]['steps'][i]:
                    if 'step' in item:
                        question += ' ' + item['step']
            question += ' Now, what happens?'
            entry = {'id': f'{input_json[idx]["goal"]}|{step_i}',
                     'question': question.strip()}
            entries.append(entry)

    with jsonlines.open(args.output_file, mode='w') as writer:
        writer.write_all(entries)
