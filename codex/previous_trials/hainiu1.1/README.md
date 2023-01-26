Based on current SOTA prompt `harry1.2`

Change:

First use Codex to generate `(entity, state)` pairs corresponding to an event.

During Inference:

1. Prompt Codex once to determine the state of `entity`
2. Add predicted `(entity, state)` to the prompt and call Codex again to answer the change of likelihood of the event.

---

### Usage

First run entity predictor 

```
python generate_entity.py
```

The outcome will be stored as `data_dev_v2_entity.json`

Then run event likelihood predictor

```
python openai_models.py
```

No argument required.

---

### Performance

Accuracy: 0.83

F1 Score: 0.64



