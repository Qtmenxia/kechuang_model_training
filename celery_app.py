from celery import Celery

app = Celery('tasks', broker='redis://127.0.0.1:6379/0', backend='redis://127.0.0.1:6379/0')

# 配置任务重试策略
app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='Asia/Shanghai',
    enable_utc=True,
    task_annotations={
        'tasks.generate_warnings': {'rate_limit': '10/s'}  # 限流控制
    }
)