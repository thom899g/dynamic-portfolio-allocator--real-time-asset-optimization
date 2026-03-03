"""
Real-time market data fetcher with caching and error handling
Supports multiple data sources with fallback mechanisms
"""
import logging
import time
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Third-party imports with error handling
try:
    import ccxt
    CCXT_AVAILABLE = True
except ImportError:
    CCXT_AVAILABLE = False
    logging.warning("ccxt not available, crypto data fetching disabled")

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    logging.warning("yfinance not available, stock data fetching disabled")

from config import DataConfig, get_config

logger = logging.getLogger(__name__)

@dataclass
class MarketData:
    """Structured market data container"""
    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    vwap: Optional[float] = None
    bid: Optional[float] = None
    ask: Optional[float] = None
    spread: Optional[float] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for Firebase storage"""
        return {
            "symbol": self.symbol,
            "timestamp": self.timestamp.isoformat(),
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
            "vwap": self.vwap,
            "bid": self.bid,
            "ask": self.ask