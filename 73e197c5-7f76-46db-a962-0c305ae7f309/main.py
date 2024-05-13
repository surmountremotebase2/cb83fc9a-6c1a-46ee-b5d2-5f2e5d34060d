from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "MANGO"  # Replace 'MANGO' with the actual ticker

    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        return "1day"

    def run(self, data):
        # Retrieve closing prices for the SMA calculations
        closing_prices = [entry[self.ticker]["close"] for entry in data["ohlcv"] if self.ticker in entry]
        
        # Calculate the 50-day and 200-day SMAs
        sma_short = SMA(self.ticker, data["ohlcv"], length=50)
        sma_long = SMA(self.ticker, data["ohlcv"], length=200)
        
        # Check if enough data is available to compute both SMAs
        if not sma_short or not sma_long or len(sma_short) < 200 or len(sma_long) < 200:
            log("Not enough data for SMA calculations.")
            return TargetAllocation({})
        
        # Determine the trading signal based on the SMA crossover
        # Buy when SMA(50) is above SMA(200), sell/avoid otherwise
        current_position = sma_short[-1] > sma_long[-1]
        mango_stake = 1.0 if current_position else 0.0

        log(f"Current SMA(50): {sma_short[-1]}, SMA(200): {sma_long[-1]}, Trading Signal: {'Buy' if current_position else 'Sell'}")

        return TargetAllocation({self.ticker: mango_stake})