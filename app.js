window.addEventListener('load', function() {
    const tg = window.Telegram?.WebApp;
    if (tg) tg.expand();

    const BLOCK_ID = "57861"; 
    const urlParams = new URLSearchParams(window.location.search);
    let userId = tg?.initDataUnsafe?.user?.id || urlParams.get('user_id');
    
    let currentBalance = parseFloat(urlParams.get('balance') || 0.0000000);
    let refsCount = parseInt(urlParams.get('refs') || 0);
    
    const REWARD_AMOUNT = 0.01;

    function updateUI() {
        const balanceEl = document.getElementById('balance');
        if (balanceEl) balanceEl.innerText = currentBalance.toFixed(7);
    }

    updateUI();

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
        } catch (e) {}
    }

    fetchBalanceFromServer();

    const watchAdBtn = document.getElementById('watchAdBtn');
    const showBalanceBtn = document.getElementById('showBalanceBtn');
    const showRefsBtn = document.getElementById('showRefsBtn');
    const withdrawBtn = document.getElementById('withdrawBtn');
    const statusMessage = document.getElementById('statusMessage');

    if (showBalanceBtn) showBalanceBtn.addEventListener('click', () => tg.showAlert(`💎 رصيدك الحالي: ${currentBalance.toFixed(7)} TRX`));
    
    // زر الإحالات
    if (showRefsBtn) showRefsBtn.addEventListener('click', () => tg.showAlert(`👥 عدد إحالاتك: ${refsCount}\n\nكل 100 إحالة = 1.0000000 TRX`));

    // زر السحب
    if (withdrawBtn) {
        withdrawBtn.addEventListener('click', () => {
            if (currentBalance >= 10.0) {
                tg.showAlert("✅ طلب السحب قيد المعالجة!\nسيتم تحويل المبلغ إلى محفظتك قريباً. يرجى التواصل مع الدعم لإكمال العملية.");
                // هنا ممكن تضيف كود يبعت إشعار للمطور عشان يحول المبلغ
            } else {
                tg.showAlert(`⚠️ الحد الأدنى للسحب هو 10.0000000 TRX.\nرصيدك الحالي: ${currentBalance.toFixed(7)} TRX\n\nاستمر في جمع النقاط!`);
            }
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
});
