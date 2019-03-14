
from multiprocessing import cpu_count
# gunicorn 只适用于 Linux


bind="127.0.0.1:9000" #线上环境不会开启在公网IP下  一般使用内网IP
daemon=True  #是否开启守护进程
pidfile='logs/gunicorn.pid'

workers=cpu_count()*2 #工作进程数量

worker_class="gevent" #指定一个异步处理库
worker_connections=65535

keepalive=60
timeout=30
graceful_timeout=10
forwarded_allow_ips='*'

capture_output=True
loglevel='info'
errorlog='logs/error.log'


































