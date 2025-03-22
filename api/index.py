"""
Vercel部署主入口文件
"""

import sys
import os
import traceback

# 打印当前工作目录和Python路径，用于调试
print(f"Current Working Directory: {os.getcwd()}")
print(f"Python Path: {sys.path}")

try:
    # 计算bible_study_app的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    bible_app_path = os.path.join(parent_dir, 'bible_study_app')
    
    # 检查路径是否存在
    if os.path.exists(bible_app_path):
        print(f"Bible app path exists: {bible_app_path}")
    else:
        print(f"Bible app path does NOT exist: {bible_app_path}")
        # 尝试列出父目录内容以找到正确路径
        print(f"Contents of parent directory: {os.listdir(parent_dir)}")
    
    # 添加到Python路径
    sys.path.insert(0, parent_dir)
    sys.path.insert(0, bible_app_path)
    
    # 导入应用
    from bible_study_app.web_app import create_app
    
    # 创建应用实例
    app = create_app()
    
except Exception as e:
    print(f"Error during import: {e}")
    traceback.print_exc()
    
    # 创建一个简单的错误处理应用
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        return jsonify({
            "error": "Application initialization failed",
            "details": str(e),
            "traceback": traceback.format_exc()
        }), 500

# Vercel入口点
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 