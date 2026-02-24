import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Tuple
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)

class PCAModel:
    
    def __init__(self, n_components: int = 3):
        self.n_components = n_components
        self.pca = PCA(n_components=n_components)
        self.scaler = StandardScaler()
        self.explained_variance: np.ndarray = np.array([])
        self.components: pd.DataFrame = pd.DataFrame()

    def fit(self, yield_changes: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        logger.info("Fitting PCA model on yield changes...")

        scaled_data = self.scaler.fit_transform(yield_changes)

        factors = self.pca.fit_transform(scaled_data)
        self.explained_variance = self.pca.explained_variance_ratio_
        
        logger.info(f"Explained Variance by first {self.n_components} PCs: "
                    f"{np.cumsum(self.explained_variance)[-1]:.4%}")

        self.components = pd.DataFrame(
            self.pca.components_,
            columns=yield_changes.columns,
            index=[f'PC{i+1}' for i in range(self.n_components)]
        )
        
        factors_df = pd.DataFrame(
            factors, 
            index=yield_changes.index,
            columns=[f'PC{i+1}' for i in range(self.n_components)]
        )
        
        return self.components, factors_df

    def plot_loadings(self):
        if self.components.empty:
            raise ValueError("Model not fitted. Run fit() first.")
            
        plt.figure(figsize=(10, 6))
        for i in range(self.n_components):
            plt.plot(self.components.columns, self.components.iloc[i, :], 
                     marker='o', label=f'PC{i+1} ({self.explained_variance[i]:.1%})')
        
        plt.title('PCA Loadings: Level, Slope, Curvature')
        plt.xlabel('Maturity')
        plt.ylabel('Eigenvector Weight')
        plt.axhline(0, color='black', linestyle='--', linewidth=0.8)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()