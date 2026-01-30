import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.config import get_exchange 
from src.utils import log_trade, validate_inputs

def place_limit_order(symbol, side, quantity, price):
    exchange = get_exchange()
    
    try:
        # Validate inputs with exchange rules
        validate_inputs(symbol, quantity, price, exchange)
        
        log_trade(f"LIMIT {side.upper()}", symbol, quantity, price, status="SENDING")
        
        # Execute Limit Order
        order = exchange.create_order(
            symbol=symbol,
            type='limit',
            side=side,
            amount=quantity,
            price=price
        )
        
        log_trade(f"LIMIT {side.upper()}", symbol, quantity, price, "OPEN", f"ID: {order['id']}")
        print(f"✅ Limit Order Placed: {side} {quantity} {symbol} @ {price}")
        return order
        
    except Exception as e:
        log_trade(f"LIMIT {side.upper()}", symbol, quantity, price, status="ERROR", details=str(e))
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Usage: python src/limit_orders.py BTC/USDT buy 0.001 55000
    if len(sys.argv) < 5:
        print("Usage: python src/limit_orders.py <symbol> <buy/sell> <qty> <price>")
    else:
        place_limit_order(sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]))