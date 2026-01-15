#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
浪漫抽奖网站 - Python Flask 后端
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os
from pathlib import Path

app = Flask(__name__, static_folder='public', static_url_path='')
CORS(app)

PORT = 1314 
DATA_FILE = 'data.json'

# 初始化数据
def init_data():
    """初始化抽奖数据"""
    default_data = {
        'drawnPrizes': [],  # 已抽取的奖项
        'prizes': [
            {'id': 'grand', 'name': '大奖', 'type': 'prize'},
            {'id': 'second', 'name': '二等奖', 'type': 'prize'},
            {'id': 'special', 'name': '特别奖', 'type': 'prize'}
        ],
        'poems': [
            '愿得一心人，白首不相离',
            '山有木兮木有枝，心悦君兮君不知',
            '玲珑骰子安红豆，入骨相思知不知',
            '一日不见兮，思之如狂',
            '执子之手，与子偕老',
            '愿我如星君如月，夜夜流光相皎洁',
            '身无彩凤双飞翼，心有灵犀一点通',
            '在天愿作比翼鸟，在地愿为连理枝',
            '此情可待成追忆，只是当时已惘然',
            '两情若是久长时，又岂在朝朝暮暮',
            '金风玉露一相逢，便胜却人间无数',
            '柔情似水，佳期如梦',
            '君问归期未有期，巴山夜雨涨秋池',
            '曾经沧海难为水，除却巫山不是云',
            '只愿君心似我心，定不负相思意',
            '一生一世一双人，半醉半醒半浮生',
            '情不知所起，一往而深',
            '你是我的独家记忆，我的甜蜜回忆',
            '余生很长，想和你在一起',
            '世间所有的相遇，都是久别重逢'
        ]
    }
    
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)
    
    return default_data

# 读取数据
def read_data():
    """读取抽奖数据"""
    try:
        if not os.path.exists(DATA_FILE):
            return init_data()
        
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f'读取数据失败: {e}')
        return init_data()

# 写入数据
def write_data(data):
    """写入抽奖数据"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f'写入数据失败: {e}')
        return False

# 路由：首页
@app.route('/')
def index():
    """返回主抽奖页面"""
    return send_from_directory('public', 'index.html')

# API：获取抽奖状态
@app.route('/api/status', methods=['GET'])
def get_status():
    """获取当前抽奖状态"""
    data = read_data()
    return jsonify({
        'drawnCount': len(data['drawnPrizes']),
        'totalPrizes': len(data['prizes']),
        'allPrizesDrawn': len(data['drawnPrizes']) >= len(data['prizes'])
    })

# API：抽奖
@app.route('/api/draw', methods=['POST'])
def draw():
    """执行抽奖"""
    import random
    
    data = read_data()
    
    # 检查是否还有奖品未抽取
    available_prizes = [
        prize for prize in data['prizes']
        if prize['id'] not in data['drawnPrizes']
    ]
    
    if available_prizes:
        # 还有奖品，返回一个未抽取的奖品
        prize = available_prizes[0]
        data['drawnPrizes'].append(prize['id'])
        write_data(data)
        
        return jsonify({
            'success': True,
            'type': 'prize',
            'result': prize['name'],
            'message': f'恭喜你抽中了{prize["name"]}！'
        })
    else:
        # 所有奖品已抽完，返回诗句
        random_poem = random.choice(data['poems'])
        return jsonify({
            'success': True,
            'type': 'poem',
            'result': random_poem,
            'message': '送你一句情话~'
        })

# API：重置抽奖
@app.route('/api/reset', methods=['POST'])
def reset():
    """重置抽奖状态"""
    data = read_data()
    data['drawnPrizes'] = []
    
    if write_data(data):
        return jsonify({
            'success': True,
            'message': '抽奖状态已重置'
        })
    else:
        return jsonify({
            'success': False,
            'message': '重置失败'
        }), 500

# API：管理后台 - 获取详细信息
@app.route('/api/admin/info', methods=['GET'])
def admin_info():
    """获取管理后台详细信息"""
    data = read_data()
    return jsonify({
        'drawnPrizes': data['drawnPrizes'],
        'prizes': data['prizes'],
        'allPrizesDrawn': len(data['drawnPrizes']) >= len(data['prizes'])
    })

if __name__ == '__main__':
    print('🎉 抽奖服务器启动中...')
    print(f'📱 前端页面: http://localhost:{PORT}')
    print(f'🔧 管理后台: http://localhost:{PORT}/admin.html')
    
    # 初始化数据
    init_data()
    
    # 启动服务器
    app.run(host='0.0.0.0', port=PORT, debug=True)
