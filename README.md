# Overview
This repository contains the resources pertaining to the paper "Causal Reasoning of Entities and Events in Procedural Texts" and the dataset **C**ausal **R**easoning of **E**ntities and **E**vents in **P**rocedural Texts (CREPE).

# Files
- `data_dev_v2.json` is the development set of CREPE.
- `data_test_v2.json` is the test set of CREPE.
- `evaluate.py` is used to evaluate a model output. Usage : `python evaluate.py PATH_TO_OUTPUT` Example: `python evaluate.py codex/v1.2/data_dev_out_entity_and_event_atonce.json`

# Folders
- `/codex` contains variations of the Codex prompt and the code to run them. 
- `/gpt3` contains variations of the GPT3 prompt and the code to run them. 
- `/t5` contains variations of the T5 prompt and the code to run them. 
- `/naive` contains the naive baselines. 
- `/human_performance` contains the second-annotator's labels on the development set, and code to calculate the human performance. 
- `/strategyqa` contains the data from [StrategyQA](https://github.com/eladsegal/strategyqa) and the code to have it work with GPT3 (see details in the paper).
- `/openpi` contains the data from [OpenPI](https://github.com/allenai/openpi-dataset), the code to make inference with its accompanying GPT2 model, and the code to finetune and make inferene with a GPT3 model.
- `/codex_error_analysis` contains the code and results for the error anlysis of Codex.

# Citation
If you find our work useful, please cite
```
@inproceedings{zhang-etal-2023-causal,
  title = "Causal Reasoning of Entities and Events in Procedural Texts",
  author = "Zhang, Li  and
    Xu, Hainiu  and
    Yang, Yue  and
    Zhou, Shuyan  and
    You, Weiqiu  and
    Arora, Manni  and
    Callison-burch, Chris",
  booktitle = "Findings of the Association for Computational Linguistics: EACL 2023",
  month = may,
  year = "2023",
  address = "Dubrovnik, Croatia",
  publisher = "Association for Computational Linguistics",
  url = "https://aclanthology.org/2023.findings-eacl.31",
  pages = "415--431",
  abstract = "Entities and events are crucial to natural language reasoning and common in procedural texts. Existing work has focused either exclusively on entity state tracking (e.g., whether a pan is hot) or on event reasoning (e.g., whether one would burn themselves by touching the pan), while these two tasks are often causally related. We propose CREPE, the first benchmark on causal reasoning of event plausibility and entity states. We show that most language models, including GPT-3, perform close to chance at .35 F1, lagging far behind human at .87 F1. We boost model performance to .59 F1 by creatively representing events as programming languages while prompting language models pretrained on code. By injecting the causal relations between entities and events as intermediate reasoning steps in our representation, we further boost the performance to .67 F1. Our findings indicate not only the challenge that CREPE brings for language models, but also the efficacy of code-like prompting combined with chain-of-thought prompting for multihop event reasoning.",
}
```
