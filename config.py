# config.py
import os
from dotenv import load_dotenv

load_dotenv()

RECALL_API_KEY = os.getenv("RECALL_API_KEY")
BASE_URL = "https://api.sandbox.competitions.recall.network"

# Token addresses (mainnet fork)
TOKENS = {
    "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    "WETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
    "WBTC": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
    "LINK": "0x514910771AF9Ca656af840dff83E8264EcF986CA"
}                   