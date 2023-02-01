GPT-3.5 (text-davinci-003) 

To run, use

```
python openai_models --data_path [path to CREPE dataset] --key [path to OpenAI API key]
```

After running, script will save a file in the `results` folder with name `gpt3_result_dict.pkl` which contains GPT-3 results stored as list of dictionaries. 

In addition, a confusion matrix named `conf_mtx.png` will be saved to the same folder.

---

Performance:

Development Set: __0.424__ (macro f1)

Testing Set: __0.423__ (macro f1)

