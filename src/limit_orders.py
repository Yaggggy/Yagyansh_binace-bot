import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.config import get_exchange 
from src.utils import log_trade, validate_inputs

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'

def place_limit_order(symbol, side, quantity, price):
    """
    Place a limit order at a specific price target.
    
    Args:
        symbol: Trading pair (e.g., BTC/USDT)
        side: Order side (buy/sell)
        quantity: Order quantity
        price: Target price for execution
    """
    exchange = get_exchange()
    
    try:
        # Validate inputs with exchange rules
        validate_inputs(symbol, quantity, price, exchange)
        
        log_trade(f"LIMIT {side.upper()}", symbol, quantity, price, status="SENDING")
        print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Processing limit {side.upper()} order")
        
        # Execute Limit Order
        order = exchange.create_order(
            symbol=symbol,
            type='limit',
            side=side,
            amount=quantity,
            price=price
        )
        
        log_trade(f"LIMIT {side.upper()}", symbol, quantity, price, "OPEN", f"ID: {order['id']}")
        print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} Limit order placed successfully")
        print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} Order ID: {order['id']}")
        print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} Details: {side.upper()} {quantity} {symbol} @ {price}")
        return order
        
    except Exception as e:
        log_trade(f"LIMIT {side.upper()}", symbol, quantity, price, status="ERROR", details=str(e))
        print(f"{Colors.RED}[ERROR]{Colors.ENDC} Limit order failed: {e}")

if __name__ == "__main__":
    # Usage: python src/limit_orders.py BTC/USDT buy 0.001 55000
    if len(sys.argv) < 5:
        print("Usage: python src/limit_orders.py <symbol> <buy/sell> <qty> <price>")
    else:
        place_limit_order(sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]))