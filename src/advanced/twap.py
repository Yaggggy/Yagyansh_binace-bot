import time
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.config import get_exchange
from src.utils import log_trade

def execute_twap(symbol, side, total_qty, duration_minutes, num_orders):
    exchange = get_exchange()
    
    chunk_size = total_qty / num_orders
    interval = (duration_minutes * 60) / num_orders
    
    print(f"Starting TWAP: {side} {total_qty} {symbol} over {duration_minutes}m in {num_orders} batches.")
    
    for i in range(num_orders):
        try:
            # Place small market order
            order = exchange.create_order(symbol, 'market', side, chunk_size)
            log_trade(f"TWAP BATCH {i+1}/{num_orders}", symbol, chunk_size, order['average'], "FILLED")
            
            if i < num_orders - 1:
                print(f"Sleeping for {interval} seconds...")
                time.sleep(interval)
                
        except Exception as e:
            log_trade("TWAP ERROR", symbol, chunk_size, status="ERROR")
            print(f"Error in batch {i}: {e}")
            break

if __name__ == "__main__":

    execute_twap(sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))