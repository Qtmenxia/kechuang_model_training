import json
import pandas as pd

def json_to_txt(input_file, output_file, delimiter='|||'):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = [json.loads(line) for line in f]

    with open(output_file, 'w', encoding='utf-8') as f:
        for item in data:
            text = item['text'].replace('\n', ' ')  # 清理换行符[2](@ref)
            label = item['labels'][0] if isinstance(item['labels'], list) else item['labels']
            f.write(f"{text}{delimiter}{label}\n")

json_to_txt('labeled_data.jsonl', 'training_data.txt')
