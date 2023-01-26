# Usage
`python openai_models.py --prompt event_only`
`python openai_models.py --prompt entity_and_event`
`python openai_models.py --prompt entity_and_event --gold_entity`

Each of these outputs a `.json` file, which should then be evaluated using `/v2/evaluate.py`.

# Change Log
Compared to 1.2, in the entity+event prompt, the entity-attribute-change tuple now has a "soft representation" as a sentence.

# Result
