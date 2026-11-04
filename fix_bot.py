import re
with open('bot.py', 'r', encoding='utf-8') as f:
    content = f.read()

# تعديل زر فتح التطبيق عشان ياخد الرصيد
old_btn = """btn_app = types.InlineKeyboardButton(
        text="🔥 فتح التطبيق ومشاهدة الإعلانات", 
        web_app=types.WebAppInfo(url="https://zideot-tron-karim.netlify.app") 
    )"""
    
new_btn = """current_bal = user[1] if user else 0.0
    btn_app = types.InlineKeyboardButton(
        text="🔥 فتح التطبيق ومشاهدة الإعلانات", 
        web_app=types.WebAppInfo(url=f"https://zideot-tron-karim.netlify.app/?balance={current_bal}") 
    )"""

if old_btn in content:
    content = content.replace(old_btn, new_btn)
    with open('bot.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ تم تعديل البوت بنجاح")
else:
    print("⚠️ لم يتم العثور على الكود القديم، قد يكون معدلاً مسبقاً.")
