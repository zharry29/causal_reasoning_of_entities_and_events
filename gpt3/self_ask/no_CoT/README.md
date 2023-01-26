GPT-3 Using the _Self Ask_ Prompt: https://ofir.io/self-ask.pdf

This script use Self-Ask with **No Chain-of-Thought Prompting** 

To run, use

```
python openai_models --data_path [path to CREPE dataset] --key [path to OpenAI API key]
```

After running, script will save a file named `gpt3_result_dict.pkl` which contains GPT-3 results stored as list of dictionaries. 

In addition, a confusion matrix named `conf_mtx.png` will be saved to the same folder.