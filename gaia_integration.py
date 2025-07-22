# gaia_integration.py - FIXED VERSION WITH PUBLIC NODES
import requests
import json
from typing import Dict, List
import os
from dotenv import load_dotenv

load_dotenv()

class GAIANode:
    def __init__(self):
        # USE PUBLIC NODES - Don't run locally!
        self.public_nodes = {
            "qwen72b": "https://qwen72b.gaia.domains/v1",
            "llama": "https://llama.us.gaia.domains/v1",
            "phi": "https://phi3.gaia.domains/v1"
        }
        
        # Get API key from https://gaianet.ai/
        self.api_key = os.getenv("GAIA_API_KEY")
        if not self.api_key:
            print("⚠️  No GAIA API key found. Get one from https://gaianet.ai/")
            print("   1. Click 'Launch App'")
            print("   2. Connect wallet")
            print("   3. Go to Settings -> Gaia API Keys -> Developer Free Trial")
            
    def setup_gaia_models(self) -> Dict:
        """Setup using PUBLIC nodes (don't run locally!)"""
        print("🔧 Setting up GAIA models using public nodes...")
        
        models = {}
        
        # Test each public node
        for name, endpoint in self.public_nodes.items():
            try:
                response = requests.post(
                    f"{endpoint}/chat/completions",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={
                        "model": "default",
                        "messages": [{"role": "user", "content": "test"}],
                        "max_tokens": 10
                    },
                    timeout=5
                )
                
                if response.ok:
                    models[name] = endpoint
                    print(f"✅ {name} node ready: {endpoint}")
                else:
                    print(f"❌ {name} node failed: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ {name} node error: {str(e)}")
                
        return models
    
    def get_trading_signals(self, market_data: Dict) -> List[Dict]:
        """Get signals from multiple GAIA models"""
        signals = []
        
        prompt = f"""Analyze this market data and find trading opportunities:
        {json.dumps(market_data, indent=2)}
        
        Return ONLY a JSON array of opportunities like:
        [{{"pair": "ETH/USDC", "action": "buy", "confidence": 0.85, "reason": "oversold"}}]
        """
        
        # Query multiple models for consensus
        for name, endpoint in self.public_nodes.items():
            try:
                response = requests.post(
                    f"{endpoint}/chat/completions",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={
                        "model": "default",
                        "messages": [
                            {"role": "system", "content": "You are a crypto trading AI. Return only valid JSON."},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.1,
                        "max_tokens": 200
                    },
                    timeout=10
                )
                
                if response.ok:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    
                    # Try to parse JSON
                    try:
                        opportunities = json.loads(content)
                        signals.extend(opportunities)
                    except:
                        # Fallback if JSON parsing fails
                        print(f"⚠️  {name} returned non-JSON: {content[:100]}")
                        
            except Exception as e:
                print(f"❌ Error querying {name}: {str(e)}")
                
        return signals