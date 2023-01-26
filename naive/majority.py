import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--split', type=str, default='dev', help='Either dev or test set.')

args = parser.parse_args()

with open(f'../data_{args.split}_v2.json') as f:
    jobj = json.load(f)
    jout = jobj.copy()

outfile = f'data_{args.split}_out_majority.json'
with open(outfile,'w') as fw:
    json.dump(jout, fw, indent=4)