# Usage

Modified from `harry1.2`. Prompt Codex for each event independently. Hence, Codex only need to predict one entity states and the likelihood of one event at a given step.

Further, the golden entity is not provided in __init__, Codex needs to predict the event-related entity

__F1 Score__: 0.32