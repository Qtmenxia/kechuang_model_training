from tasks import generate_warnings
from tasks import _generate_single_warning
import requests
from flask import Flask, render_template, request, jsonify
import json
# from to_doccano import upload_to_doccano

app = Flask(__name__)

template_dirs=['./templates']

# app.jinja_environment.config['template_dirs'] = ['./templates', ]

@app.route('/')
def index():
    return render_template('index.html' , template_folder='templates')

@app.route('/start_batch', methods=['POST'])
def start_batch():
    print('start batch -- test')
    # 假设前端传递100组参数的JSON数组
    params_list = request.json.get('parameters', [])

    # print(params_list)
    
    # 分批次提交任务（防止内存溢出）
    batch_size = 10
    task_ids = []
    for i in range(0, len(params_list), batch_size):
        batch = params_list[i:i+batch_size]
        task = generate_warnings.delay(batch)
        task_ids.append(task.id)
    
    return jsonify({
        "message": f"已提交100个任务,任务ID:{task_ids}",
        "check_endpoint": "/get_results"
    })

if __name__ == '__main__':
    app.run(debug=True, port=1809)
    