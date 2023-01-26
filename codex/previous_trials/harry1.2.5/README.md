# Usage
`python openai_models.py --prompt event_only`
`python openai_models.py --prompt entity_and_event`
`python openai_models.py --prompt entity_and_event --gold_entity`

Each of these outputs a `.json` file, which should then be evaluated using `/v2/evaluate.py`.

# Change Log
Init instead of __init__

# Result