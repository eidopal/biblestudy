"""
Vercel部署主入口文件
"""

import sys
import os

# 将项目根目录添加到Python路径
bible_app_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'bible_study_app')
sys.path.insert(0, bible_app_path)

# 导入应用
from web_app import create_app

# 创建应用实例
app = create_app()

# Vercel入口点 - 这行对Vercel不是必需的，但对本地测试有用
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 