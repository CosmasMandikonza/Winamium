# risk_management.py
import numpy as np
from typing import Dict, Optional

class RiskManager:
    def __init__(self, initial_capital: float = 10000):
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.max_drawdown_threshold = 0.15
        self.daily_loss_limit = 0.03
        self.position_limits = {}
        
    def calculate_kelly_criterion(self, win_rate: float, avg_win: float, avg_loss: float) -> float:
        """Calculate optimal position size using Kelly Criterion"""
        if avg_loss == 0:
            return 0
        
        b = avg_win / avg_loss
        p = win_rate
        q = 1 - p
        
        kelly = (b * p - q) / b
        
        # Apply conservative buffer (use 25% of Kelly)
        return max(0, min(kelly * 0.25, 0.1))
    
    def calculate_position_size(self, signal_strength: float, volatility: float) -> float:
        """Dynamic position sizing based on signal and volatility"""
        base_size = self.current_capital * 0.02  # 2% base risk
        
        # Adjust for signal strength
        signal_multiplier = min(signal_strength, 1.5)
        
        # Inverse volatility scaling
        volatility_multiplier = 1 / (1 + volatility)
        
        position_size = base_size * signal_multiplier * volatility_multiplier
        
        return min(position_size, self.current_capital * 0.05)  # Max 5% per trade
    
    def check_risk_limits(self, current_pnl: float) -> Dict[str, bool]:
        """Multi-layer risk checking"""
        checks = {
            "daily_limit_ok": current_pnl > -self.daily_loss_limit * self.initial_capital,
            "drawdown_ok": self.current_capital / self.initial_capital > (1 - self.max_drawdown_threshold),
            "position_concentration_ok": self._check_position_concentration()
        }
        
        return checks
    
    def _check_position_concentration(self) -> bool:
        """Ensure no single position is too large"""
        # Implementation depends on portfolio structure
        return True