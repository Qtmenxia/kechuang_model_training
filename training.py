from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
import datasets

# 加载模型和分词器
model_name_or_path = "D:/deepseek0/deepseek1/deepseek2/Llama-3-8B-ShareGPT-112K.Q2_K.gguf"  # 替换成你的模型路径
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
model = AutoModelForCausalLM.from_pretrained(model_name_or_path)

# 加载你的训练数据
train_dataset = datasets.load_dataset('json', data_files='labled_data.jsonl', split='train')

# 快速编码
def preprocess(examples):
    return tokenizer(examples['prompt'], truncation=True, max_length=512, padding='max_length')

train_dataset = train_dataset.map(preprocess, batched=True)

# 定义训练参数
training_args = TrainingArguments(
    output_dir="D:/deepseek0/deepseek1",
    per_device_train_batch_size=4,
    num_train_epochs=3,
    logging_dir='./logs',
    logging_steps=10,
    save_total_limit=2,
    save_steps=500,
    fp16=True,
)

# 训练器
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
)

# 开始微调
trainer.train()
