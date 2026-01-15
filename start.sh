#!/bin/bash

# 激活虚拟环境
source venv/bin/activate

# 后台启动服务
nohup python3 server.py > lottery.log 2>&1 &

# 获取进程ID
PID=$!

# 保存进程ID到文件
echo $PID > lottery.pid

echo "服务已启动，进程ID: $PID"
echo "查看日志: tail -f lottery.log"
echo "停止服务: ./stop.sh"
