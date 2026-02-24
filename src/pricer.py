import logging
import pandas as pd
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

class ButterflyPricer:
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.maturities = {'2Y': 2, '5Y': 5, '10Y': 10}
        
    def estimate_par_duration(self, yield_pct: float, maturity: int) -> float:
        y_decimal = yield_pct / 100.0
        if y_decimal == 0:
            return float(maturity)
        return (1 - (1 + y_decimal)**-maturity) / y_decimal

    def calculate_fly_spread(self) -> pd.DataFrame:
        logger.info("Calculating duration-neutral 2s5s10s butterfly spread...")
        
        fly_records = []
        
        for date, row in self.data.iterrows():
            y2, y5, y10 = row['2Y'], row['5Y'], row['10Y']

            d2 = self.estimate_par_duration(y2, self.maturities['2Y'])
            d5 = self.estimate_par_duration(y5, self.maturities['5Y'])
            d10 = self.estimate_par_duration(y10, self.maturities['10Y'])

            w5 = 1.0  
            w2 = -0.5 * (d5 / d2)  
            w10 = -0.5 * (d5 / d10)

            fly_yield = (w2 * y2) + (w5 * y5) + (w10 * y10)
            fly_records.append({'Date': date, 'Fly_Yield': fly_yield, 'W2': w2, 'W5': w5, 'W10': w10})
            
        df_fly = pd.DataFrame(fly_records).set_index('Date')

        df_fly['Rolling_Mean'] = df_fly['Fly_Yield'].rolling(window=252).mean()
        df_fly['Rolling_Std'] = df_fly['Fly_Yield'].rolling(window=252).std()
        df_fly['Z_Score'] = (df_fly['Fly_Yield'] - df_fly['Rolling_Mean']) / df_fly['Rolling_Std']
        
        return df_fly.dropna()

    def plot_trade_signals(self, fly_data: pd.DataFrame):
        plt.figure(figsize=(12, 6))
        plt.plot(fly_data.index, fly_data['Z_Score'], label='2s5s10s Fly Z-Score', color='blue')
        plt.axhline(2, color='red', linestyle='--', label='Short Belly Signal (Mean Revert Down)')
        plt.axhline(-2, color='green', linestyle='--', label='Long Belly Signal (Mean Revert Up)')
        plt.axhline(0, color='black', linewidth=1)
        
        plt.title('2s5s10s Butterfly Z-Score (Duration Neutral)')
        plt.ylabel('Z-Score')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()