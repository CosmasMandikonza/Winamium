# config.py - FIXED VERSION
import os
from dotenv import load_dotenv

load_dotenv()

RECALL_API_KEY = os.getenv("RECALL_API_KEY")

# CRITICAL: Switch this for competition on July 23!
# Sandbox for testing:
BASE_URL = "https://api.sandbox.competitions.recall.network"
# Production for competition (July 23):
# BASE_URL = "https://api.competitions.recall.network"

# Token addresses - YOU MUST HARDCODE THESE (confirmed by Derrek)
TOKENS = {
    "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    "WETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
    "WBTC": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
    "LINK": "0x514910771AF9Ca656af840dff83E8264EcF986CA",
    "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    "UNI": "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
    "AAVE": "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9"
}

# Supported chains (from Discord)
SUPPORTED_CHAINS = ["eth", "polygon", "bsc", "arbitrum", "base", "optimism", "avalanche", "linea"]

# IMPORTANT: Gas costs are IGNORED in competition!
GAS_COST = 0  # Don't calculate gas