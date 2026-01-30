import sys
import os
import time
from datetime import datetime

# Ensure Python can find the 'src' folder
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import your existing logic
from src.market_orders import place_market_order
from src.limit_orders import place_limit_order
from src.advanced.grid import place_grid_orders
from src.advanced.twap import execute_twap
from src.advanced.stop_limit import place_stop_limit_order
from src.advanced.oco import place_futures_oco

# Color codes for professional output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def format_timestamp():
    """Returns current timestamp in professional format."""
    return datetime.now().strftime("%H:%M:%S")

def log_info(message):
    """Logs info message with timestamp."""
    print(f"{Colors.BLUE}[INFO {format_timestamp()}]{Colors.ENDC} {message}")

def log_success(message):
    """Logs success message with timestamp."""
    print(f"{Colors.GREEN}[SUCCESS {format_timestamp()}]{Colors.ENDC} {message}")

def log_warning(message):
    """Logs warning message with timestamp."""
    print(f"{Colors.YELLOW}[WARNING {format_timestamp()}]{Colors.ENDC} {message}")

def log_error(message):
    """Logs error message with timestamp."""
    print(f"{Colors.RED}[ERROR {format_timestamp()}]{Colors.ENDC} {message}")

def get_input(prompt, type_func=str, allow_empty=False):
    """
    Get validated input from user with proper error handling.
    Args:
        prompt: The input prompt to display
        type_func: Function to convert input type (str, float, int)
        allow_empty: Allow empty input
    """
    while True:
        try:
            value = input(f"{Colors.BLUE}{prompt}{Colors.ENDC}").strip()
            if not value and not allow_empty:
                log_error(f"Input cannot be empty. Please provide a value.")
                continue
            if not value and allow_empty:
                return None
            return type_func(value)
        except ValueError:
            log_error(f"Invalid input format. Expected {type_func.__name__}.")
        except KeyboardInterrupt:
            log_warning("Operation cancelled by user.")
            return None
        except Exception as e:
            log_error(f"Unexpected error: {e}")

def print_header():
    """Display main menu header."""
    print("\n" + "="*60)
    print(f"{Colors.BOLD}{Colors.HEADER}BINANCE FUTURES TRADING BOT - MAIN MENU{Colors.ENDC}")
    print("="*60)
    print(f"  {Colors.BOLD}1. Market Order{Colors.ENDC}        - Execute orders at current market price")
    print(f"  {Colors.BOLD}2. Limit Order{Colors.ENDC}         - Place orders at specific price targets")
    print(f"  {Colors.BOLD}3. Stop-Limit Order{Colors.ENDC}    - Trigger limit order at stop price")
    print(f"  {Colors.BOLD}4. Grid Strategy{Colors.ENDC}       - Automated grid trading setup")
    print(f"  {Colors.BOLD}5. TWAP Strategy{Colors.ENDC}       - Time-weighted average price execution")
    print(f"  {Colors.BOLD}6. OCO Strategy{Colors.ENDC}        - One-Cancels-Other (TP/SL orders)")
    print(f"  {Colors.BOLD}7. Exit{Colors.ENDC}                - Terminate the application")
    print("-"*60)

def main():
    """Main application loop with interactive menu."""
    log_info("Starting Binance Futures Trading Bot")
    log_info("Simulation mode enabled - No real trades will be executed")
    
    while True:
        try:
            print_header()
            choice = get_input(">> Select an action (1-7): ").strip()

            # --- OPTION 1: MARKET ORDER ---
            if choice == '1':
                log_info("Initializing market order setup...")
                print("\n" + "-"*60)
                print(f"{Colors.BOLD}MARKET ORDER CONFIGURATION{Colors.ENDC}")
                print("-"*60)
                
                symbol = get_input("   Enter trading pair (e.g., BTC/USDT): ")
                if symbol is None:
                    continue
                symbol = symbol.upper()
                
                side = get_input("   Enter side [BUY/SELL]: ")
                if side is None:
                    continue
                side = side.lower()
                
                quantity = get_input("   Enter quantity to trade: ", float)
                if quantity is None:
                    continue
                
                # Confirmation step
                print(f"\n{Colors.BOLD}Order Summary:{Colors.ENDC}")
                print(f"  Pair:     {symbol}")
                print(f"  Side:     {side.upper()}")
                print(f"  Quantity: {quantity}")
                
                confirm = input(f"\n{Colors.BLUE}Type 'confirm' to proceed: {Colors.ENDC}").strip().lower()
                if confirm == 'confirm':
                    log_info(f"Executing market order: {side.upper()} {quantity} {symbol}")
                    place_market_order(symbol, side, quantity)
                else:
                    log_warning("Market order cancelled.")

            # --- OPTION 2: LIMIT ORDER ---
            elif choice == '2':
                log_info("Initializing limit order setup...")
                print("\n" + "-"*60)
                print(f"{Colors.BOLD}LIMIT ORDER CONFIGURATION{Colors.ENDC}")
                print("-"*60)
                
                symbol = get_input("   Enter trading pair (e.g., BTC/USDT): ")
                if symbol is None:
                    continue
                symbol = symbol.upper()
                
                side = get_input("   Enter side [BUY/SELL]: ")
                if side is None:
                    continue
                side = side.lower()
                
                quantity = get_input("   Enter quantity to trade: ", float)
                if quantity is None:
                    continue
                
                price = get_input("   Enter target price: ", float)
                if price is None:
                    continue
                
                # Confirmation step
                print(f"\n{Colors.BOLD}Order Summary:{Colors.ENDC}")
                print(f"  Pair:     {symbol}")
                print(f"  Side:     {side.upper()}")
                print(f"  Quantity: {quantity}")
                print(f"  Price:    {price}")
                
                confirm = input(f"\n{Colors.BLUE}Type 'confirm' to proceed: {Colors.ENDC}").strip().lower()
                if confirm == 'confirm':
                    log_info(f"Executing limit order: {side.upper()} {quantity} {symbol} @ {price}")
                    place_limit_order(symbol, side, quantity, price)
                else:
                    log_warning("Limit order cancelled.")

            # --- OPTION 3: STOP-LIMIT ORDER ---
            elif choice == '3':
                log_info("Initializing stop-limit order setup...")
                print("\n" + "-"*60)
                print(f"{Colors.BOLD}STOP-LIMIT ORDER CONFIGURATION{Colors.ENDC}")
                print("-"*60)
                print("A stop-limit order triggers a limit order when the stop price is reached.\n")
                
                symbol = get_input("   Enter trading pair (e.g., BTC/USDT): ")
                if symbol is None:
                    continue
                symbol = symbol.upper()
                
                side = get_input("   Enter side [BUY/SELL]: ")
                if side is None:
                    continue
                side = side.lower()
                
                quantity = get_input("   Enter quantity to trade: ", float)
                if quantity is None:
                    continue
                
                stop_price = get_input("   Enter stop price (trigger price): ", float)
                if stop_price is None:
                    continue
                
                limit_price = get_input("   Enter limit price (execution price): ", float)
                if limit_price is None:
                    continue
                
                # Confirmation step
                print(f"\n{Colors.BOLD}Order Summary:{Colors.ENDC}")
                print(f"  Pair:         {symbol}")
                print(f"  Side:         {side.upper()}")
                print(f"  Quantity:     {quantity}")
                print(f"  Stop Price:   {stop_price} (triggers order)")
                print(f"  Limit Price:  {limit_price} (execution price)")
                
                confirm = input(f"\n{Colors.BLUE}Type 'confirm' to proceed: {Colors.ENDC}").strip().lower()
                if confirm == 'confirm':
                    log_info(f"Executing stop-limit order: {side.upper()} {quantity} {symbol}")
                    place_stop_limit_order(symbol, side, quantity, stop_price, limit_price)
                else:
                    log_warning("Stop-limit order cancelled.")

            # --- OPTION 4: GRID STRATEGY ---
            elif choice == '4':
                log_info("Initializing grid trading strategy...")
                print("\n" + "-"*60)
                print(f"{Colors.BOLD}GRID STRATEGY CONFIGURATION{Colors.ENDC}")
                print("-"*60)
                print("Grid trading places orders at regular intervals above and below")
                print("a center price, allowing automated profit-taking at multiple levels.\n")
                
                symbol = get_input("   Enter trading pair (e.g., BTC/USDT): ")
                if symbol is None:
                    continue
                symbol = symbol.upper()
                
                center_price = get_input("   Enter center price (base reference): ", float)
                if center_price is None:
                    continue
                
                quantity = get_input("   Enter quantity per grid level: ", float)
                if quantity is None:
                    continue
                
                levels = get_input("   Number of grid levels (up and down): ", int)
                if levels is None:
                    continue
                
                step_percent = get_input("   Step percentage between levels (e.g., 1 for 1%): ", float)
                if step_percent is None:
                    continue
                
                # Confirmation step
                print(f"\n{Colors.BOLD}Grid Strategy Summary:{Colors.ENDC}")
                print(f"  Pair:              {symbol}")
                print(f"  Center Price:      {center_price}")
                print(f"  Qty per Level:     {quantity}")
                print(f"  Grid Levels:       {levels} (both sides)")
                print(f"  Step:              {step_percent}%")
                print(f"  Total Orders:      {levels * 2}")
                
                confirm = input(f"\n{Colors.BLUE}Type 'confirm' to proceed: {Colors.ENDC}").strip().lower()
                if confirm == 'confirm':
                    log_info(f"Deploying grid strategy with {levels * 2} orders")
                    place_grid_orders(symbol, center_price, quantity, levels, step_percent)
                else:
                    log_warning("Grid strategy cancelled.")

            # --- OPTION 5: TWAP STRATEGY ---
            elif choice == '5':
                log_info("Initializing TWAP strategy...")
                print("\n" + "-"*60)
                print(f"{Colors.BOLD}TIME-WEIGHTED AVERAGE PRICE (TWAP) CONFIGURATION{Colors.ENDC}")
                print("-"*60)
                print("TWAP divides a large order into smaller chunks executed")
                print("at regular intervals to minimize market impact.\n")
                
                symbol = get_input("   Enter trading pair (e.g., BTC/USDT): ")
                if symbol is None:
                    continue
                symbol = symbol.upper()
                
                side = get_input("   Enter side [BUY/SELL]: ")
                if side is None:
                    continue
                side = side.lower()
                
                total_quantity = get_input("   Enter total quantity to trade: ", float)
                if total_quantity is None:
                    continue
                
                duration_minutes = get_input("   Duration in minutes: ", int)
                if duration_minutes is None:
                    continue
                
                num_chunks = get_input("   Number of execution chunks: ", int)
                if num_chunks is None:
                    continue
                
                # Calculate chunk details
                chunk_size = total_quantity / num_chunks
                interval_seconds = (duration_minutes * 60) / num_chunks
                
                # Confirmation step
                print(f"\n{Colors.BOLD}TWAP Strategy Summary:{Colors.ENDC}")
                print(f"  Pair:              {symbol}")
                print(f"  Side:              {side.upper()}")
                print(f"  Total Quantity:    {total_quantity}")
                print(f"  Duration:          {duration_minutes} minutes")
                print(f"  Number of Chunks:  {num_chunks}")
                print(f"  Size per Chunk:    {chunk_size:.6f}")
                print(f"  Interval:          ~{interval_seconds:.1f} seconds")
                
                confirm = input(f"\n{Colors.BLUE}Type 'confirm' to proceed: {Colors.ENDC}").strip().lower()
                if confirm == 'confirm':
                    log_info(f"Starting TWAP execution: {side.upper()} {total_quantity} {symbol}")
                    execute_twap(symbol, side, total_quantity, duration_minutes, num_chunks)
                else:
                    log_warning("TWAP strategy cancelled.")

            # --- OPTION 6: OCO STRATEGY ---
            elif choice == '6':
                log_info("Initializing OCO strategy...")
                print("\n" + "-"*60)
                print(f"{Colors.BOLD}ONE-CANCELS-OTHER (OCO) CONFIGURATION{Colors.ENDC}")
                print("-"*60)
                print("OCO places entry, take-profit, and stop-loss orders simultaneously.\n")
                
                symbol = get_input("   Enter trading pair (e.g., BTC/USDT): ")
                if symbol is None:
                    continue
                symbol = symbol.upper()
                
                side = get_input("   Enter side [BUY/SELL]: ")
                if side is None:
                    continue
                side = side.lower()
                
                quantity = get_input("   Enter quantity to trade: ", float)
                if quantity is None:
                    continue
                
                tp_price = get_input("   Enter take-profit price: ", float)
                if tp_price is None:
                    continue
                
                sl_price = get_input("   Enter stop-loss price: ", float)
                if sl_price is None:
                    continue
                
                # Confirmation step
                print(f"\n{Colors.BOLD}OCO Strategy Summary:{Colors.ENDC}")
                print(f"  Pair:              {symbol}")
                print(f"  Side:              {side.upper()}")
                print(f"  Quantity:          {quantity}")
                print(f"  Take Profit:       {tp_price}")
                print(f"  Stop Loss:         {sl_price}")
                
                confirm = input(f"\n{Colors.BLUE}Type 'confirm' to proceed: {Colors.ENDC}").strip().lower()
                if confirm == 'confirm':
                    log_info(f"Deploying OCO strategy for {symbol}")
                    place_futures_oco(symbol, side, quantity, tp_price, sl_price)
                else:
                    log_warning("OCO strategy cancelled.")

            # --- OPTION 7: EXIT ---
            elif choice == '7':
                log_info("Shutdown command received")
                print(f"\n{Colors.GREEN}Thank you for using Binance Futures Trading Bot.{Colors.ENDC}")
                print(f"{Colors.GREEN}Exiting safely...{Colors.ENDC}\n")
                break
            
            else:
                log_error("Invalid selection. Please choose an option between 1 and 7.")
                continue

        except KeyboardInterrupt:
            print()
            log_warning("Application interrupted by user")
            break
        except Exception as e:
            log_error(f"Unexpected error in main loop: {e}")
            print(f"Stack trace: {type(e).__name__}")
        
        # Pause so the user can see the result before the menu clears
        input(f"\n{Colors.BLUE}Press Enter to continue...{Colors.ENDC}")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()