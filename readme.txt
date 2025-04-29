安装redis
pip install redis

安装这个
pip install eventlet

启动redis服务
PS D:\proj\redis> .\redis-server.exe

启动celery
python -m celery -A tasks.app worker --loglevel=info -P eventlet

启动app
python.exe .\flask_change.py

应该就可以了