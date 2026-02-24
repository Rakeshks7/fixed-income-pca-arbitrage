import logging
from datetime import datetime, timedelta

from src.data_loader import YieldCurveData
from src.pca_model import PCAModel
from src.pricer import ButterflyPricer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("RatesQuant_Main")

def main():
    logger.info("Starting Fixed Income PCA Arbitrage Pipeline...")

    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=365*20)).strftime('%Y-%m-%d') # 20 Years

    loader = YieldCurveData(start_date, end_date)
    yields = loader.fetch_fred_data()
    yield_changes = loader.get_daily_changes()

    pca_engine = PCAModel(n_components=3)
    loadings, factors = pca_engine.fit(yield_changes)
    
    print("\n--- Eigenvector Loadings ---")
    print(loadings)
    pca_engine.plot_loadings()

    pricer = ButterflyPricer(yields)
    fly_data = pricer.calculate_fly_spread()
    
    print("\n--- Recent Butterfly Positioning & Z-Scores ---")
    print(fly_data.tail())
    pricer.plot_trade_signals(fly_data)
    
    logger.info("Pipeline execution completed.")

if __name__ == "__main__":
    main()