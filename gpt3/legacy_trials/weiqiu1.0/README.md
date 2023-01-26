Finetune GPT-3 to do what openpi does

## Dev

```
python v2/gpt3/weiqiu1.0/format_openpi_data_for_gpt3.py 

python v2/gpt3/weiqiu1.0/generate_openpi_answers_with_gpt3.py

python v2/gpt3/weiqiu1.0/postprocessing.py
```

## Test

```
python v2/openpi/weiqiu1.0/preprocessing.py --input-file v2/data_test_v2.json --output-file v2/openpi/weiqiu1.0/0hop_questions_test.jsonl

python v2/gpt3/weiqiu1.0/generate_openpi_answers_with_gpt3.py --questions-file v2/openpi/weiqiu1.0/0hop_questions_test.jsonl --answers-file v2/gpt3/weiqiu1.0/0hop-predictions-test-formatted.jsonl

python v2/gpt3/weiqiu1.0/postprocessing.py --input-file v2/data_test_v2.json --output-file v2/gpt3/weiqiu1.0/0hop-pred-test.json --pred-file v2/gpt3/weiqiu1.0/0hop-predictions-test-format

```