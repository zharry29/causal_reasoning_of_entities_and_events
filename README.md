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