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
  author = "Lyu, Qing  and
  Zhang, Li  and
  Callison-Burch, Chris",
  booktitle = "Findings of the Association for Computational Linguistics: EACL 2023",
  month = may,
  year = "2023",
  address = "Dubrovnik, Croatia",
  publisher = "Association for Computational Linguistics",
  url = "https://arxiv.org/pdf/2301.10896.pdf",
  abstract = "Entities and events have long been regarded as the crux of machine reasoning. Procedural texts have received increasing attention due to the dynamic nature of involved entities and events. Existing work has focused either on entity state tracking (e.g., the temperature of a pan) or on counterfactual event reasoning (e.g., how likely am I to burn myself by touching the pan), while these two tasks are tightly intertwined. In this work, we propose CREPE, the first benchmark on causal reasoning about event plausibility based on entity states. We experiment with strong large language models and show that most models, including GPT3, perform close to chance at .30 F1, lagging far behind the human performance of .87 F1. Inspired by the finding that structured representations such as programming languages benefits event reasoning as a prompt to code language models such as Codex, we creatively inject the causal relations between entities and events through intermediate variables and boost the performance to .67 to .72 F1. Our proposed event representation not only allows for knowledge injection, but also marks the first successful attempt of chain-of-thought reasoning with code language models.",
}
```
