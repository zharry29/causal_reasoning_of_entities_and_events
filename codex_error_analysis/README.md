## Usage of Codes for Entity Quality Evaluation

1. To label data, run

```
python label_entity.py --output_path [path to Codex result]
```

The resulting labled data will be save to the `data` folder

The schema for data labeling prompt is

```
[current step]

[events]

[(entity, state, bool)]
```

There will be two questions: 

	1. related (whether entity state is related to any of the event)
	1. Correct (whether the predicted entity state is correct)

---

To get test statistics on labeled data, run

```
python evaluate.py --data_path [path to labeled data]
```

