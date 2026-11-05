window.addEventListener('load', async function() {
    const tg = window.Telegram?.WebApp;
    if (tg) tg.expand();
    let report = "🔍 تقرير الفحص:\n\n";
    try {
        const res = await fetch('https://zideot-tron.onrender.com/api/diagnostic');
        const data = await res.json();
        report += `🌐 السيرفر: ${data.server}\n🗄️ قاعدة البيانات: ${data.database}\n`;
    } catch (e) {
        report += "❌ فشل الاتصال بالسيرفر (Render نايم أو متوقف).\n";
    }
    document.body.innerHTML = `<div style="padding: 20px; color: white; background: #121212; font-family: Tahoma; direction: rtl; min-height: 100vh;"><h2 style="color: #FF060A;">Zideot Tron - تشخيص</h2><pre style="white-space: pre-wrap; font-size: 18px; line-height: 1.6;">${report}</pre><button onclick="location.reload()" style="margin-top: 20px; padding: 10px 20px; background: #FF060A; color: white; border: none; border-radius: 5px;">إعادة الفحص</button></div>`;
});
