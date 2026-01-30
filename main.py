import sys
import os

# Ensure Python can find the 'src' folder
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import your existing logic
from src.market_orders import place_market_order
from src.limit_orders import place_limit_order
from src.advanced.grid import place_grid_orders
from src.advanced.twap import execute_twap

def get_input(prompt, type_func=str):
    """
    Helper function to get input from the user and ensure it's the right type.
    """
    while True:
        try:
            value = input(prompt)
            if not value.strip(): continue  # Ignore empty inputs
            return type_func(value)
        except ValueError:
            print(f"❌ Invalid input. Please enter a valid {type_func.__name__}.")

def print_header():
    print("\n" + "="*45)
    print("       🤖 BINANCE FUTURES TRADING BOT       ")
    print("="*45)
    print("1. 🚀 Place Market Order  (Instant)")
    print("2. 🎯 Place Limit Order   (Target Price)")
    print("3. 🕸️  Run Grid Strategy   (Bonus)")
    print("4. ⏳ Run TWAP Strategy   (Advanced)")
    print("5. 🚪 Exit")
    print("-" * 45)

def main():
    while True:
        print_header()
        choice = input("👉 Select an action (1-5): ").strip()

        try:
            # --- OPTION 1: MARKET ORDER ---
            if choice == '1':
                print("\n--- 🚀 Market Order Setup ---")
                symbol = get_input("   Enter Symbol (e.g., BTC/USDT): ").upper()
                side = get_input("   Enter Side (buy/sell): ").lower()
                qty = get_input("   Enter Quantity: ", float)
                
                print(f"\n   [Confirm] Buying {qty} {symbol} at Market Price?")
                if input("   Type 'y' to confirm: ").lower() == 'y':
                    place_market_order(symbol, side, qty)
                else:
                    print("   ❌ Cancelled.")

            # --- OPTION 2: LIMIT ORDER ---
            elif choice == '2':
                print("\n--- 🎯 Limit Order Setup ---")
                symbol = get_input("   Enter Symbol (e.g., BTC/USDT): ").upper()
                side = get_input("   Enter Side (buy/sell): ").lower()
                qty = get_input("   Enter Quantity: ", float)
                price = get_input("   Enter Target Price: ", float)
                
                place_limit_order(symbol, side, qty, price)

            # --- OPTION 3: GRID STRATEGY ---
            elif choice == '3':
                print("\n--- 🕸️  Grid Strategy Setup ---")
                symbol = get_input("   Enter Symbol (e.g., BTC/USDT): ").upper()
                center = get_input("   Center Price: ", float)
                qty = get_input("   Qty per Grid Level: ", float)
                levels = get_input("   Number of Levels (e.g., 5): ", int)
                step = get_input("   Step % (e.g., 1 for 1%): ", float)
                
                place_grid_orders(symbol, center, qty, levels, step)

            # --- OPTION 4: TWAP STRATEGY ---
            elif choice == '4':
                print("\n--- ⏳ TWAP Strategy Setup ---")
                symbol = get_input("   Enter Symbol (e.g., BTC/USDT): ").upper()
                side = get_input("   Enter Side (buy/sell): ").lower()
                total_qty = get_input("   Total Quantity to Trade: ", float)
                duration = get_input("   Duration (in minutes): ", int)
                chunks = get_input("   Split into how many orders?: ", int)
                
                execute_twap(symbol, side, total_qty, duration, chunks)

            # --- OPTION 5: EXIT ---
            elif choice == '5':
                print("\nExiting... Good luck with your trading! 👋")
                break
            
            else:
                print("\n❌ Invalid choice. Please select 1-5.")

        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
        
        # Pause so the user can see the result before the menu clears
        input("\nPress Enter to return to menu...")

if __name__ == "__main__":
    main()