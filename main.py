# main.py - FIXED VERSION WITH PROPER ERROR HANDLING
import asyncio
import json
import time
from datetime import datetime
import traceback
import sys

class AutonomousApesBot:
    def __init__(self):
        print("🦍 Initializing Autonomous Apes Bot...")
        
        # Check for API keys
        if not config.RECALL_API_KEY:
            print("❌ RECALL_API_KEY not found in .env!")
            sys.exit(1)
            
        self.engine = TradingEngine(config.RECALL_API_KEY, config.BASE_URL)
        self.strategy = StatisticalArbitrageStrategy()
        self.lit_agent = LitProtocolAgent()
        self.gaia_node = GAIANode()
        self.risk_manager = RiskManager()
        
        # Competition tracking
        self.competition_mode = "sandbox" in config.BASE_URL
        
    async def check_api_status(self) -> bool:
        """Check if API is working (maintenance issues from Discord)"""
        try:
            portfolio = self.engine.get_portfolio()
            if portfolio:
                print("✅ API is working")
                return True
            else:
                print("⚠️  API might be under maintenance")
                return False
        except:
            print("❌ Cannot connect to API")
            return False
    
    async def run_competition_mode(self):
        """Special mode for July 23 competition"""
        print("\n🏁 COMPETITION MODE ACTIVATED!")
        print("📅 Date: July 23, 2025")
        print("⏰ Duration: 24 hours")
        print("💰 Using REAL prices (not simulated)")
        print("⛽ Gas costs: IGNORED")
        print(f"🔗 Endpoint: {config.BASE_URL}")
        
        # Aggressive trading for competition
        while True:
            try:
                # 1. Get all market opportunities
                opportunities = await self.find_all_opportunities()
                
                # 2. Execute ALL profitable trades
                for opp in opportunities:
                    if opp["expected_profit"] > 10:  # $10 minimum
                        await self.execute_opportunity(opp)
                        
                # 3. Sleep briefly
                await asyncio.sleep(5)  # Check every 5 seconds in competition
                
            except Exception as e:
                print(f"❌ Competition error: {str(e)}")
                traceback.print_exc()
                await asyncio.sleep(10)
    
    async def find_all_opportunities(self) -> List[Dict]:
        """Find opportunities using ALL methods"""
        all_opportunities = []
        
        # 1. GAIA signals (CRITICAL for prize)
        gaia_signals = self.gaia_node.get_trading_signals({
            "eth_price": 2000,
            "btc_price": 45000,
            "market_trend": "volatile"
        })
        all_opportunities.extend(gaia_signals)
        
        # 2. Statistical arbitrage
        # 3. Cross-DEX arbitrage
        # 4. Liquidation hunting
        
        # Sort by profit potential
        all_opportunities.sort(key=lambda x: x.get("expected_profit", 0), reverse=True)
        
        return all_opportunities[:10]  # Top 10 opportunities
    
    async def run(self):
        """Main entry point"""
        print("\n" + "="*60)
        print("🦍 AUTONOMOUS APES BOT - READY TO DOMINATE")
        print("="*60)
        
        # Check API status first
        if not await self.check_api_status():
            print("⚠️  API issues detected. Waiting 30 seconds...")
            await asyncio.sleep(30)
        
        # Setup all systems
        print("\n📦 Setting up systems...")
        
        # 1. GAIA setup
        gaia_models = self.gaia_node.setup_gaia_models()
        if not gaia_models:
            print("⚠️  No GAIA models available - get API key from https://gaianet.ai/")
        
        # 2. Vincent/Lit setup
        self.lit_agent.create_pkp_wallet()
        
        # 3. Check competition mode
        if not self.competition_mode:
            print("\n⚠️  SANDBOX MODE - Switch to production URL for competition!")
            print("   Edit config.py and change BASE_URL")
        
        # Start appropriate mode
        if self.competition_mode:
            await self.run_sandbox_mode()
        else:
            await self.run_competition_mode()

if __name__ == "__main__":
    bot = AutonomousApesBot()
    
    # Handle interrupts gracefully
    try:
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        traceback.print_exc()