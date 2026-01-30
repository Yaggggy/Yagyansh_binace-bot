import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.config import get_exchange 
from src.utils import log_trade, validate_inputs

def place_market_order(symbol, side, quantity):
    exchange = get_exchange()
    try:
        validate_inputs(symbol, float(quantity))
        log_trade(f"MARKET {side}", symbol, quantity, status="SENDING")
        
        # Execute Order
        order = exchange.create_order(symbol, 'market', side, quantity)
        
        log_trade(f"MARKET {side}", symbol, quantity, order['average'], "FILLED")
        print(f"Order Successful: {order['id']}")
        
    except Exception as e:
        log_trade(f"MARKET {side}", symbol, quantity, status="ERROR")
        print(f"Error: {e}")

if __name__ == "__main__":
    # Usage: python src/market_orders.py BTC/USDT buy 0.001
    place_market_order(sys.argv[1], sys.argv[2], float(sys.argv[3]))