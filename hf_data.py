from datasets import Dataset
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# 读取Doccano导出的JSONL
df = pd.read_json("labeled_data.jsonl", lines=True)

# 转换为Hugging Face Dataset
dataset = Dataset.from_pandas(df)
dataset = dataset.map(lambda x: {"text": x["text"], "label": x["labels"][0]})

# 划分训练集/验证集
dataset = dataset.train_test_split(test_size=0.1)

# 标签编码
label_encoder = LabelEncoder()
dataset = dataset.map(lambda x: {"label_id": label_encoder.fit_transform([x["label"]])[0]})

# 构建Prompt模板（适配Llama风格）
# 修改原有prompt模板为Llama3指令格式
prompt_template = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>
你是一个中文文本分类专家，请从以下类别中选择最合适的标签：{options}<|eot_id|>
<|start_header_id|>user<|end_header_id|>
文本内容：{text}<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
分类结果："""

# 应用模板
dataset = dataset.map(lambda x: {"prompt": prompt_template.format(
    text=x["text"],
    options=" ".join(label_encoder.classes_)
)})