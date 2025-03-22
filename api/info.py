from http.server import BaseHTTPRequestHandler
import json
import sys
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        info = {
            "python_version": sys.version,
            "working_directory": os.getcwd(),
            "path": sys.path,
            "environment": {k: v for k, v in os.environ.items() if not k.startswith('_')},
            "vercel": True
        }
        
        # 获取目录结构
        try:
            base_dir = os.getcwd()
            dirs = []
            files = []
            
            # 列出当前目录内容
            for item in os.listdir(base_dir):
                if os.path.isdir(os.path.join(base_dir, item)):
                    dirs.append(item)
                else:
                    files.append(item)
                    
            info["directory_structure"] = {
                "base_directory": base_dir,
                "directories": dirs,
                "files": files
            }
        except Exception as e:
            info["directory_error"] = str(e)
        
        self.wfile.write(json.dumps(info, indent=2).encode()) 