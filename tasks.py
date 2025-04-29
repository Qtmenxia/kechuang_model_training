from celery_app import app
import requests 
import re
# from to_doccano import upload_to_doccano
import json

@app.task(bind=True, max_retries=3)
def generate_warnings(self, params_list):
    results = []
    for idx, form_data in enumerate(params_list):
        try:
            # 调用原始生成逻辑（需改造为函数）
            warning_text = _generate_single_warning(form_data)
            results.append({
                "prompt": form_data,
                "response": warning_text,
                "status": "success"
            })
            # 可选：实时上传到Doccano
            # upload_to_doccano(form_data, warning_text)
            data = [{"prompt": form_data, "response": warning_text, "label": "待标注"}]
            with open("temp.jsonl", "a", encoding="utf-8") as f:
               for item in data:
                    f.write(json.dumps(item, ensure_ascii=False) + "\n")
        except Exception as e:
            self.retry(exc=e, countdown=2 ** idx)  # 指数退避重试
            results.append({
                "prompt": form_data,
                "error": str(e),
                "status": "failed"
            })
    return results

def _generate_single_warning(form_data):
    """生成单个提示词并获取模型响应的核心逻辑"""
    # 1. 参数解析
    gender = form_data.get('gender')
    speed = form_data.get('speed')
    added_key_value = {
        k: v for k, v in form_data.items()
        if k not in ['gender', 'character', 'speed', 'smoke', 'added_key', 'added_value', 'newkey']
    }

    # 2. 构建Prompt
    prompt_content = f"驾驶员性别: {gender}, 当前车速: {speed} km/h"
    if added_key_value:
        for key, value in added_key_value.items():
            prompt_content += f", {key}: {value}"
    prompt = (
    f"请为一位驾驶员生成一段个性化的、搞笑的、危险驾驶行为的提示文本。"
    f"下述特征源于车载摄像头拍摄的照片分析，特征是：{prompt_content}, "
    f"其中分别对应着：性别(gender)、当前车速(speed)、驾驶员是否抽烟(smoke)、"
    f"驾驶员是否接打电话(phone)、驾驶员是否玩手机(surf)、驾驶员是否闭眼(close_eyes)、"
    f"驾驶员是否疲劳(tired)、驾驶员是否分心(distracted)、驾驶员是否系安全带(belt)、"
    f"摄像头是否有图像(camera_image)、摄像头是否被遮挡(camera_cover)、"
    f"摄像头是否偏转(camera_deflection)、车辆是否超载(overcrowding)、"
    f"车辆是否超速(overspeeding)、乘客是否系安全带(passenger_belt)"
)

    # 3. 调用模型API
    url = "http://127.0.0.1:1234/v1/chat/completions"
    headers = {'Content-Type': 'application/json'}
    data = {
        "model": "llama-3-8b-sharegpt-112k.q2_k.gguf",
        "temperature": 0.7,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant..."},
            {"role": "user", "content": prompt}
        ]
    }

    # 4. 处理响应
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()  # 触发HTTP异常
    warning_text = response.json()['choices'][0]['message']['content']
    
    # 5. 清洗文本
    return re.sub(r'<.*?>', '', warning_text)