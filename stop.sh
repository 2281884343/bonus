#!/bin/bash

if [ -f lottery.pid ]; then
    PID=$(cat lottery.pid)
    if ps -p $PID > /dev/null; then
        kill $PID
        echo "服务已停止，进程ID: $PID"
        rm lottery.pid
    else
        echo "进程不存在"
        rm lottery.pid
    fi
else
    echo "找不到 lottery.pid 文件"
    echo "尝试查找并停止所有 server.py 进程..."
    pkill -f "python.*server.py"
fi
