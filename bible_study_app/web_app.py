"""
Web application for Bible Study
This provides a web interface for viewing daily Bible reading and memorization.
"""

import os
import json
import datetime
import secrets
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from bible_data import format_reference, ALL_BOOKS, get_book_chapters
from bible_api import get_verse
from study_plan import StudyPlan

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'bible-study-app-secret-key')

# 添加用户登录管理
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = '请先登录以访问此页面'

# 数据目录
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(DATA_DIR, exist_ok=True)
USERS_FILE = os.path.join(DATA_DIR, 'users.json')

# 用户类
class User(UserMixin):
    def __init__(self, id, username, password_hash, is_admin=False):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.is_admin = is_admin

# 用户存储
users = {}
# 初始管理员用户（如果用户文件不存在）
default_admin = {
    '1': {
        'username': 'admin',
        'password_hash': generate_password_hash('admin'),
        'is_admin': True
    }
}

# 加载用户
def load_users():
    global users
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                users = json.load(f)
        except:
            users = default_admin
    else:
        users = default_admin
        save_users()

# 保存用户
def save_users():
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

# 加载用户
load_users()

# 用户加载回调
@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        user_data = users[user_id]
        return User(
            id=user_id,
            username=user_data['username'],
            password_hash=user_data['password_hash'],
            is_admin=user_data.get('is_admin', False)
        )
    return None

# 管理员权限装饰器
def admin_required(func):
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('需要管理员权限才能访问此页面', 'danger')
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# Initialize the study plan
study_plan = StudyPlan()

# Add current year to all templates
@app.context_processor
def inject_now():
    return {'now': datetime.datetime.now()}

# 登录页面
@app.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user_id = None
        for uid, user_data in users.items():
            if user_data['username'] == username:
                user_id = uid
                break
                
        if user_id and check_password_hash(users[user_id]['password_hash'], password):
            user = User(
                id=user_id,
                username=users[user_id]['username'],
                password_hash=users[user_id]['password_hash'],
                is_admin=users[user_id].get('is_admin', False)
            )
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('index'))
        else:
            flash('用户名或密码不正确', 'danger')
            
    return render_template('login.html')

# 退出登录
@app.route('/logout')
@login_required
def logout():
    """用户退出登录"""
    logout_user()
    flash('您已成功退出登录', 'success')
    return redirect(url_for('index'))

# 用户注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册"""
    # 只有管理员可以注册新用户
    if not current_user.is_authenticated or not current_user.is_admin:
        flash('只有管理员可以注册新用户', 'danger')
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        is_admin = 'is_admin' in request.form
        
        # 检查用户名是否已存在
        for user_data in users.values():
            if user_data['username'] == username:
                flash('用户名已存在', 'danger')
                return render_template('register.html')
                
        # 创建新用户
        user_id = str(len(users) + 1)
        users[user_id] = {
            'username': username,
            'password_hash': generate_password_hash(password),
            'is_admin': is_admin
        }
        save_users()
        
        flash(f'用户 {username} 已成功创建', 'success')
        return redirect(url_for('index'))
        
    return render_template('register.html')

@app.route('/')
def index():
    """Render the main page with daily Bible content."""
    # Get current time and day of year
    current_time = datetime.datetime.now()
    day_of_year = current_time.timetuple().tm_yday
    
    # Format date and time
    date_str = current_time.strftime("%Y年%m月%d日")
    time_str = current_time.strftime("%H:%M:%S")
    
    # Get reading passages
    reading_passages = study_plan.get_daily_reading_passages()
    
    # Get memorization verse for today
    verse_dict = study_plan.get_daily_memorization_verses()
    mem_ref = ""
    mem_text = ""
    has_custom_text = False
    verse_index = -1
    
    if verse_dict:
        try:
            book = verse_dict['book']
            chapter = verse_dict['chapter']
            verse_start = verse_dict['verse_start']
            verse_end = verse_dict['verse_end']
            
            if verse_end:
                mem_ref = f"{book} {chapter}:{verse_start}-{verse_end}"
            else:
                mem_ref = f"{book} {chapter}:{verse_start}"
            
            # Check if we have custom text first
            custom_text = verse_dict.get('custom_text', '')
            if custom_text:
                mem_text = custom_text
                has_custom_text = True
            else:
                # Try to get verse text from API or cache
                mem_text = get_verse(book, chapter, verse_start, verse_end)
            
            # Get verse index for editing
            all_verses = study_plan.get_all_memorization_verses()
            for i, verse in enumerate(all_verses):
                if (verse['book'] == book and 
                    verse['chapter'] == chapter and 
                    verse['verse_start'] == verse_start and 
                    verse['verse_end'] == verse_end):
                    verse_index = i
                    break
                
            # Ensure we have text content
            if not mem_text:
                mem_text = f"获取 {mem_ref} 内容时出现问题，请稍后再试。"
        except Exception as e:
            mem_ref = "读取经文时出现错误"
            mem_text = f"应用程序出现问题：{str(e)}"
    else:
        mem_ref = "未设置背诵经文"
        mem_text = "请在设置页面添加经文进行背诵。"
    
    return render_template(
        'index.html',
        date=date_str,
        time=time_str,
        day_of_year=day_of_year,
        reading_passages=reading_passages,
        mem_ref=mem_ref,
        mem_text=mem_text,
        has_custom_text=has_custom_text,
        verse_index=verse_index
    )

@app.route('/settings')
@login_required
@admin_required
def settings():
    """Render the settings page. Requires admin privileges."""
    # Get all Bible books for dropdowns
    old_testament = ALL_BOOKS[:39]  # First 39 books are Old Testament
    new_testament = ALL_BOOKS[39:]  # Rest are New Testament
    
    # Get current reading passages and memorization verses
    reading_passages = study_plan.get_all_reading_passages()
    memorization_verses = study_plan.get_all_memorization_verses()
    
    return render_template(
        'settings.html',
        old_testament=old_testament,
        new_testament=new_testament,
        reading_passages=reading_passages,
        memorization_verses=memorization_verses
    )

@app.route('/api/chapters/<book>')
def get_chapters(book):
    """API endpoint to get chapters for a given book."""
    num_chapters = get_book_chapters(book)
    chapters = list(range(1, num_chapters + 1))
    return jsonify(chapters)

@app.route('/api/add_reading', methods=['POST'])
@login_required
@admin_required
def add_reading():
    """API endpoint to add a reading passage. Requires admin privileges."""
    data = request.form
    book = data.get('book')
    chapter = int(data.get('chapter'))
    
    success = study_plan.add_reading_passage(book, chapter)
    
    return jsonify({
        'success': success,
        'message': f"已添加 {book} {chapter} 到阅读计划" if success else "无法添加阅读章节，可能已存在或是无效章节"
    })

@app.route('/api/remove_reading/<int:index>', methods=['POST'])
@login_required
@admin_required
def remove_reading(index):
    """API endpoint to remove a reading passage. Requires admin privileges."""
    success = study_plan.remove_reading_passage(index)
    
    return jsonify({
        'success': success,
        'message': "已从阅读计划中删除所选章节" if success else "无法删除所选章节"
    })

@app.route('/api/add_memorization', methods=['POST'])
@login_required
@admin_required
def add_memorization():
    """API endpoint to add a memorization verse. Requires admin privileges."""
    data = request.form
    book = data.get('book')
    chapter = int(data.get('chapter'))
    verse_start = int(data.get('verse_start'))
    verse_end = data.get('verse_end')
    custom_text = data.get('custom_text', '')
    
    # Convert verse_end to int if it exists
    if verse_end and verse_end.strip():
        verse_end = int(verse_end)
    else:
        verse_end = None
    
    success = study_plan.add_memorization_verse(book, chapter, verse_start, verse_end, custom_text)
    
    msg = ""
    if success:
        if verse_end:
            msg = f"已添加 {book} {chapter}:{verse_start}-{verse_end} 到背诵计划"
        else:
            msg = f"已添加 {book} {chapter}:{verse_start} 到背诵计划"
    else:
        msg = "无法添加背诵经文，可能是无效章节或经节"
    
    return jsonify({
        'success': success,
        'message': msg
    })

@app.route('/api/remove_memorization/<int:index>', methods=['POST'])
@login_required
@admin_required
def remove_memorization(index):
    """API endpoint to remove a memorization verse. Requires admin privileges."""
    success = study_plan.remove_memorization_verse(index)
    
    return jsonify({
        'success': success,
        'message': "已从背诵计划中删除所选经文" if success else "无法删除所选经文"
    })

@app.route('/update_time')
def update_time():
    """API endpoint to get the current time."""
    current_time = datetime.datetime.now()
    time_str = current_time.strftime("%H:%M:%S")
    return jsonify({'time': time_str})

@app.route('/api/update_verse_text', methods=['POST'])
@login_required
@admin_required
def update_verse_text():
    """API endpoint to update the custom text for a verse. Requires admin privileges."""
    data = request.form
    index = int(data.get('index'))
    custom_text = data.get('custom_text', '')
    
    success = study_plan.update_verse_text(index, custom_text)
    
    return jsonify({
        'success': success,
        'message': "已更新经文内容" if success else "无法更新经文内容"
    })

def create_app():
    """Create and configure the Flask app."""
    # Create template and static directories if they don't exist
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'), exist_ok=True)
    
    return app

if __name__ == '__main__':
    create_app()
    # 在生产环境中，应该使用 app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))