import telebot
from telebot import types

# ⚠️ ضع التوكن هنا
BOT_TOKEN = '9146096363:AAEjCeMT60JTUIBto8KpxKTl7lBbqAHVRtg'
bot = telebot.TeleBot(BOT_TOKEN)

user_balances = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id not in user_balances:
        user_balances[user_id] = 0.0000000

    markup = types.InlineKeyboardMarkup()
    
    # ⚠️ ضع رابط موقعك هنا
    btn_app = types.InlineKeyboardButton(
        text="🔥 فتح التطبيق ومشاهدة الإعلانات", 
        web_app=types.WebAppInfo(url="https://your-site.netlify.app") 
    )
    markup.add(btn_app)

    balance_formatted = f"{user_balances[user_id]:.7f}"
    
    welcome_text = (
        f"👋 أهلاً بك في **Zideot Tron**\n\n"
        f"💎 رصيدك الحالي:\n"
        f"`{balance_formatted} kk`\n\n"
        f"⚡️ **ملاحظة:** كل 100 إعلان تعادل 1.0000000 kk\n\n"
        f"اضغط على الزر أدناه لفتح التطبيق والبدء بالربح."
    )
    
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown', reply_markup=markup)

print("البوت يعمل الآن...")
bot.infinity_polling()
