import logging
import sys
import os
import json
from datetime import datetime
from dotenv import load_dotenv
import ccxt

# Load environment variables
load_dotenv()

# --- Logging Setup ---
def setup_logger():
    """Configures the logging system."""
    logger = logging.getLogger("BinanceBot")
    logger.setLevel(logging.INFO)
    
    # File Handler (saved to bot.log)
    file_handler = logging.FileHandler('bot.log')
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    
    # Console Handler (printed to screen)
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter('[%(levelname)s] %(message)s')
    console_handler.setFormatter(console_formatter)
    
    # Avoid duplicate logs if logger is already initialized
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    return logger

logger = setup_logger()

def log_trade(action, symbol, quantity, price=None, status="ATTEMPT", details=None):
    """Structured logging for trade actions."""
    msg = f"{action} | Symbol: {symbol} | Qty: {quantity}"
    if price:
        msg += f" | Price: {price}"
    msg += f" | Status: {status}"
    if details:
        msg += f" | Details: {details}"
    
    if status == "ERROR":
        logger.error(msg)
    elif status == "FILLED":
        logger.info(f"✅ {msg}")
    else:
        logger.info(msg)

# --- Validation Helper ---
def get_precision_and_limits(exchange, symbol):
    """
    Fetches the specific precision and limits for a symbol from Binance.
    This prevents 'Invalid Quantity' or 'Price Precision' errors.
    """
    try:
        markets = exchange.load_markets()
        market = markets[symbol]
        
        return {
            'amount_precision': market['precision']['amount'],
            'price_precision': market['precision']['price'],
            'min_amount': market['limits']['amount']['min'],
            'min_cost': market['limits']['cost']['min'], # Min value in USDT
        }
    except Exception as e:
        logger.error(f"Failed to fetch limits for {symbol}: {e}")
        raise

def validate_inputs(symbol, quantity, price=None, exchange=None):
    """Validates inputs against exchange rules."""
    if not isinstance(symbol, str):
        raise ValueError("Symbol must be a string (e.g., BTC/USDT).")
    
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")
    
    if price is not None and price <= 0:
        raise ValueError("Price must be greater than 0.")

    if exchange:
        limits = get_precision_and_limits(exchange, symbol)
        
        # Check Minimum Quantity
        if quantity < limits['min_amount']:
            raise ValueError(f"Quantity {quantity} is below minimum {limits['min_amount']} for {symbol}")
            
        # Check Minimum Notional Value (approximate)
        if price and (quantity * price) < limits['min_cost']:
            raise ValueError(f"Order value {quantity * price} is below minimum {limits['min_cost']} USDT")
            
    return True