// 配置
const API_BASE = '';

// 转盘选项（包括奖品和"谢谢参与"等选项）
const options = [
  { text: '大奖', color: '#FF6B6B', isPrize: true },
  { text: '谢谢参与', color: '#4ECDC4', isPrize: false },
  { text: '二等奖', color: '#FFE66D', isPrize: true },
  { text: '再接再厉', color: '#95E1D3', isPrize: false },
  { text: '特别奖', color: '#FF8C94', isPrize: true },
  { text: '下次努力', color: '#A8E6CF', isPrize: false },
  { text: '继续加油', color: '#C7CEEA', isPrize: false },
  { text: '差一点点', color: '#FFDAC1', isPrize: false }
];

let canvas, ctx;
let isSpinning = false;
let currentRotation = 0;

// 初始化
window.addEventListener('DOMContentLoaded', () => {
  canvas = document.getElementById('lottery-canvas');
  ctx = canvas.getContext('2d');
  
  drawWheel();
  
  // 绑定事件
  document.getElementById('draw-button').addEventListener('click', startDraw);
  document.getElementById('close-button').addEventListener('click', closeModal);
});

// 绘制转盘
function drawWheel(rotation = 0) {
  const centerX = canvas.width / 2;
  const centerY = canvas.height / 2;
  const radius = canvas.width / 2 - 10;
  const sliceAngle = (Math.PI * 2) / options.length;
  
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.save();
  ctx.translate(centerX, centerY);
  ctx.rotate(rotation);
  
  // 绘制每个扇形
  options.forEach((option, index) => {
    const startAngle = index * sliceAngle - Math.PI / 2;
    const endAngle = startAngle + sliceAngle;
    
    // 绘制扇形
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.arc(0, 0, radius, startAngle, endAngle);
    ctx.closePath();
    ctx.fillStyle = option.color;
    ctx.fill();
    
    // 绘制边框
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 3;
    ctx.stroke();
    
    // 绘制文字
    ctx.save();
    ctx.rotate(startAngle + sliceAngle / 2);
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillStyle = '#fff';
    ctx.font = 'bold 18px Microsoft YaHei';
    ctx.shadowColor = 'rgba(0, 0, 0, 0.3)';
    ctx.shadowBlur = 4;
    ctx.fillText(option.text, radius * 0.65, 0);
    ctx.restore();
  });
  
  // 绘制中心圆
  ctx.beginPath();
  ctx.arc(0, 0, 60, 0, Math.PI * 2);
  ctx.fillStyle = 'white';
  ctx.fill();
  ctx.strokeStyle = '#ff6b6b';
  ctx.lineWidth = 4;
  ctx.stroke();
  
  ctx.restore();
}

// 开始抽奖
async function startDraw() {
  if (isSpinning) return;
  
  const button = document.getElementById('draw-button');
  button.disabled = true;
  isSpinning = true;
  
  try {
    // 调用后端API
    const response = await fetch(`${API_BASE}/api/draw`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    const result = await response.json();
    
    if (result.success) {
      // 根据结果找到对应的选项索引
      let targetIndex;
      if (result.type === 'prize') {
        // 如果是奖品，找到对应的奖品选项
        targetIndex = options.findIndex(opt => opt.text === result.result);
      } else {
        // 如果是诗句，随机选择一个非奖品选项
        const nonPrizeIndices = options
          .map((opt, idx) => opt.isPrize ? -1 : idx)
          .filter(idx => idx !== -1);
        targetIndex = nonPrizeIndices[Math.floor(Math.random() * nonPrizeIndices.length)];
      }
      
      if (targetIndex === -1) {
        targetIndex = 1; // 默认选项
      }
      
      // 计算目标角度
      const sliceAngle = (Math.PI * 2) / options.length;
      // 转盘旋转，让目标选项的中心对准顶部指针
      // 目标扇形中心的角度偏移 = index * sliceAngle + sliceAngle/2
      // 需要旋转的角度让这个中心移到顶部（相对于初始-PI/2位置）
      const targetAngle = -(targetIndex * sliceAngle + sliceAngle / 2);
      
      // 旋转动画
      await spinWheel(targetAngle);
      
      // 显示结果
      showResult(result);
    }
  } catch (error) {
    console.error('抽奖失败:', error);
    alert('抽奖失败，请稍后重试');
  } finally {
    button.disabled = false;
    isSpinning = false;
  }
}

// 转盘旋转动画
function spinWheel(targetAngle) {
  return new Promise(resolve => {
    const spinDuration = 3000; // 3秒
    const extraSpins = 5; // 额外转5圈
    
    // 规范化目标角度到 0-2π 范围
    let normalizedTarget = targetAngle % (Math.PI * 2);
    if (normalizedTarget < 0) normalizedTarget += Math.PI * 2;
    
    // 计算从当前角度到目标角度需要旋转的角度
    let angleDiff = normalizedTarget - (currentRotation % (Math.PI * 2));
    if (angleDiff < 0) angleDiff += Math.PI * 2;
    
    // 总旋转 = 额外的圈数 + 到达目标的角度
    const totalRotation = Math.PI * 2 * extraSpins + angleDiff;
    const startTime = Date.now();
    const startRotation = currentRotation;
    
    function animate() {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / spinDuration, 1);
      
      // 使用缓动函数
      const easeOut = 1 - Math.pow(1 - progress, 3);
      const rotation = startRotation + totalRotation * easeOut;
      
      drawWheel(rotation);
      
      if (progress < 1) {
        requestAnimationFrame(animate);
      } else {
        currentRotation = startRotation + totalRotation;
        resolve();
      }
    }
    
    animate();
  });
}

// 显示结果
function showResult(result) {
  const modal = document.getElementById('result-modal');
  const title = document.getElementById('result-title');
  const message = document.getElementById('result-message');
  const icon = document.querySelector('.result-icon');
  
  if (result.type === 'prize') {
    icon.textContent = '🎁';
    title.textContent = result.result;
    message.textContent = result.message;
  } else {
    icon.textContent = '✨';
    title.textContent = result.result;
    message.textContent = '';
  }
  
  modal.classList.add('show');
}

// 关闭弹窗
function closeModal() {
  const modal = document.getElementById('result-modal');
  modal.classList.remove('show');
}
