import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.config import get_exchange
from src.utils import log_trade, validate_inputs

def place_grid_orders(symbol, center_price, quantity_per_grid, grid_levels, grid_step_percent):
    """
    Places a grid of buy orders below and sell orders above a center price.
    """
    exchange = get_exchange()
    
    print(f"Starting Grid Strategy for {symbol}...")
    print(f"Center: {center_price} | Levels: {grid_levels} | Step: {grid_step_percent}%")

    # 1. Place Buy Orders (Below Center)
    for i in range(1, grid_levels + 1):
        price = center_price * (1 - (i * grid_step_percent / 100))
        try:
            exchange.create_order(symbol, 'limit', 'buy', quantity_per_grid, price)
            log_trade(f"GRID BUY #{i}", symbol, quantity_per_grid, price, "OPEN")
            print(f"Placed Grid BUY at {price:.2f}")
        except Exception as e:
            log_trade(f"GRID BUY #{i}", symbol, quantity_per_grid, price, "ERROR", str(e))

    # 2. Place Sell Orders (Above Center)
    for i in range(1, grid_levels + 1):
        price = center_price * (1 + (i * grid_step_percent / 100))
        try:
            exchange.create_order(symbol, 'limit', 'sell', quantity_per_grid, price)
            log_trade(f"GRID SELL #{i}", symbol, quantity_per_grid, price, "OPEN")
            print(f"Placed Grid SELL at {price:.2f}")
        except Exception as e:
            log_trade(f"GRID SELL #{i}", symbol, quantity_per_grid, price, "ERROR", str(e))

if __name__ == "__main__":
    # Usage: python src/advanced/grid.py BTC/USDT 50000 0.001 5 1
    # (Center 50k, 0.001 BTC per order, 5 levels up/down, 1% distance)
    if len(sys.argv) < 6:
        print("Usage: python src/advanced/grid.py <symbol> <center_price> <qty> <levels> <step_%>")
    else:
        place_grid_orders(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]))