with open('bot.py', 'r', encoding='utf-8') as f:
    content = f.read()

diag_code = """
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
"""
import re
content = re.sub(r"@app\.route\('/'\)\ndef index\(\):\n    return \"Bot API is running!\"", diag_code, content)
with open('bot.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ تم تعديل البوت")
