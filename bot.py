import telebot
from telebot import types
import sqlite3
import os
from flask import Flask, request, jsonify
import threading

# قراءة التوكن من إعدادات Render
BOT_TOKEN = os.environ.get('BOT_TOKEN', 'ضع_التوكن_هنا_كاحتياط')
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# إعداد قاعدة البيانات
def init_db():
    conn = sqlite3.connect('zideot.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY, 
                  balance REAL DEFAULT 0.0, 
                  referrals INTEGER DEFAULT 0,
                  referrer_id INTEGER DEFAULT NULL)''')
    conn.commit()
    conn.close()

init_db()

def get_user(user_id):
    conn = sqlite3.connect('zideot.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def create_user(user_id, referrer_id=None):
    conn = sqlite3.connect('zideot.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, referrer_id) VALUES (?, ?)", (user_id, referrer_id))
    conn.commit()
    conn.close()

def add_points(user_id, amount):
    conn = sqlite3.connect('zideot.db')
    c = conn.cursor()
    c.execute("UPDATE users SET balance = balance + ? WHERE user_id=?", (amount, user_id))
    conn.commit()
    conn.close()

def add_referral(referrer_id):
    conn = sqlite3.connect('zideot.db')
    c = conn.cursor()
    c.execute("UPDATE users SET referrals = referrals + 1 WHERE user_id=?", (referrer_id,))
    c.execute("SELECT referrals FROM users WHERE user_id=?", (referrer_id,))
    refs = c.fetchone()[0]
    if refs % 100 == 0:
        c.execute("UPDATE users SET balance = balance + 1.0 WHERE user_id=?", (referrer_id,))
    conn.commit()
    conn.close()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    args = message.text.split()
    
    user = get_user(user_id)
    if not user:
        referrer_id = None
        if len(args) > 1:
            try:
                referrer_id = int(args[1])
                if referrer_id != user_id:
                    add_referral(referrer_id)
            except:
                pass
        create_user(user_id, referrer_id)
        user = get_user(user_id)

    balance = user[1] if user else 0.0
    referrals = user[2] if user else 0

    markup = types.InlineKeyboardMarkup()
    # الرابط هيتم تحديثه لرابط Render
    btn_app = types.InlineKeyboardButton(
        text="🔥 فتح التطبيق ومشاهدة الإعلانات", 
        web_app=types.WebAppInfo(url=f"https://zideot-tron-karim.netlify.app/?balance={balance}&refs={referrals}&user_id={user_id}") 
    )
    btn_balance = types.InlineKeyboardButton("💳 عرض رصيدي الحالي", callback_data="check_balance")
    btn_refs = types.InlineKeyboardButton("👥 عرض إحالاتي", callback_data="check_refs")
    
    bot_info = bot.get_me()
    ref_link = f"https://t.me/{bot_info.username}?start={user_id}"
    btn_share = types.InlineKeyboardButton(
        text="🎁 رابط الإحالة الخاص بك", 
        url=f"https://t.me/share/url?url={ref_link}&text=اربح معي من Zideot Tron!"
    )
    
    markup.add(btn_app)
    markup.add(btn_balance, btn_refs)
    markup.add(btn_share)

    welcome_text = (
        f"👋 **أهلاً بك في Zideot Tron!** 🚀\n\n"
        f"🌟 مرحباً بك في منصة الأرباح الأسرع!\n\n"
        f"⚡️ **ملاحظة:** كل 100 إعلان تعادل 1.0000000 TRX\n"
        f"👥 **الإحالات:** كل 100 إحالة تعادل 1.0000000 TRX\n\n"
        f"👇 اضغط على الأزرار أدناه للبدء:"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check_balance")
def callback_balance(call):
    user_id = call.from_user.id
    user = get_user(user_id)
    balance = user[1] if user else 0.0
    bot.answer_callback_query(call.id, f"💎 رصيدك الحالي: {balance:.7f} TRX", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "check_refs")
def callback_refs(call):
    user_id = call.from_user.id
    user = get_user(user_id)
    refs = user[2] if user else 0
    bot.answer_callback_query(call.id, f"👥 عدد إحالاتك: {refs}\n\n(كل 100 إحالة = 1.0000000 TRX)", show_alert=True)

# ===== مسار الـ API =====
@app.route('/api/add_points', methods=['POST'])
def api_add_points():
    try:
        data = request.json
        user_id = int(data.get('user_id'))
        amount = float(data.get('amount', 0.01))
        
        add_points(user_id, amount)
        user = get_user(user_id)
        new_balance = user[1]
        
        markup = types.InlineKeyboardMarkup()
        btn_balance = types.InlineKeyboardButton("💳 عرض الرصيد", callback_data="check_balance")
        markup.add(btn_balance)
        
        text = (
            f"✅ **تمت إضافة المكافأة بنجاح!**\n\n"
            f"💰 تم إضافة: `+{amount:.7f} TRX` إلى حسابك.\n"
            f"💎 إجمالي رصيدك: `{new_balance:.7f} TRX`\n\n"
            f"استمر في الربح! 🚀"
        )
        bot.send_message(user_id, text, parse_mode='Markdown', reply_markup=markup)
        
        return jsonify({"status": "success", "new_balance": new_balance}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/get_user/<int:user_id>", methods=["GET"])
def api_get_user(user_id):
    user = get_user(user_id)
    if user:
        return jsonify({"status": "success", "balance": user[1], "referrals": user[2]}), 200
    return jsonify({"status": "not_found", "balance": 0.0, "referrals": 0}), 200


# ===== مسار التشخيص =====
@app.route('/api/diagnostic', methods=['GET'])
def api_diagnostic():
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT 1")
        c.close()
        conn.close()
        db_status = "شغالة 100%"
    except Exception as e:
        db_status = f"خطأ: {str(e)}"
    return jsonify({"server": "شغال", "database": db_status}), 200


# تشغيل البوت في الخلفية عشان يشتغل مع السيرفر
def run_polling():
    bot.infinity_polling()

# بدء تشغيل البوت
threading.Thread(target=run_polling, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
