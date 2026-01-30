import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.config import get_exchange
from src.utils import log_trade

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'

def place_futures_oco(symbol, side, quantity, take_profit_price, stop_loss_price):
    """
    Place an One-Cancels-Other (OCO) order with take profit and stop loss.
    
    Args:
        symbol: Trading pair (e.g., BTC/USDT)
        side: Order side (buy/sell)
        quantity: Order quantity
        take_profit_price: Take profit price level
        stop_loss_price: Stop loss price level
    """
    exchange = get_exchange()
    
    # Invert side for closing orders (if entry is Buy, exits are Sell)
    exit_side = 'sell' if side.lower() == 'buy' else 'buy'
    
    try:
        log_trade(f"OCO ENTRY", symbol, quantity, status="SENDING")
        print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Placing OCO entry order for {quantity} {symbol}")

        # 1. Place the Entry Order (Market for immediate entry, or Limit)
        entry_order = exchange.create_order(symbol, 'market', side, quantity)
        log_trade(f"OCO ENTRY FILLED", symbol, quantity, entry_order['average'], "FILLED")
        print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} Entry order filled at {entry_order['average']:.4f}")
        
        params = {'reduceOnly': True}

        # 2. Place Take Profit (Limit Order)
        tp_order = exchange.create_order(symbol, 'limit', exit_side, quantity, take_profit_price, params)
        print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} Take Profit order placed at {take_profit_price:.4f}")

        # 3. Place Stop Loss (Stop Market)
        sl_params = {'stopPrice': stop_loss_price, 'reduceOnly': True}
        sl_order = exchange.create_order(symbol, 'STOP_MARKET', exit_side, quantity, None, sl_params)
        print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} Stop Loss order placed at {stop_loss_price:.4f}")
        
        log_trade(f"OCO EXITS PLACED", symbol, quantity, f"TP:{take_profit_price}/SL:{stop_loss_price}", "ACTIVE")
        print(f"\n{Colors.BLUE}[INFO]{Colors.ENDC} OCO Strategy Summary:")
        print(f"  Entry Price: {entry_order['average']:.4f}")
        print(f"  Take Profit: {take_profit_price:.4f}")
        print(f"  Stop Loss: {stop_loss_price:.4f}")
        print(f"  Potential Profit: {((take_profit_price - entry_order['average']) / entry_order['average'] * 100):.2f}%")
        print(f"  Maximum Loss: {((entry_order['average'] - stop_loss_price) / entry_order['average'] * 100):.2f}%")

    except Exception as e:
        log_trade("OCO ERROR", symbol, quantity, status="ERROR", details=str(e))
        print(f"{Colors.RED}[ERROR]{Colors.ENDC} OCO placement failed: {e}")

if __name__ == "__main__":
    # Usage: python src/advanced/oco.py BTC/USDT buy 0.01 50000 40000
    if len(sys.argv) < 6:
        print("Usage: python src/advanced/oco.py <symbol> <buy/sell> <qty> <take_profit_price> <stop_loss_price>")
    else:
        place_futures_oco(sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]))