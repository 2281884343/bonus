# 💝 浪漫抽奖网站

一个精心设计的浪漫抽奖转盘网站，表面随机但实际上每次都能抽到礼物！

## ✨ 特性

- 🎯 **智能抽奖**: 表面看起来随机，实际上保证抽中三个大奖（大奖、二等奖、特别奖）
- 💕 **浪漫风格**: 精美的渐变色设计，简洁优雅的浪漫氛围
- 🎁 **不重复机制**: 每个奖品只会被抽中一次
- 💌 **爱意诗句**: 抽完三个奖品后，继续抽奖会收到浪漫的诗句和经典语句
- 🔧 **管理后台**: 方便的后台管理，可以查看状态和重置抽奖

## 📋 项目结构

```
bonus/
├── server.py          # Python Flask 后端服务器
├── requirements.txt   # Python 依赖配置
├── data.json          # 数据存储（自动生成）
├── README.md          # 说明文档
└── public/            # 前端文件
    ├── index.html     # 主抽奖页面
    ├── admin.html     # 管理后台
    ├── style.css      # 样式文件
    └── script.js      # 前端逻辑
```

## 🚀 快速开始

### 1. 安装 Python 依赖

确保你已安装 Python 3.7+，然后安装依赖：

```bash
pip install -r requirements.txt
```

### 2. 启动服务器

```bash
python server.py
```

服务器将在端口 **1314** 上运行（一生一世 💕）

### 3. 访问网站

- **抽奖页面**: http://localhost:1314
- **管理后台**: http://localhost:1314/admin.html

## 🎮 使用说明

### 抽奖页面

1. 打开抽奖页面
2. 点击中心的"开始抽奖"按钮
3. 转盘会旋转，停止后显示结果
4. 前三次抽奖保证获得：大奖、二等奖、特别奖
5. 之后的抽奖会显示浪漫的诗句

### 管理后台

1. 访问 http://localhost:5211314/admin.html
2. 查看当前抽奖状态（已抽取/剩余奖品）
3. 可以随时重置抽奖状态
4. 重置后所有奖品恢复到未抽取状态

## 🎨 设计特点

### 前端设计
- 渐变紫色背景（#667eea → #764ba2 → #f093fb）
- 简洁优雅的浪漫配色
- 流畅的转盘旋转动画
- 精美的结果弹窗展示
- 响应式设计，支持移动设备

### 后端逻辑
- Python Flask 轻量级框架
- JSON 文件存储，简单可靠
- RESTful API 设计
- 智能抽奖算法，确保完美体验

## 📡 API 接口

### 获取抽奖状态
```
GET /api/status
```

返回示例：
```json
{
  "drawnCount": 2,
  "totalPrizes": 3,
  "allPrizesDrawn": false
}
```

### 进行抽奖
```
POST /api/draw
```

返回示例（奖品）：
```json
{
  "success": true,
  "type": "prize",
  "result": "大奖",
  "message": "恭喜你抽中了大奖！"
}
```

返回示例（诗句）：
```json
{
  "success": true,
  "type": "poem",
  "result": "愿得一心人，白首不相离",
  "message": "送你一句情话~"
}
```

### 重置抽奖（管理后台）
```
POST /api/reset
```

### 获取详细信息（管理后台）
```
GET /api/admin/info
```

## 💡 工作原理

1. **奖品池**: 系统预设三个真实奖品（大奖、二等奖、特别奖）
2. **智能分配**: 前三次抽奖确保每次抽到一个不同的奖品
3. **诗句备份**: 抽完所有奖品后，返回浪漫的诗句和情话
4. **视觉欺骗**: 转盘上显示多个选项，但后端控制最终结果
5. **状态管理**: 通过 data.json 文件记录已抽取的奖品

## 🎁 自定义

### 修改奖品

编辑 `server.py` 中的 `prizes` 数组：

```python
'prizes': [
    {'id': 'grand', 'name': '你的奖品1', 'type': 'prize'},
    {'id': 'second', 'name': '你的奖品2', 'type': 'prize'},
    {'id': 'special', 'name': '你的奖品3', 'type': 'prize'}
]
```

### 修改诗句

编辑 `server.py` 中的 `poems` 数组，添加你喜欢的诗句或情话：

```python
'poems': [
    '你的情话1',
    '你的情话2',
    # ... 更多诗句
]
```

### 修改转盘选项

编辑 `public/script.js` 中的 `options` 数组，修改转盘显示的选项和颜色。

### 修改端口

编辑 `server.py` 中的 `PORT` 变量：

```python
PORT = 你的端口号
```

### 修改配色

编辑 `public/style.css` 中的背景渐变色：

```css
background: linear-gradient(135deg, #你的颜色1, #你的颜色2, #你的颜色3);
```

## 🔒 安全建议

1. 管理后台建议添加密码保护（可使用 Flask-Login）
2. 生产环境建议使用数据库（SQLite/MySQL）替代 JSON 文件
3. 建议添加访问日志记录
4. 生产环境请关闭 Flask 的 debug 模式

## 📦 依赖说明

- **Flask**: 轻量级 Python Web 框架
- **Flask-CORS**: 处理跨域请求

## 🛠️ 开发模式

Flask 内置开发服务器会自动重载代码更改：

```bash
python server.py
```

修改代码后，服务器会自动重启。

## 🚀 生产部署

### 使用 Gunicorn (推荐)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:1314 server:app
```

### 使用 Waitress (Windows)

```bash
pip install waitress
waitress-serve --host=0.0.0.0 --port=1314 server:app
```

## 🙏 致谢

用心设计，只为给 TA 一个惊喜！❤️

## 📄 许可

MIT License
