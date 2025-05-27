# ✅ calculate_position.py (Final Enhanced Version)
# ⚙️ إعدادات قابلة للتعديل - الآن مربوطة مع تيليجرام
from settings import load_settings
import ccxt
settings = load_settings()

risk = settings["risk"]
leverage = settings["leverage"]
use_percentage = settings["use_percentage"]
fixed_amount = settings["fixed_amount"]



# 🔐 مفاتيح Binance Testnet (تأكد أنها مطابقة لباقي ملفاتك)
api_key = 'cae8dd73436fad5416d4efc52b1dd9cbe5fabf0017c202dbbab910b64f3b63e9'
api_secret = '00a2ecf4d375752b214168e56bf1d2923af4016865344381aa4b759079563009'

exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future'
    }
})

exchange.set_sandbox_mode(True)

# ✅ تعيين الرافعة المالية مباشرة
def set_leverage(symbol, leverage):
    try:
        exchange.load_markets()
        response = exchange.set_leverage(leverage, symbol)
        print(f"🔁 Leverage set to {leverage}x for {symbol}")
        return response
    except Exception as e:
        print("❌ Error setting leverage:", e)

# ✅ جلب رصيد USDT من Futures Testnet
def get_futures_balance():
    try:
        balance = exchange.fetch_balance({"type": "future"})
        usdt_balance = balance['total']['USDT']
        print(f"💰 Current USDT Balance: {usdt_balance}")
        return usdt_balance
    except Exception as e:
        print("❌ Error fetching balance:", e)
        return 1000  # fallback وهمي إذا فشل الطلب

# ✅ حساب حجم الصفقة بناءً على الرصيد أو المبلغ الثابت

def calculate_position(entry_price, symbol):
    current_leverage = LEVERAGE()
    set_leverage(symbol, current_leverage)

    if USE_PERCENTAGE():
        capital_to_use = get_futures_balance() * RISK_PERCENTAGE()
    else:
        capital_to_use = FIXED_AMOUNT()

    position_size = (capital_to_use * current_leverage) / entry_price
    print(f"🧮 Entry: {entry_price}, Capital: {capital_to_use}, Leverage: {current_leverage}x, Size: {position_size}")
    return round(position_size, 3)
