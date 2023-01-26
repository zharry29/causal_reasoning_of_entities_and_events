import argparse
import json
import jsonlines

import os
import torch
import random
import numpy as np
import inflect

import pdb
from tqdm import tqdm

# I want to sear a steak.
# First, I start.
# Second, I set the steak at room temperature.
# Third, I heat the pan. Now the pan is more likely to be hot.
# Is it more likely or less likely that I touch the pan without getting burned?
# ###
# less likely


def lower_first(s):
    return s[0].lower() + s[1:]


def parse_args():
    parser = argparse.ArgumentParser()

    # paths and info
    parser.add_argument('--input-file', type=str, default='v2/openpi/weiqiu1.0/0hop-pred.json',
                        help='input dir')
    parser.add_argument('--output-file', type=str, default='v2/gpt3/weiqiu1.0/ft_gpt3_1hop_0hop_openpi_entities.jsonl',
                        help='output dir')  # ehs = easy hard split
    parser.add_argument('--entity-type', type=str, default='openpi_entity',
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

    p = inflect.engine()

    with open(args.input_file, 'rt') as input_file:
        input_json = json.load(input_file)

    entries = []

    for idx in input_json.keys():
        for step_i in range(1, len(input_json[idx]['steps'])):
            step = input_json[idx]['steps'][step_i]
            event_found = None
            for item in input_json[idx]['steps'][step_i]:
                if 'event' in item:
                    event_found = item
            if not event_found:
                continue
            prompt = ''
            prompt += f'I want to {lower_first(input_json[idx]["goal"])}\n'
            for i in range(step_i + 1):
                for item in input_json[idx]['steps'][i]:
                    if 'step' in item:
                        prompt += f'{p.number_to_words(p.ordinal(i + 1)).capitalize()}, I {lower_first(item["step"])}'
                for item in input_json[idx]['steps'][i]:
                    if 'type' in item and item['type'] == args.entity_type:
                        be = 'is' if p.singular_noun(item["entity"]) else 'are'
                        prompt += f' Then {item["entity"]} {be} {item["change"]} to be {item["attribute"]}.'
                prompt += '\n'
            event = event_found["event"] if event_found["event"][-1] != '.' else event_found["event"][:-1]
            prompt += f'Now, is it more likely or less likely that {event}?\n\n'

            entry = {'prompt': prompt,
                     'completion': f'{event_found["change"]}\n###\n'}
            entries.append(entry)

    with jsonlines.open(args.output_file, mode='w') as writer:
        writer.write_all(entries)
