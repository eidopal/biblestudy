from http.server import BaseHTTPRequestHandler
import json

# 极简的Vercel Serverless函数
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
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
                        <div class="alert alert-success">
                            <h4>成功!</h4>
                            <p>如果您能看到此页面，表示API函数已成功部署。</p>
                            <p>这是使用Vercel Serverless Functions模式部署的测试页面。</p>
                        </div>
                    </div>
                    <div class="card-footer text-center">
                        <p>Bible Study App &copy; 2023</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        self.wfile.write(html.encode()) 