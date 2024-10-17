from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import json
import sqlite3
import datetime

# 从 config.json 读取配置
def load_config():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)

# 从 token.txt 读取 Telegram token
def load_token():
    with open("token.txt", "r", encoding="utf-8") as f:
        return f.read().strip()

config = load_config()
telegram_token = load_token()

# 从 config.json 加载关键词和模板
promotion_keywords = config["promotion_keywords"]
help_keywords = config["help_keywords"]
default_reply = config["default_reply"]
promotion_reply = config["templates"]["promotion_response"]
help_reply = config["templates"]["help_response"]
personal_telegram_reply = config["templates"]["personal_telegram"]

# 初始化数据库
def init_db():
    conn = sqlite3.connect('chat_logs.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            message_text TEXT,
            bot_reply TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# 记录聊天信息
def log_chat_to_db(user_id, username, message_text, bot_reply):
    conn = sqlite3.connect('chat_logs.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO chat_logs (user_id, username, message_text, bot_reply)
        VALUES (?, ?, ?, ?)
    ''', (user_id, username, message_text, bot_reply))
    conn.commit()
    conn.close()

# 用户意图状态字典
user_intent = {}

# 处理消息
async def handle_message(update: Update, context):
    user_id = update.message.from_user.id
    username = update.message.from_user.username or "Unknown"
    message_text = update.message.text

    # 判断用户意图，使用部分匹配关键词
    if any(keyword in message_text for keyword in promotion_keywords):
        bot_reply = promotion_reply
        user_intent[user_id] = "promotion"  # 更新用户意图状态
        await update.message.reply_text(bot_reply, parse_mode="Markdown", disable_web_page_preview=True)
    elif any(keyword in message_text for keyword in help_keywords):
        bot_reply = help_reply
        user_intent[user_id] = "help"  # 更新用户意图状态
        await update.message.reply_text(bot_reply, disable_web_page_preview=True)
    elif message_text.lower() == "个人电报":
        # 根据之前的意图状态提供“个人电报”回复
        if user_intent.get(user_id) == "promotion":
            bot_reply = personal_telegram_reply
            await update.message.reply_text(bot_reply, disable_web_page_preview=True)
        else:
            bot_reply = "该指令仅对合作商务用户开放。"
            await update.message.reply_text(bot_reply)
    else:
        bot_reply = default_reply
        await update.message.reply_text(bot_reply)

    # 记录聊天内容
    log_chat_to_db(user_id, username, message_text, bot_reply)

# 启动 Telegram 应用
async def start(update: Update, context):
    await update.message.reply_text("您好！我是您的客服助手，有什么可以帮您的吗？")

# 主函数
def main():
    init_db()  # 初始化数据库
    application = ApplicationBuilder().token(telegram_token).build()

    # 注册指令和消息处理器
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()
