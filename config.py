"""
Configuration module for Dynamic Portfolio Allocator
Centralized configuration with environment variable fallbacks
"""
import os
from dataclasses import dataclass
from typing import List, Dict, Any
from enum import Enum

class AssetClass(Enum):
    """Asset class classification for portfolio construction"""
    EQUITY = "equity"
    CRYPTO = "crypto"
    BOND = "bond"
    COMMODITY = "commodity"
    CASH = "cash"

class RiskProfile(Enum):
    """Investor risk profile classifications"""
    CONSERVATIVE = "conservative"  # 20% max equity exposure
    MODERATE = "moderate"          # 50% max equity exposure
    AGGRESSIVE = "aggressive"     # 80% max equity exposure

@dataclass
class PortfolioConfig:
    """Portfolio configuration parameters"""
    # Core parameters
    initial_capital: float = 10000.0
    max_position_size: float = 0.25  # Maximum 25% in single asset
    min_position_size: float = 0.02   # Minimum 2% position
    rebalance_threshold: float = 0.05  # 5% deviation triggers rebalance
    max_leverage: float = 1.0  # No leverage by default
    
    # Risk parameters
    max_drawdown_limit: float = 0.15  # 15% max drawdown
    var_confidence: float = 0.95  # 95% VaR confidence
    max_concentration: Dict[AssetClass, float] = None
    
    # Transaction parameters
    max_transactions_per_day: int = 5
    transaction_fee_rate: float = 0.001  # 0.1% transaction fee
    
    def __post_init__(self):
        """Initialize default concentration limits"""
        if self.max_concentration is None:
            self.max_concentration = {
                AssetClass.EQUITY: 0.6,
                AssetClass.CRYPTO: 0.3,
                AssetClass.BOND: 0.4,
                AssetClass.COMMODITY: 0.2,
                AssetClass.CASH: 0.1
            }

@dataclass
class DataConfig:
    """Data source configuration"""
    # API configurations with environment variable fallbacks
    ccxt_exchange: str = "binance"
    ccxt_timeframe: str = "1h"
    max_retries: int = 3
    request_timeout: int = 30
    
    # Data retention
    max_data_points: int = 1000
    cache_ttl_seconds: int = 300  # 5 minutes cache
    
    # Default watchlist
    default_symbols: List[str] = None
    
    def __post_init__(self):
        """Initialize default symbols"""
        if self.default_symbols is None:
            self.default_symbols = [
                "BTC/USDT", "ETH/USDT", "SPY", "QQQ", 
                "TLT", "GLD", "BND", "VTI"
            ]

# Load from environment variables with defaults
def load_config() -> Dict[str, Any]:
    """Load configuration from environment variables"""
    config = {
        "portfolio": PortfolioConfig(
            initial_capital=float(os.getenv("INITIAL_CAPITAL", "10000.0")),
            max_position_size=float(os.getenv("MAX_POSITION_SIZE", "0.25")),
            rebalance_threshold=float(os.getenv("REBALANCE_THRESHOLD", "0.05"))
        ),
        "data": DataConfig(),
        "firebase": {
            "project_id": os.getenv("FIREBASE_PROJECT_ID", "portfolio-optimizer"),
            "credentials_path": os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
        },
        "logging": {
            "level": os.getenv("LOG_LEVEL", "INFO"),
            "file": os.getenv("LOG_FILE", "portfolio_allocator.log")
        }
    }
    
    return config

# Singleton configuration instance
_config = None

def get_config() -> Dict[str, Any]:
    """Get singleton configuration instance"""
    global _config
    if _config is None:
        _config = load_config()
    return _config