import re

with open('bot.py', 'r', encoding='utf-8') as f:
    content = f.read()

# مسح أي كود استقبال قديم
content = re.sub(r'# ===== استقبال.*', '', content, flags=re.DOTALL)

# إضافة كود الاستقبال الجديد المطور
new_handler = """
# ===== استقبال رسائل إضافة النقاط من الموقع =====
@bot.message_handler(func=lambda message: message.text and '__ADD_POINTS__' in message.text)
def handle_add_points(message):
    print(f"\\n[!] وصلت رسالة جديدة: {message.text}") # طباعة في التريمكس للتشخيص
    try:
        user_id = message.from_user.id
        # استخراج الرقم وتنظيف النص من أي مسافات
        amount_str = message.text.replace('__ADD_POINTS__', '').strip()
        amount = float(amount_str)
        
        add_points(user_id, amount)
        user = get_user(user_id)
        new_balance = user[1]
        
        print(f"[+] تم إضافة {amount} للمستخدم {user_id}. الرصيد الجديد: {new_balance}")
        
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

print("✅ تم تحديث الكود بنجاح")
