window.addEventListener('load', function() {
    const tg = window.Telegram?.WebApp;
    if (tg) tg.expand();

    const BLOCK_ID = "57861"; 
    
    const urlParams = new URLSearchParams(window.location.search);
    // نعتمد على الآي دي اللي جاي من تيليجرام
    let userId = tg?.initDataUnsafe?.user?.id || urlParams.get('user_id');
    
    let currentBalance = 0.0000000;
    let refsCount = 0;
    const REWARD_AMOUNT = 0.01;

    function updateUI() {
        const balanceEl = document.getElementById('balance');
        if (balanceEl) balanceEl.innerText = currentBalance.toFixed(7);
    }

    // جلب الرصيد الحقيقي من السيرفر
    async function fetchBalanceFromServer() {
        if (!userId) return;
        try {
            const response = await fetch(`https://zideot-tron.onrender.com/api/get_user/${userId}`);
            const data = await response.json();
            if (data.status === 'success') {
                currentBalance = data.balance;
                refsCount = data.referrals;
                updateUI();
            }
        } catch (e) {
            console.log("خطأ في جلب الرصيد:", e);
        }
    }

    // تشغيل جلب الرصيد بمجرد فتح التطبيق
    fetchBalanceFromServer();

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

                    // إرسال النقاط للسيرفر
                    fetch('https://zideot-tron.onrender.com/api/add_points', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ user_id: userId, amount: REWARD_AMOUNT })
                    }).catch(e => console.log(e));
                })
                .catch((result) => {
                    if(statusMessage) statusMessage.innerText = "⚠️ لم تكمل مشاهدة الإعلان.";
                    watchAdBtn.disabled = false;
                });
        });
    }
    updateUI();
});
