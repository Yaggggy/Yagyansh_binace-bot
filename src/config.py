import ccxt
from dotenv import load_dotenv

load_dotenv()

class MockExchange(ccxt.binance):
    def __init__(self, config={}):
        super().__init__(config)
        self.urls['api'] = 'https://testnet.binancefuture.com/fapi/v1' 

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        print(f"   [MOCK] Simulating {side} order for {amount} {symbol}...")
        return {
            'id': '123456789',
            'symbol': symbol,
            'type': type,
            'side': side,
            'amount': amount,
            'price': price if price else 50000.00,
            'average': 50000.00,
            'status': 'closed',
            'info': {'mock': True}
        }

    def fetch_limits(self, symbol):
        return {'limits': {'amount': {'min': 0.001}, 'cost': {'min': 5.0}}}

def get_exchange():
    return MockExchange({
        'apiKey': 'mock_key',
        'secret': 'mock_secret',
        'options': {'defaultType': 'future'},
    })