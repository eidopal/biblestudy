"""
Vercel部署入口文件
"""

import sys
import os

# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入应用
from web_app import app, create_app

# 创建应用实例
app = create_app()

# Vercel入口点
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 