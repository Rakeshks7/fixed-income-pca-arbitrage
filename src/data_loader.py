import logging
import pandas as pd
import pandas_datareader.data as web

logger = logging.getLogger(__name__)

class YieldCurveData:
    
    TICKERS = {
        '2Y': 'DGS2',
        '5Y': 'DGS5',
        '10Y': 'DGS10',
        '30Y': 'DGS30'
    }

    def __init__(self, start_date: str, end_date: str):
        self.start_date = start_date
        self.end_date = end_date
        self.data: pd.DataFrame = pd.DataFrame()

    def fetch_fred_data(self) -> pd.DataFrame:
        logger.info(f"Fetching FRED data from {self.start_date} to {self.end_date}...")
        try:
            df = web.DataReader(
                list(self.TICKERS.values()), 
                'fred', 
                self.start_date, 
                self.end_date
            )
            df.columns = list(self.TICKERS.keys())
            
            # Forward fill missing data (weekends/holidays), then drop remaining NAs
            self.data = df.ffill().dropna()
            logger.info(f"Data fetched successfully. Shape: {self.data.shape}")
            return self.data
        except Exception as e:
            logger.error(f"Failed to fetch data from FRED: {e}")
            raise

    def get_daily_changes(self) -> pd.DataFrame:
        if self.data.empty:
            raise ValueError("Data not loaded. Call fetch_fred_data() first.")
        return self.data.diff().dropna()