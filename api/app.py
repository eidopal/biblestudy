from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Bible Study App</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { 
                font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
                background-color: #f8f9fa;
            }
            .container { 
                max-width: 800px; 
                margin-top: 50px; 
            }
            .card {
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                border-radius: 0.5rem;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h2 class="text-center">圣经学习应用</h2>
                </div>
                <div class="card-body">
                    <div class="alert alert-info">
                        <h4>应用正在加载中...</h4>
                        <p>我们正在努力部署应用。如果您看到此页面，表示基本服务已启动，但完整应用尚未加载。</p>
                        <p>请检查控制台日志以获取更多信息。</p>
                    </div>
                    <div class="mt-4">
                        <h5>系统信息:</h5>
                        <pre id="sysinfo" class="bg-light p-3"></pre>
                    </div>
                </div>
                <div class="card-footer text-center">
                    <p>Bible Study App &copy; 2023</p>
                </div>
            </div>
        </div>
        
        <script>
            // 获取系统信息
            fetch('/api/info')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('sysinfo').textContent = JSON.stringify(data, null, 2);
                })
                .catch(err => {
                    document.getElementById('sysinfo').textContent = "无法获取系统信息: " + err;
                });
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/api/info')
def info():
    import sys
    import os
    
    info = {
        "python_version": sys.version,
        "working_directory": os.getcwd(),
        "python_path": sys.path,
        "environment": {k: v for k, v in os.environ.items() if not k.startswith('_')},
        "request_headers": dict(request.headers)
    }
    
    # 获取目录结构
    base_dir = os.getcwd()
    structure = {"base_dir": base_dir, "files": []}
    
    for root, dirs, files in os.walk(base_dir, topdown=True, followlinks=False):
        # 限制深度和文件数以避免响应过大
        rel_dir = os.path.relpath(root, base_dir)
        if rel_dir.count(os.sep) > 3 or len(structure["files"]) > 100:
            continue
            
        for file in files:
            rel_path = os.path.join(rel_dir, file)
            structure["files"].append(rel_path)
    
    info["file_structure"] = structure
    
    return jsonify(info)

if __name__ == "__main__":
    app.run(debug=True) 