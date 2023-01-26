### Two-step approach

derived from `harry1.2`

First prompt Codex to generate event-related entity using `entity_prompt.py`

During inference time, prompt Codex to first deduce the state of the event-related entity at every step, append the predicted state, and then prompt Codex again to estimate the event likelihood.

---
Performance:
F1 Score: 0.59

