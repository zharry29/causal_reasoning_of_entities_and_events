# Overview
The Codex prompts discussed in the paper are shown here. Each folder represents a variation. **In each folder**, the usage is: `python openpi_models.py --prompt PROMPT --split SPLIT [--gold_entity] [--at_once] --key KEY`, where
- PROMPT is either `event_only` (without chain-of-thought) or `entity_and_event` (with entities as chain-of-thought)
- SPLIT is either `dev` or `test`
- `--gold_entity` is specified if ground truth entity change labels are provided. If specified, then `--at_once` must not be specified, since entity change labels must be provided step by step.
- `--at_once` should always be specified if `--gold_entity` is NOT specified, to save computation resources.
- KEY lets the script look for an OpenPI API-KEY file in `/api_keys/KEY.key`

Runing the above command produces an output `.json` file in the folder of the variation, which can be evaluated using `/evaluate.py`.

In each folder, the `/prompt` folder contains the 3 in-context examples for both the `event_only` and `entity_and_event` settings. For some variations, only one is possible.