To run, use

```
python t5.py model split
```

`model` could be `t5` or `t0` and `split` could be `dev` or `test`.

The output will be saved to a json file named as `data_{split}_out_{model}.json`.

To evaluate the results, navigate to the upper folder and run

```
python evaluate.py data_{split}_out_{model}.json
```

#### Result

T5: dev: 0.3430, test: 0.3356
T0: dev: 0.3427, test: 0.3373