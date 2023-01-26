import argparse
import json
import jsonlines

import os
import torch
import random
import numpy as np
from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser()

    # paths and info
    parser.add_argument('--input-path', type=str, default='/Users/weiqiuyou/Documents/Penn/research/procedural-qa/openpi-dataset/data/gold',
                        help='input dir')
    parser.add_argument('--output-file', type=str, default='v2/gpt3/weiqiu1.0/ft_gpt3_on_openpi_data.jsonl',
                        help='output dir')
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

    question_filename = os.path.join(args.input_path, 'train', 'id_question.jsonl')
    answers_filename = os.path.join(args.input_path, 'train', 'id_answers.jsonl')
    with jsonlines.open(question_filename, 'r') as input_file:
        question_json = [obj for obj in input_file]
    with jsonlines.open(answers_filename, 'r') as input_file:
        answers_json = [obj for obj in input_file]

    entries = []

    for i in tqdm(range(len(question_json))):
        answers = 'There will be no change.' if len(answers_json[i]['answers']) == 0 else ', '.join(answers_json[i]['answers'])
        entry = {'prompt': question_json[i]['question'].strip() + '\n',
                 'completion': answers + '\n###\n'}
        entries.append(entry)

    with jsonlines.open(args.output_file, mode='w') as writer:
        writer.write_all(entries)
