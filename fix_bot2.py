import re

with open('bot.py', 'r', encoding='utf-8') as f:
    content = f.read()

# مسح أي كود استقبال قديم
content = re.sub(r'# ===== استقبال.*', '', content, flags=re.DOTALL)

new_handler = """
# ===== استقبال البيانات الرسمية من الموقع =====
@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    print(f"\\n[!] استلمت بيانات من الموقع: {message.web_app_data.data}")
    try:
        import json
        data = json.loads(message.web_app_data.data)
        
        if data.get("action") == "add_points":
            amount = data.get("amount", 0.01)
            user_id = message.from_user.id
            
            add_points(user_id, amount)
            user = get_user(user_id)
            new_balance = user[1]
            
            print(f"[+] تم إضافة {amount} TRX. الرصيد الحالي: {new_balance}")
            
            markup = types.InlineKeyboardMarkup()
            btn_balance = types.InlineKeyboardButton("💳 عرض الرصيد الحالي", callback_data="check_balance")
            markup.add(btn_balance)

            text = (
                f"✅ **تمت إضافة المكافأة بنجاح!**\\n\\n"
                f"💰 تم إضافة: `+{amount} TRX` إلى حسابك.\\n"
                f"💎 إجمالي رصيدك: `{new_balance:.7f} TRX`\\n\\n"
                f"استمر في مشاهدة الإعلانات لزيادة أرباحك! 🚀"
            )
            
            bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)
    except Exception as e:
        print(f"[-] خطأ في المعالجة: {e}")

@bot.callback_query_handler(func=lambda call: call.data == "check_balance")
def callback_balance(call):
    user_id = call.from_user.id
    user = get_user(user_id)
    balance = user[1]
    
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"💎 **رصيدك المحدث:**\\n`{balance:.7f} TRX`",
        parse_mode='Markdown'
    )

print("البوت يعمل الآن...")
bot.infinity_polling()
"""

content = content + new_handler

with open('bot.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ تم تحديث البوت بنجاح")
