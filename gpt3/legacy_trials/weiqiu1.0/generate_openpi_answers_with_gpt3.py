import json
import jsonlines
import openai
import os
from tqdm import tqdm
import argparse

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_answers_with_gpt3(question):
    response = openai.Completion.create(
        model="babbage:ft-ccb-lab-members-2022-10-07-20-19-31",
        prompt=question.strip() + '\n',
        temperature=0,
        max_tokens=256,
        top_p=1,
        stop=['###'],
        frequency_penalty=0,
        presence_penalty=0
    )
    return response['choices'][0]['text']



def parse_args():
    parser = argparse.ArgumentParser()

    # paths and info
    parser.add_argument('--questions-file', type=str, default='v2/openpi/weiqiu1.0/0hop_questions.jsonl',
                        help='input dir')
    parser.add_argument('--answers-file', type=str, default='v2/gpt3/weiqiu1.0/0hop-predictions-formatted.jsonl',
                        help='output dir')
    parser.add_argument('--seed', type=int, default=42, help='random seed')

    return parser


if __name__ == '__main__':
    parser = parse_args()
    args = parser.parse_args()

    questions_path = args.questions_file
    answers_path = args.answers_file

    with jsonlines.open(questions_path, 'r') as input_file:
        question_json = [obj for obj in input_file]

    answers_json = []

    for q in tqdm(question_json):
        answers = get_answers_with_gpt3(q['question'])
        answers_json.append({'id': q['id'],
                             'answers': [answer.strip() for answer in answers.split(',')]})

    with jsonlines.open(answers_path, mode='w') as writer:
        writer.write_all(answers_json)