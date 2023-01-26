"""
Postprocess predictions for openpi to evaluate

{"id": "Sear a steak|1", "answers": ["temperature of food was cold before and hot afterwards",
"temperature of steak was room temperature before and heated afterwards", "temperature of stove was cold before and hot afterwards",
"temperature of temperature was unset before and set afterwards", "temperature of room was cold before and hot afterwards",
"power of thermostat was turned off before and turned on afterwards", "temperature of pot was cold before and hot afterwards",
"temperature of steel rod was cold before and hot afterwards", "temperature of pan was cold before and hot afterwards."]}

{
    "1": {
        "goal": "Sear a steak",
        "annotator": "Harry",
        "steps": [
            [
                {
                    "type": "step",
                    "step": "Start."
                }
            ],
            [
                {
                    "type": "step",
                    "step": "Set the steak at room temperature."
                }
            ],
            [
                {
                    "type": "step",
                    "step": "Heat the pan."
                },
                {
                    "type": "entity",
                    "entity": "the pan",
                    "attribute": "hot",
                    "change": "more likely"
                },
                {
                    "type": "multihop",
                    "event": "I touch the pan without getting burned.",
                    "change": "less likely"
                }
            ],
"""


import json
import jsonlines
from tqdm import tqdm
import pdb
import argparse

# from sentence_transformers import SentenceTransformer, util
# model = SentenceTransformer('all-MiniLM-L6-v2')


def parse_args():
    parser = argparse.ArgumentParser()

    # paths and info
    parser.add_argument('--input-file', type=str, default='v2/data_dev_v2.json',
                        help='input dir')
    parser.add_argument('--output-file', type=str, default='v2/openpi/weiqiu1.0/0hop-pred.json',
                        help='output file')
    parser.add_argument('--pred-file', type=str, default='v2/openpi/weiqiu1.0/0hop-predictions-formatted.jsonl',
                        help='prediction file')
    parser.add_argument('--seed', type=int, default=42, help='random seed')

    return parser


if __name__ == '__main__':
    parser = parse_args()
    args = parser.parse_args()

    with open(args.input_file, 'rt') as input_file:
        with open(args.output_file, 'wt') as output_file:
            annotation_dict = json.load(input_file)
            goal2idx = {}
            for key in tqdm(sorted(annotation_dict.keys(), key=lambda x: int(x))):
                goal2idx[annotation_dict[key]['goal']] = key
                # for step in annotation_dict[key]["steps"]:
                #     for j in range(len(step), -1, -1):
                #         if 'type' in step[j] and step[j]['type'] in ['entity', 'multihop']:
                #             step.pop(j)
            pred_dict = {}
            attr2question = {}
            prev_goal = None
            goal_idx = -1
            goals = sorted(annotation_dict.keys(), key=lambda x: int(x))

            with jsonlines.open(args.pred_file) as pred_file:
                for i, line in tqdm(enumerate(pred_file.iter())):
                    goal = line['id'].split('|')[0]
                    if prev_goal != goal:
                        goal_idx += 1
                    prev_goal = goal
                    step_i = int(line['id'].split('|')[1])

                    step = annotation_dict[goals[goal_idx]]["steps"][step_i]
                    # step = annotation_dict[goal2idx[goal]]["steps"][step_i]

                    answers = list(set(line['answers']))
                    # print('step_i', step_i, 'answers', answers)

                    if len(answers) == 1 and answers[0] == 'There will be no change.':
                        continue
                    else:
                        for answer in answers:
                            plural = False
                            # answer = answer.replace('.', '')
                            if ' was ' in answer:
                                answer_list = answer.split(' was ')
                            elif ' were ' in answer:
                                answer_list = answer.split(' were ')
                                plural = True
                            else:
                                if 'was' in answer:
                                    answer_list = answer.split('was')
                                elif 'were' in answer:
                                    answer_list = answer.split('were')
                                    plural = True
                                else:
                                    print(answer)
                                    continue

                            answer_list = [answer_list[0], ' '.join(answer_list[1:])]

                            attribute = answer_list[0].strip()
                            value_list = answer_list[1].split('before and')
                            before = value_list[0].strip()
                            afterwards = value_list[1].replace('afterwards.', '').replace('afterwards', '').strip()
                            step.append({
                                "type": "openpi_entity",
                                "entity": attribute.split('of')[-1].strip(),
                                "attribute": afterwards,
                                "change": "more likely"
                            })
                            step.append({
                                "type": "openpi_entity",
                                "entity": attribute.split('of')[-1].strip(),
                                "attribute": before,
                                "change": "less likely"
                            })
                    # print(step)
                    # exit()

            json.dump(annotation_dict, output_file, indent=4)
