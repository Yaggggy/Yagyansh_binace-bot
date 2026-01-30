import logging
from dotenv import load_dotenv

load_dotenv()

class MockExchange:
    """
    A standalone Simulation Exchange.
    It implements the same methods as CCXT (create_order, load_markets)
    but runs locally without any network connection.
    """
    
    def __init__(self, config={}):
        self.id = 'binance'
        self.name = 'Binance Futures (Simulation)'
        self.iso8601 = '2023-10-27T10:00:00Z'
        self.urls = {'api': 'https://testnet.binancefuture.com/fapi/v1'}
        
        # Define market rules (Mocking what CCXT usually downloads)
        self.markets = {
            'BTC/USDT': {
                'symbol': 'BTC/USDT',
                'precision': {'amount': 3, 'price': 2},
                'limits': {'amount': {'min': 0.001}, 'cost': {'min': 5.0}},
                'active': True
            },
            'ETH/USDT': {
                'symbol': 'ETH/USDT',
                'precision': {'amount': 3, 'price': 2},
                'limits': {'amount': {'min': 0.01}, 'cost': {'min': 5.0}},
                'active': True
            }
        }

    def load_markets(self, reload=False):
        """Simulates fetching market rules from the exchange."""
        return self.markets

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        """
        Simulates placing an order.
        Returns a dictionary structure identical to a real CCXT response.
        """
        print(f"   [SIMULATION] Sending {type.upper()} {side.upper()} order for {amount} {symbol}...")
        
        # Mock Response
        return {
            'id': '123456789',  # Fake Order ID
            'datetime': self.iso8601,
            'symbol': symbol,
            'type': type,
            'side': side,
            'amount': amount,
            'price': price if price else 50000.00,  # Use price if Limit, else mock market price
            'average': 50000.00,
            'status': 'closed',
            'filled': amount,
            'remaining': 0.0,
            'info': {'msg': 'Simulation Mode - Order Successful'}
        }

def get_exchange():
    """
    Returns the Simulation Exchange.
    """
    print("\n✅  Bot initialized in PURE SIMULATION MODE.")
    print("    (No network calls, no API keys required)\n")
    return MockExchange()