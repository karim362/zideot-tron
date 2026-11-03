const tg = window.Telegram.WebApp;
tg.expand();

// ⚠️ ضع الـ Block ID الخاص بك هنا
const BLOCK_ID = "ضع_رقم_الـ_Block_ID_هنا"; 

let AdController;
try {
    AdController = window.Adsgram.init({ blockId: BLOCK_ID });
} catch (e) {
    console.error("خطأ في تحميل الإعلانات", e);
}

let currentBalance = 0.0000000;
const REWARD_AMOUNT = 0.01;

function updateUI() {
    document.getElementById('balance').innerText = currentBalance.toFixed(7);
}

const watchAdBtn = document.getElementById('watchAdBtn');
const statusMessage = document.getElementById('statusMessage');

watchAdBtn.addEventListener('click', () => {
    if (!AdController) {
        statusMessage.innerText = "عذراً، الإعلانات غير متوفرة حالياً.";
        return;
    }

    watchAdBtn.disabled = true;
    statusMessage.innerText = "جاري تحميل الإعلان...";
    watchAdBtn.innerHTML = "جاري التحميل...";

    AdController.show()
        .then((result) => {
            currentBalance += REWARD_AMOUNT;
            updateUI();
            statusMessage.innerText = `🎉 مبروك! تمت إضافة ${REWARD_AMOUNT} kk لرصيدك.`;
            watchAdBtn.disabled = false;
            watchAdBtn.innerHTML = `<span class="icon">▶</span> مشاهدة إعلان (+0.01)`;
        })
        .catch((result) => {
            statusMessage.innerText = "⚠️ لم تكمل مشاهدة الإعلان، لم يتم إضافة نقاط.";
            watchAdBtn.disabled = false;
            watchAdBtn.innerHTML = `<span class="icon">▶</span> مشاهدة إعلان (+0.01)`;
        });
});

updateUI();
