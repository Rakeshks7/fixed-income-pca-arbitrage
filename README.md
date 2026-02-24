# Fixed Income PCA & Yield Curve Arbitrage

![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Quant Finance](https://img.shields.io/badge/Domain-Quantitative_Finance-success.svg)

An institutional-grade fixed income quantitative model utilizing Principal Component Analysis (PCA) to extract the latent factors of the US Treasury yield curve (Level, Slope, Curvature). The project implements a duration-neutral 2s5s10s butterfly spread trading strategy designed to capitalize on mean-reverting curvature dislocations.

##  Overview

Professional Rates traders manage risk across the entire yield curve, not just isolated maturities. By applying dimensionality reduction (PCA) to historical Treasury yields, this engine mathematically isolates three primary drivers of curve movement:

1. **PC1 (Level):** Parallel shifts in the curve.
2. **PC2 (Slope):** Flattening or steepening of the curve.
3. **PC3 (Curvature):** The "butterfly" effect (belly vs. wings).

This framework identifies statistical anomalies in the curvature (PC3) and generates trading signals using a duration-matched, risk-neutral portfolio (Short 2Y, Long 5Y, Short 10Y) to capture mean reversion without taking directional interest rate risk.

##  Tech Stack
* **Language:** Python
* **Data Retrieval:** `pandas-datareader` (FRED API)
* **Quantitative Modeling:** `scikit-learn` (PCA), `numpy`, `scipy`
* **Data Processing:** `pandas`
* **Visualization:** `matplotlib`

## Methodology
* Data Ingestion: Fetches daily DGS2, DGS5, DGS10, and DGS30 yields.
* Factor Extraction: Standardizes daily yield changes and computes the covariance matrix to extract principal components.
* Duration Weighting: Calculates dynamic par duration for each node to ensure the butterfly portfolio maintains a net-zero DV01 (Dollar Value of 1 basis point).
* Signal Generation: Applies a rolling 252-day Z-score to the duration-neutral spread to identify $+2 \sigma$ or $-2 \sigma$ entry points.

## Disclaimer

For educational and research purposes only. The code and strategies presented in this repository do not constitute financial advice, investment recommendations, or an offer to buy or sell any securities. Quantitative models are subject to market risks, and historical performance is not indicative of future results. Use at your own risk.