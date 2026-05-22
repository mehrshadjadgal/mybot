* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Tahoma', sans-serif;
    background: linear-gradient(135deg, #1e3a8a, #3b82f6);
    color: white;
    min-height: 100vh;
    padding: 15px;
}

.container {
    max-width: 600px;
    margin: 0 auto;
}

.header {
    text-align: center;
    margin-bottom: 25px;
}

.header h1 {
    font-size: 24px;
    margin-bottom: 8px;
}

.plans {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
}

.plan-card {
    background: rgba(255, 255, 255, 0.15);
    border-radius: 16px;
    padding: 18px 12px;
    text-align: center;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.2);
}

.plan-card h2 {
    font-size: 22px;
    margin-bottom: 8px;
}

.price {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 15px;
    color: #fff;
}

.buy-btn {
    background: #22c55e;
    color: white;
    border: none;
    padding: 12px 20px;
    border-radius: 12px;
    font-size: 16px;
    width: 100%;
    cursor: pointer;
    font-weight: bold;
}

.buy-btn:hover {
    background: #16a34a;
    transform: scale(1.05);
}

@media (max-width: 480px) {
    .plans {
        grid-template-columns: 1fr;
    }
}