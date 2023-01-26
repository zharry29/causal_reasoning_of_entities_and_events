# Usage
`python openai_models.py --prompt event_only`
`python openai_models.py --prompt entity_and_event`
`python openai_models.py --prompt entity_and_event --gold_entity`

Each of these outputs a `.json` file, which should then be evaluated using `/v2/evaluate.py`.

# Change Log
Compared to 1.2, the `entity_and_event` setting now explicity outputsa logical relation between the predicted entity change and event change (either entailment or negation). The application of this logic relation is enforced.