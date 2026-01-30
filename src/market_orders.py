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

def place_market_order(symbol, side, quantity):
    """
    Execute a market order at current market price.
    
    Args:
        symbol: Trading pair (e.g., BTC/USDT)
        side: Order side (buy/sell)
        quantity: Order quantity
    """
    exchange = get_exchange()
    try:
        validate_inputs(symbol, float(quantity))
        log_trade(f"MARKET {side.upper()}", symbol, quantity, status="SENDING")
        print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Processing market {side.upper()} order for {quantity} {symbol}")
        
        # Execute Order
        order = exchange.create_order(symbol, 'market', side, quantity)
        
        log_trade(f"MARKET {side.upper()}", symbol, quantity, order['average'], "FILLED")
        print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} Market order executed")
        print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} Order ID: {order['id']}")
        print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} Average Price: {order['average']}")
        
    except Exception as e:
        log_trade(f"MARKET {side.upper()}", symbol, quantity, status="ERROR", details=str(e))
        print(f"{Colors.RED}[ERROR]{Colors.ENDC} Market order failed: {e}")

if __name__ == "__main__":
    # Usage: python src/market_orders.py BTC/USDT buy 0.001
    if len(sys.argv) < 4:
        print("Usage: python src/market_orders.py <symbol> <buy/sell> <qty>")
    else:
        place_market_order(sys.argv[1], sys.argv[2], float(sys.argv[3]))