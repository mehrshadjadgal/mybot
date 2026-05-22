document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.buy-btn');
    
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const planCard = button.parentElement;
            const planSize = planCard.querySelector('h2').textContent;
            const price = planCard.querySelector('.price').textContent;
            
            // ارسال اطلاعات به ربات تلگرام
            const message = `🛒 خرید جدید:\n\nپلن: ${planSize}\nقیمت: ${price}`;
            
            // این قسمت بعداً با Web App API تلگرام کامل می‌شه
            alert(`✅ انتخاب شد:\n${planSize} - ${price}\n\nدر حال اتصال به ربات...`);
            
            // پیام به ربات (در نسخه کامل)
            if (window.Telegram && window.Telegram.WebApp) {
                window.Telegram.WebApp.sendData(JSON.stringify({
                    action: "buy",
                    plan: planSize,
                    price: price
                }));
            }
        });
    });
});