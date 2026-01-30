import time
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.config import get_exchange
from src.utils import log_trade

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m'

def execute_twap(symbol, side, total_qty, duration_minutes, num_orders):
    """
    Execute Time-Weighted Average Price (TWAP) strategy.
    Divides a large order into smaller chunks executed at regular intervals.
    
    Args:
        symbol: Trading pair (e.g., BTC/USDT)
        side: Order side (buy/sell)
        total_qty: Total quantity to trade
        duration_minutes: Duration over which to spread orders
        num_orders: Number of order chunks
    """
    exchange = get_exchange()
    
    chunk_size = total_qty / num_orders
    interval = (duration_minutes * 60) / num_orders
    
    print(f"\n{Colors.BLUE}[INFO]{Colors.ENDC} TWAP Execution Started")
    print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Pair: {symbol} | Side: {side.upper()}")
    print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Total Qty: {total_qty} | Duration: {duration_minutes} min | Chunks: {num_orders}")
    print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Chunk Size: {chunk_size:.6f} | Interval: {interval:.1f} sec\n")
    
    successful_orders = 0
    failed_orders = 0
    
    for i in range(num_orders):
        try:
            print(f"{Colors.YELLOW}[TWAP]{Colors.ENDC} Executing batch {i+1}/{num_orders}...")
            
            # Place market order
            order = exchange.create_order(symbol, 'market', side, chunk_size)
            log_trade(f"TWAP BATCH {i+1}/{num_orders}", symbol, chunk_size, order['average'], "FILLED")
            
            print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} Batch {i+1} executed at {order['average']:.4f}")
            successful_orders += 1
            
            if i < num_orders - 1:
                print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Waiting {interval:.1f} seconds before next batch...\n")
                time.sleep(interval)
                
        except Exception as e:
            log_trade("TWAP ERROR", symbol, chunk_size, status="ERROR", details=str(e))
            print(f"{Colors.RED}[ERROR]{Colors.ENDC} Batch {i+1} failed: {e}\n")
            failed_orders += 1
            
            if i < num_orders - 1:
                print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Retrying in {interval:.1f} seconds...\n")
                time.sleep(interval)
    
    # Summary
    print(f"\n{Colors.BLUE}[INFO]{Colors.ENDC} TWAP Execution Summary:")
    print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} {successful_orders} batches completed successfully")
    if failed_orders > 0:
        print(f"{Colors.RED}[ERROR]{Colors.ENDC} {failed_orders} batches failed")
    print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Total executed: {successful_orders * chunk_size:.6f} {symbol}")

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: python src/advanced/twap.py <symbol> <buy/sell> <total_qty> <duration_min> <num_chunks>")
    else:
        execute_twap(sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))