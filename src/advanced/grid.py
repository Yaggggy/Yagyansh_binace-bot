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

def place_grid_orders(symbol, center_price, quantity_per_grid, grid_levels, grid_step_percent):
    """
    Place a grid of buy orders below and sell orders above a center price.
    
    Args:
        symbol: Trading pair (e.g., BTC/USDT)
        center_price: Center price reference point
        quantity_per_grid: Quantity for each grid level
        grid_levels: Number of levels above and below center
        grid_step_percent: Step percentage between levels
    """
    exchange = get_exchange()
    
    print(f"\n{Colors.BLUE}[INFO]{Colors.ENDC} Initializing grid strategy...")
    print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Pair: {symbol} | Center: {center_price} | Levels: {grid_levels}")
    print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Step: {grid_step_percent}% | Qty per level: {quantity_per_grid}\n")

    orders_placed = 0
    orders_failed = 0

    # 1. Place Buy Orders (Below Center)
    print(f"{Colors.YELLOW}[GRID]{Colors.ENDC} Placing BUY orders below center price...\n")
    for i in range(1, grid_levels + 1):
        price = center_price * (1 - (i * grid_step_percent / 100))
        try:
            exchange.create_order(symbol, 'limit', 'buy', quantity_per_grid, price)
            log_trade(f"GRID BUY #{i}", symbol, quantity_per_grid, price, "OPEN")
            print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} Grid BUY #{i} placed at {price:.4f}")
            orders_placed += 1
        except Exception as e:
            log_trade(f"GRID BUY #{i}", symbol, quantity_per_grid, price, "ERROR", str(e))
            print(f"{Colors.RED}[ERROR]{Colors.ENDC} Grid BUY #{i} failed: {e}")
            orders_failed += 1

    # 2. Place Sell Orders (Above Center)
    print(f"\n{Colors.YELLOW}[GRID]{Colors.ENDC} Placing SELL orders above center price...\n")
    for i in range(1, grid_levels + 1):
        price = center_price * (1 + (i * grid_step_percent / 100))
        try:
            exchange.create_order(symbol, 'limit', 'sell', quantity_per_grid, price)
            log_trade(f"GRID SELL #{i}", symbol, quantity_per_grid, price, "OPEN")
            print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} Grid SELL #{i} placed at {price:.4f}")
            orders_placed += 1
        except Exception as e:
            log_trade(f"GRID SELL #{i}", symbol, quantity_per_grid, price, "ERROR", str(e))
            print(f"{Colors.RED}[ERROR]{Colors.ENDC} Grid SELL #{i} failed: {e}")
            orders_failed += 1

    # Summary
    print(f"\n{Colors.BLUE}[INFO]{Colors.ENDC} Grid deployment summary:")
    print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} {orders_placed} orders placed successfully")
    if orders_failed > 0:
        print(f"{Colors.RED}[ERROR]{Colors.ENDC} {orders_failed} orders failed")

if __name__ == "__main__":
    # Usage: python src/advanced/grid.py BTC/USDT 50000 0.001 5 1
    # (Center 50k, 0.001 BTC per order, 5 levels up/down, 1% distance)
    if len(sys.argv) < 6:
        print("Usage: python src/advanced/grid.py <symbol> <center_price> <qty> <levels> <step_%>")
    else:
        place_grid_orders(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]))