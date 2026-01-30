import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.config import get_exchange
from src.utils import log_trade

def place_futures_oco(symbol, side, quantity, take_profit_price, stop_loss_price):
    exchange = get_exchange()
    
    # Invert side for closing orders (if entry is Buy, exits are Sell)
    exit_side = 'sell' if side.lower() == 'buy' else 'buy'
    
    try:
        log_trade(f"OCO ENTRY", symbol, quantity, status="SENDING")

        # 1. Place the Entry Order (Market for immediate entry, or Limit)
        entry_order = exchange.create_order(symbol, 'market', side, quantity)
        log_trade(f"OCO ENTRY FILLED", symbol, quantity, entry_order['average'], "FILLED")
        
        params = {'reduceOnly': True}

        # 2. Place Take Profit (Limit Order)
        tp_order = exchange.create_order(symbol, 'limit', exit_side, quantity, take_profit_price, params)
        print(f"TP Placed at {take_profit_price}")

        # 3. Place Stop Loss (Stop Market)
        # Note: params structure depends on exchange, for Binance Futures via CCXT:
        sl_params = {'stopPrice': stop_loss_price, 'reduceOnly': True}
        sl_order = exchange.create_order(symbol, 'STOP_MARKET', exit_side, quantity, None, sl_params)
        print(f"SL Placed at {stop_loss_price}")
        
        log_trade(f"OCO EXITS PLACED", symbol, quantity, f"TP:{take_profit_price}/SL:{stop_loss_price}", "ACTIVE")

    except Exception as e:
        log_trade("OCO ERROR", symbol, quantity, status="ERROR")
        print(f"Error: {e}")

if __name__ == "__main__":
    # Usage: python src/advanced/oco.py BTC/USDT buy 0.01 50000 40000
    place_futures_oco(sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]))