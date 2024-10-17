from flask import Flask, render_template
import sqlite3
from datetime import datetime
import pytz  # 引入 pytz 用于处理时区

app = Flask(__name__)

# 获取所有用户和最后一条消息，用于左侧列表
def get_users():
    conn = sqlite3.connect('chat_logs.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT user_id, username, message_text 
        FROM chat_logs 
        GROUP BY user_id 
        ORDER BY timestamp DESC
    ''')
    users = [{"user_id": row[0], "username": row[1], "last_message": row[2]} for row in cursor.fetchall()]
    conn.close()
    return users

# 获取特定用户的聊天记录，确保返回 user_id 和 username，并格式化日期和时间
def get_chat_by_user(user_id):
    conn = sqlite3.connect('chat_logs.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT user_id, username, message_text, bot_reply, timestamp 
        FROM chat_logs 
        WHERE user_id = ? 
        ORDER BY timestamp
    ''', (user_id,))
    chats = []
    taiwan_tz = pytz.timezone('Asia/Taipei')  # 台湾时区

    for row in cursor.fetchall():
        # 解析原始时间并转换为台湾时区
        utc_time = datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S')
        taiwan_time = utc_time.astimezone(taiwan_tz)
        
        # 格式化日期和时间
        formatted_date = taiwan_time.strftime('%Y年%m月%d日')
        formatted_time = taiwan_time.strftime('%H:%M:%S')
        
        chats.append({
            "user_id": row[0],
            "username": row[1],
            "message": row[2],
            "reply": row[3],
            "timestamp": formatted_time,  # 格式化后的时间
            "formatted_date": formatted_date  # 格式化后的日期
        })
    conn.close()
    return chats

@app.route('/')
def index():
    users = get_users()
    return render_template('index.html', users=users)

@app.route('/chat/<user_id>')
def chat(user_id):
    chats = get_chat_by_user(user_id)
    return render_template('chat_details.html', chats=chats)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)  # 设置为在所有接口上监听
