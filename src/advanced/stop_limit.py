import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.config import get_exchange
from src.utils import log_trade, validate_inputs

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m'

def place_stop_limit_order(symbol, side, quantity, stop_price, limit_price):
    """
    Place a stop-limit order that triggers a limit order when stop price is reached.
    
    The order remains inactive until the stop price is triggered.
    Once triggered, it becomes a limit order at the specified limit price.
    
    Args:
        symbol: Trading pair (e.g., BTC/USDT)
        side: Order side (buy/sell)
        quantity: Order quantity
        stop_price: Price level that triggers the order (activation trigger)
        limit_price: Price at which the order executes (after activation)
    
    Returns:
        Order confirmation dictionary
    """
    exchange = get_exchange()
    
    try:
        # Input validation
        validate_inputs(symbol, quantity, stop_price, exchange)
        validate_inputs(symbol, quantity, limit_price, exchange)
        
        # Validate stop and limit prices make sense
        if side.lower() == 'buy':
            # For buy orders: stop_price should be >= limit_price (buy below/at stop)
            if stop_price < limit_price:
                raise ValueError(
                    f"For BUY orders: Stop price ({stop_price}) should be >= Limit price ({limit_price})"
                )
        else:  # sell
            # For sell orders: stop_price should be <= limit_price (sell above/at stop)
            if stop_price > limit_price:
                raise ValueError(
                    f"For SELL orders: Stop price ({stop_price}) should be <= Limit price ({limit_price})"
                )
        
        log_trade(f"STOP-LIMIT {side.upper()}", symbol, quantity, 
                 f"Stop:{stop_price}/Limit:{limit_price}", status="SENDING")
        
        print(f"\n{Colors.BLUE}[INFO]{Colors.ENDC} Processing stop-limit {side.upper()} order")
        print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Stop Price: {stop_price:.4f} | Limit Price: {limit_price:.4f}")
        
        # Create stop-limit order using CCXT
        # Note: In simulation, this creates the order immediately
        # In live trading, it waits for the stop price to be triggered
        params = {
            'stopPrice': stop_price,
        }
        
        order = exchange.create_order(
            symbol=symbol,
            type='limit',
            side=side,
            amount=quantity,
            price=limit_price,
            params=params
        )
        
        log_trade(f"STOP-LIMIT {side.upper()}", symbol, quantity,
                 f"Stop:{stop_price}/Limit:{limit_price}", "PENDING", f"ID: {order['id']}")
        
        # Calculate and display relevant information
        if side.lower() == 'buy':
            potential_savings = ((stop_price - limit_price) / limit_price * 100)
            print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} Stop-limit order placed successfully")
            print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} Order ID: {order['id']}")
            print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Order Status: PENDING (Waiting for price to touch {stop_price:.4f})")
            if potential_savings > 0:
                print(f"{Colors.YELLOW}[INFO]{Colors.ENDC} Potential savings: {potential_savings:.2f}%")
        else:  # sell
            potential_profit = ((limit_price - stop_price) / stop_price * 100)
            print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} Stop-limit order placed successfully")
            print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} Order ID: {order['id']}")
            print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Order Status: PENDING (Waiting for price to touch {stop_price:.4f})")
            if potential_profit > 0:
                print(f"{Colors.YELLOW}[INFO]{Colors.ENDC} Potential profit increase: {potential_profit:.2f}%")
        
        return order
        
    except Exception as e:
        log_trade(f"STOP-LIMIT {side.upper()}", symbol, quantity,
                 f"Stop:{stop_price}/Limit:{limit_price}", status="ERROR", details=str(e))
        print(f"{Colors.RED}[ERROR]{Colors.ENDC} Stop-limit order failed: {e}")
        return None

def explain_stop_limit():
    """Display explanation of how stop-limit orders work."""
    print(f"\n{Colors.BLUE}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BLUE}STOP-LIMIT ORDER EXPLANATION{Colors.ENDC}")
    print(f"{Colors.BLUE}{'='*70}{Colors.ENDC}\n")
    
    print("A stop-limit order combines two prices:")
    print("  1. STOP PRICE - Triggers the order when reached")
    print("  2. LIMIT PRICE - Price at which the order executes\n")
    
    print(f"{Colors.YELLOW}[EXAMPLE 1: BUY STOP-LIMIT]{Colors.ENDC}")
    print("  Current Price: $45,000")
    print("  Stop Price: $44,000")
    print("  Limit Price: $43,500")
    print("  Scenario: Price drops to $44,000 → Order activates")
    print("  Result: BUY at $43,500 (if market allows) or better\n")
    
    print(f"{Colors.YELLOW}[EXAMPLE 2: SELL STOP-LIMIT]{Colors.ENDC}")
    print("  Current Price: $45,000")
    print("  Stop Price: $44,000")
    print("  Limit Price: $43,500")
    print("  Scenario: Price drops to $44,000 → Order activates")
    print("  Result: SELL at $43,500 (if market allows) or better\n")
    
    print(f"{Colors.YELLOW}[KEY POINTS]{Colors.ENDC}")
    print("  - Order is INACTIVE until stop price is triggered")
    print("  - Once triggered, it becomes a regular limit order")
    print("  - Limit price must be better than or at stop price")
    print("  - Useful for risk management and entry/exit strategies")
    print(f"{Colors.BLUE}{'='*70}{Colors.ENDC}\n")

if __name__ == "__main__":
    # Usage: python src/advanced/stop_limit.py BTC/USDT buy 0.01 44000 43500
    if len(sys.argv) < 6:
        print("Usage: python src/advanced/stop_limit.py <symbol> <buy/sell> <qty> <stop_price> <limit_price>")
        print("\nExample: python src/advanced/stop_limit.py BTC/USDT buy 0.01 44000 43500")
        explain_stop_limit()
    else:
        place_stop_limit_order(sys.argv[1], sys.argv[2], float(sys.argv[3]), 
                              float(sys.argv[4]), float(sys.argv[5]))
