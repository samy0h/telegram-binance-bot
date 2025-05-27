# ✅ binance_handler.py (Enhanced version with multiple TP and SL adjustment)

import ccxt

api_key = 'cae8dd73436fad5416d4efc52b1dd9cbe5fabf0017c202dbbab910b64f3b63e9'
api_secret = '00a2ecf4d375752b214168e56bf1d2923af4016865344381aa4b759079563009'

exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future',
    }
})

exchange.set_sandbox_mode(True)

# ✅ أمر جني أرباح نسبي

def create_take_profit(symbol, side, quantity, price):
    try:
        return exchange.create_order(
            symbol=symbol,
            type="TAKE_PROFIT_MARKET",
            side=side,
            amount=quantity,
            params={
                "stopPrice": price,
                "closePosition": False
            }
        )
    except Exception as e:
        print(f"❌ Failed to set TP at {price}:", e)

# ✅ أمر وقف الخسارة

def create_stop_loss(symbol, side, quantity, price):
    try:
        return exchange.create_order(
            symbol=symbol,
            type="STOP_MARKET",
            side=side,
            amount=quantity,
            params={
                "stopPrice": price,
                "closePosition": True
            }
        )
    except Exception as e:
        print("❌ Failed to set SL:", e)

# ✅ إلغاء SL السابق وتحديثه

def update_stop_loss(symbol, side, quantity, new_price):
    try:
        orders = exchange.fetch_open_orders(symbol)
        for order in orders:
            if order['type'].lower() == 'stop_market':
                exchange.cancel_order(order['id'], symbol)
        create_stop_loss(symbol, side, quantity, new_price)
        print(f"🔁 Stop Loss updated to {new_price}")
    except Exception as e:
        print("❌ Error updating SL:", e)

# ✅ فتح صفقة شراء وتوزيع الكمية 40% - 40% - 20%

def open_long(symbol, quantity, tps=[], sl=None, entry=None):
    try:
        exchange.create_market_buy_order(symbol, quantity)
        print("✅ Market Buy Executed")

        if len(tps) == 3:
            tp1_qty = round(quantity * 0.4, 3)
            tp2_qty = round(quantity * 0.4, 3)
            tp3_qty = round(quantity * 0.2, 3)
            create_take_profit(symbol, 'sell', tp1_qty, tps[0])
            create_take_profit(symbol, 'sell', tp2_qty, tps[1])
            create_take_profit(symbol, 'sell', tp3_qty, tps[2])
            print(f"🎯 TP1 set at {tps[0]} for {tp1_qty} units")
            print(f"🎯 TP2 set at {tps[1]} for {tp2_qty} units")
            print(f"🎯 TP3 set at {tps[2]} for {tp3_qty} units")

        if entry and sl:
            create_stop_loss(symbol, 'sell', quantity, sl)
            print(f"🛑 SL set at {sl}")

    except Exception as e:
        print("❌ Error in LONG:", e)

# ✅ فتح صفقة بيع وتوزيع الكمية 40% - 40% - 20%

def open_short(symbol, quantity, tps=[], sl=None, entry=None):
    try:
        exchange.create_market_sell_order(symbol, quantity)
        print("✅ Market Sell Executed")

        if len(tps) == 3:
            tp1_qty = round(quantity * 0.4, 3)
            tp2_qty = round(quantity * 0.4, 3)
            tp3_qty = round(quantity * 0.2, 3)
            create_take_profit(symbol, 'buy', tp1_qty, tps[0])
            create_take_profit(symbol, 'buy', tp2_qty, tps[1])
            create_take_profit(symbol, 'buy', tp3_qty, tps[2])
            print(f"🎯 TP1 set at {tps[0]} for {tp1_qty} units")
            print(f"🎯 TP2 set at {tps[1]} for {tp2_qty} units")
            print(f"🎯 TP3 set at {tps[2]} for {tp3_qty} units")

        if entry and sl:
            create_stop_loss(symbol, 'buy', quantity, sl)
            print(f"🛑 SL set at {sl}")

    except Exception as e:
        print("❌ Error in SHORT:", e)

# ✅ إغلاق الصفقة بالكامل

def close_position(symbol, side):
    try:
        position = exchange.fetch_positions([symbol])[0]
        amount = abs(float(position['contracts']))
        if amount > 0:
            close_side = 'sell' if side == 'buy' else 'buy'
            exchange.create_market_order(symbol, close_side, amount, {'reduceOnly': True})
            print(f"✅ Position on {symbol} closed successfully.")
        else:
            print(f"ℹ️ No open position to close on {symbol}")
    except Exception as e:
        print("❌ Error closing position:", e)

# ✅ تعديل وقف الخسارة حسب TP

def handle_tp_update(symbol, side, quantity, tp_hit, entry, tps):
    if tp_hit == 1:
        new_sl = round(entry * 0.99, 6)
    elif tp_hit == 2 and len(tps) >= 1:
        new_sl = round(tps[0] * 0.99, 6)
    elif tp_hit == 3 and len(tps) >= 2:
        new_sl = round(tps[1] * 0.99, 6)
    else:
        print("⚠️ Not enough data to update SL")
        return

    sl_side = 'sell' if side == 'buy' else 'buy'
    update_stop_loss(symbol, sl_side, quantity, new_sl)
