# Usage
`python openai_models.py --prompt event_only`
`python openai_models.py --prompt entity_and_event`
`python openai_models.py --prompt entity_and_event --gold_entity`

Each of these outputs a `.json` file, which should then be evaluated using `/v2/evaluate.py`.

# Change Log
Predict step by step instead of all steps
Provide gold state changes

Use more likely, less unlikely, equally likely as ternary labels
Remove fuel car example

# Result
event_only: .59
entity_and_event: .65
gold_entity_and_event: .74