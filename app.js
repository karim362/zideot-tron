window.addEventListener('load', function() {
    const tg = window.Telegram?.WebApp;
    if (tg) tg.expand();

    const BLOCK_ID = "57861"; 
    
    const urlParams = new URLSearchParams(window.location.search);
    let currentBalance = parseFloat(urlParams.get('balance') || 0.0000000);
    let refsCount = parseInt(urlParams.get('refs') || 0);
    const REWARD_AMOUNT = 0.01;

    function updateUI() {
        const balanceEl = document.getElementById('balance');
        if (balanceEl) balanceEl.innerText = currentBalance.toFixed(7);
    }

    const watchAdBtn = document.getElementById('watchAdBtn');
    const showBalanceBtn = document.getElementById('showBalanceBtn');
    const showRefsBtn = document.getElementById('showRefsBtn');
    const statusMessage = document.getElementById('statusMessage');

    if (showBalanceBtn) {
        showBalanceBtn.addEventListener('click', () => {
            tg.showAlert(`💎 رصيدك الحالي: ${currentBalance.toFixed(7)} TRX`);
        });
    }

    if (showRefsBtn) {
        showRefsBtn.addEventListener('click', () => {
            tg.showAlert(`👥 عدد إحالاتك: ${refsCount}\n\nكل 100 إحالة = 1.0000000 TRX`);
        });
    }

    if (watchAdBtn) {
        watchAdBtn.addEventListener('click', () => {
            if (!window.Adsgram) return;
            const AdController = window.Adsgram.init({ blockId: BLOCK_ID });

            watchAdBtn.disabled = true;
            if(statusMessage) statusMessage.innerText = "جاري تحميل الإعلان...";

            AdController.show()
                .then((result) => {
                    currentBalance += REWARD_AMOUNT;
                    updateUI();
                    if(statusMessage) statusMessage.innerText = `🎉 مبروك! تمت الإضافة.`;
                    watchAdBtn.disabled = false;

                    // إرسال البيانات للسيرفر (بدون إغلاق التطبيق)
                    const userId = tg?.initDataUnsafe?.user?.id;
                    if (userId) {
                        // ⚠️ هتغير الرابط ده برابط Render الخاص بك بعد شوي
                        fetch('https://zideot-bot.onrender.com/api/add_points', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ user_id: userId, amount: REWARD_AMOUNT })
                        }).catch(e => console.log("Fetch error:", e));
                    }
                })
                .catch((result) => {
                    if(statusMessage) statusMessage.innerText = "⚠️ لم تكمل مشاهدة الإعلان.";
                    watchAdBtn.disabled = false;
                });
        });
    }
    updateUI();
});
