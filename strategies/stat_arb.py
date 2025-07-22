# strategies/stat_arb.py
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
import ta

class StatisticalArbitrageStrategy:
    def __init__(self, lookback_period=20, n_pairs=10):
        self.lookback_period = lookback_period
        self.n_pairs = n_pairs
        self.models = {}
        self.scaler = StandardScaler()
        
    def identify_cointegrated_pairs(self, price_data: pd.DataFrame) -> List[tuple]:
        """Find cointegrated crypto pairs using statistical tests"""
        # Implement cointegration test (Johansen or Engle-Granger)
        pairs = []
        assets = price_data.columns
        
        for i in range(len(assets)):
            for j in range(i+1, len(assets)):
                # Calculate correlation and cointegration
                corr = price_data[assets[i]].corr(price_data[assets[j]])
                if corr > 0.7:  # High correlation threshold
                    pairs.append((assets[i], assets[j], corr))
        
        return sorted(pairs, key=lambda x: x[2], reverse=True)[:self.n_pairs]
    
    def calculate_spread_features(self, pair_data: pd.DataFrame) -> pd.DataFrame:
        """Calculate features for ML model"""
        features = pd.DataFrame()
        
        # Price spread
        features['spread'] = pair_data.iloc[:, 0] - pair_data.iloc[:, 1]
        features['spread_ma'] = features['spread'].rolling(20).mean()
        features['spread_std'] = features['spread'].rolling(20).std()
        features['z_score'] = (features['spread'] - features['spread_ma']) / features['spread_std']
        
        # Technical indicators
        features['rsi_1'] = ta.momentum.RSIIndicator(pair_data.iloc[:, 0]).rsi()
        features['rsi_2'] = ta.momentum.RSIIndicator(pair_data.iloc[:, 1]).rsi()
        features['volume_ratio'] = pair_data.iloc[:, 0].rolling(10).mean() / pair_data.iloc[:, 1].rolling(10).mean()
        
        return features.dropna()
    
    def train_ml_model(self, features: pd.DataFrame, signals: pd.Series):
        """Train ensemble ML model for signal generation"""
        X = self.scaler.fit_transform(features)
        
        # Ensemble of models
        rf = RandomForestClassifier(n_estimators=100, max_depth=5)
        gb = GradientBoostingClassifier(n_estimators=100, max_depth=3)
        
        rf.fit(X, signals)
        gb.fit(X, signals)
        
        self.models = {'rf': rf, 'gb': gb}
    
    def generate_signals(self, current_features: pd.DataFrame) -> Dict:
        """Generate trading signals using ML ensemble"""
        X = self.scaler.transform(current_features)
        
        # Ensemble prediction
        rf_pred = self.models['rf'].predict_proba(X)[0]
        gb_pred = self.models['gb'].predict_proba(X)[0]
        
        # Weighted average (can be optimized)
        ensemble_prob = 0.6 * rf_pred + 0.4 * gb_pred
        
        # Generate signal only if high confidence (>90th percentile)
        if ensemble_prob[1] > 0.9:  # Buy signal
            return {"action": "buy", "confidence": ensemble_prob[1]}
        elif ensemble_prob[0] > 0.9:  # Sell signal
            return {"action": "sell", "confidence": ensemble_prob[0]}
        else:
            return {"action": "hold", "confidence": max(ensemble_prob)}