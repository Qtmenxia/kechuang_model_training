// 新增批量生成函数（基于网页7的安全随机数生成）
function generateBatchParams(total = 100) {
    const batchParams = [];

    // 创建特征池（基于网页6的字符集扩展思想）
    const dynamicKeys = ['smoke', 'phone', 'surf', 'close_eyes', 'tired',
        'distracted', 'belt', 'camera_image', 'camera_cover',
        'camera_deflection', 'overcrowding', 'overspeeding',
        'passenger_belt'];

    for (let i = 0; i < total; i++) {
        // 生成随机特征（基于网页2的数学随机方法）
        const params = {
            gender: Math.random() > 0.5 ? '男性' : '女性',
            character: `驾驶员${i + 1}`, // 自动生成驾驶员编号
            speed: Math.floor(Math.random() * 160), // 0-160km/h随机车速
            added_key_value: {}
        };

        // 动态特征生成（基于网页6的随机键值对技术）
        dynamicKeys.forEach(key => {
            params.added_key_value[key] = Math.random() > 0.5 ? '是' : '否';
        });

        if (speed <= 20) {
            params.added_key_value['overspeeding'] = '否';
        }

        batchParams.push(params);
    }
    return batchParams;
}

// 修改提交事件监听器（适配网页11的API调用规范）
document.querySelector('#box5 button').addEventListener('click', async function () {
    document.getElementById('loading').style.display = 'block';

    try {
        // 生成100组参数（基于网页7的批量生成方案）
        const parameters = generateBatchParams(100);

        // 发送批量请求（符合start_batch接口要求）
        const response = await fetch('/start_batch', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ parameters })
        });

        const data = await response.json();
        if (data.task_ids) {
            // 启动进度监控（基于网页9的异步任务管理）
            monitorTasks(data.task_ids);
        }
    } catch (error) {
        console.error('批量提交失败:', error);
        document.getElementById('warning-text').textContent = `错误: ${error.message}`;
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
});

// 新增任务监控函数（参考网页10的状态跟踪机制）
function monitorTasks(taskIds) {
    taskIds.forEach(taskId => {
        const eventSource = new EventSource(`/get_results/${taskId}`);
        eventSource.onmessage = (e) => {
            const progress = JSON.parse(e.data);
            // 更新进度条显示（基于网页8的DOM操作）
            document.querySelector(`#task-${taskId} .progress`).style.width = `${progress.percentage}%`;
        };
    });
}