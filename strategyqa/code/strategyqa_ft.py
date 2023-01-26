#%%
import json

with open('/Users/seacow/Documents/GitHub/strategyqa/data/strategyqa/generated/transformer_qa_ORA-P_train_no_placeholders.json', 'r') as f:
    train_data = json.load(f)
f.close()
# %%
token_count = 0
finetune_lines = []
for d in train_data:
    prompt = ""
    completion = ""
    context = " ".join(d['facts'])
    prompt += f"Context: {context}\n"
    prompt += f"Question: {d['question']}\nTake it step by step:"
    for i, (decomp, decomp_ans) in enumerate(zip(d['decomposition'], d['step_answers'])):
        completion += f"#{i+1} {decomp}\n{decomp_ans}\n"
    completion += f"Therefore, the answer to the original question is {d['answer']}"
    finetune_lines.append({"prompt": prompt, "completion": completion})
    token_count += len(prompt.split())
    token_count += len(completion.split())

# %%
with open('/Users/seacow/School/UPenn/Research/Procedural Reasoning/v2/finetune/gpt3_ft_context.jsonl', 'w') as f:
    for l in finetune_lines:
        json.dump(l, f)
        f.write('\n')
# %%
for d in finetune_lines:
    print(d['prompt'])
    print(d['completion'])
    print('\n\n')
# %%
with open('/Users/seacow/School/UPenn/Research/Procedural Reasoning/v2/finetune/gpt3_ft_prepared.jsonl', 'r') as f:
    for l in f.readlines():
        data = json.loads(l)
        print(data['prompt'])
        print(data['completion'])
        print('\n\n')
# %%
