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
    import random
    
    # 定义三个奖品
    prizes = [
        {'id': 'grand', 'name': '大奖', 'type': 'prize'},
        {'id': 'second', 'name': '二等奖', 'type': 'prize'},
        {'id': 'special', 'name': '特别奖', 'type': 'prize'}
    ]
    
    # 定义两次未获奖（情话）
    poems_draw = [
        {'id': 'poem1', 'name': '情话1', 'type': 'poem'},
        {'id': 'poem2', 'name': '情话2', 'type': 'poem'}
    ]
    
    # 合并并随机打乱顺序（5次抽奖机会）
    draw_sequence = prizes + poems_draw
    random.shuffle(draw_sequence)
    
    default_data = {
        'currentDrawIndex': 0,  # 当前抽奖次数
        'drawSequence': draw_sequence,  # 随机生成的抽奖顺序
        'totalDraws': 5,  # 总共5次抽奖机会
        'prizes': prizes,
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
    current_index = data.get('currentDrawIndex', 0)
    total_draws = data.get('totalDraws', 5)
    
    return jsonify({
        'drawnCount': current_index,
        'totalDraws': total_draws,
        'allDrawsUsed': current_index >= total_draws
    })

# API：抽奖
@app.route('/api/draw', methods=['POST'])
def draw():
    """执行抽奖"""
    import random
    
    data = read_data()
    
    # 检查并初始化 drawSequence（兼容旧数据）
    if 'drawSequence' not in data or not data.get('drawSequence'):
        # 重新初始化抽奖顺序
        prizes = data.get('prizes', [])
        poems_draw = [
            {'id': 'poem1', 'name': '情话1', 'type': 'poem'},
            {'id': 'poem2', 'name': '情话2', 'type': 'poem'}
        ]
        draw_sequence = prizes + poems_draw
        random.shuffle(draw_sequence)
        data['drawSequence'] = draw_sequence
        data['currentDrawIndex'] = 0
        data['totalDraws'] = 5
        write_data(data)
    
    current_index = data.get('currentDrawIndex', 0)
    total_draws = data.get('totalDraws', 5)
    draw_sequence = data.get('drawSequence', [])
    
    # 检查是否还有抽奖机会
    if current_index >= total_draws:
        # 所有机会已用完，返回随机诗句
        random_poem = random.choice(data['poems'])
        return jsonify({
            'success': True,
            'type': 'poem',
            'result': random_poem,
            'message': '抽奖次数已用完~'
        })
    
    # 获取当前应该抽到的结果
    current_draw = draw_sequence[current_index]
    
    # 更新抽奖次数
    data['currentDrawIndex'] = current_index + 1
    write_data(data)
    
    if current_draw['type'] == 'prize':
        # 抽到奖品
        return jsonify({
            'success': True,
            'type': 'prize',
            'result': current_draw['name'],
            'message': f'恭喜你抽中了{current_draw["name"]}！'
        })
    else:
        # 抽到情话
        random_poem = random.choice(data['poems'])
        return jsonify({
            'success': True,
            'type': 'poem',
            'result': random_poem,
            'message': '再试试吧~'
        })

# API：重置抽奖
@app.route('/api/reset', methods=['POST'])
def reset():
    """重置抽奖状态"""
    import random
    
    data = read_data()
    
    # 重新生成随机抽奖顺序
    prizes = data['prizes']
    poems_draw = [
        {'id': 'poem1', 'name': '情话1', 'type': 'poem'},
        {'id': 'poem2', 'name': '情话2', 'type': 'poem'}
    ]
    
    draw_sequence = prizes + poems_draw
    random.shuffle(draw_sequence)
    
    # 重置抽奖状态
    data['currentDrawIndex'] = 0
    data['drawSequence'] = draw_sequence
    
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
    current_index = data.get('currentDrawIndex', 0)
    total_draws = data.get('totalDraws', 5)
    draw_sequence = data.get('drawSequence', [])
    
    return jsonify({
        'currentDrawIndex': current_index,
        'totalDraws': total_draws,
        'drawSequence': draw_sequence,
        'prizes': data['prizes'],
        'allDrawsUsed': current_index >= total_draws
    })

if __name__ == '__main__':
    print('🎉 抽奖服务器启动中...')
    print(f'📱 前端页面: http://localhost:{PORT}')
    print(f'🔧 管理后台: http://localhost:{PORT}/admin.html')
    
    # 初始化数据
    init_data()
    
    # 启动服务器
    app.run(host='0.0.0.0', port=PORT, debug=True)
