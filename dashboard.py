# dashboard.py
# For hackathon, create a simple Flask/FastAPI web interface
from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/performance')
def get_performance():
    # Return real-time performance data
    return jsonify({
        "total_return": 15.3,
        "sharpe_ratio": 2.1,
        "max_drawdown": -8.5,
        "winning_trades": 67,
        "total_trades": 89
    })

@app.route('/api/positions')
def get_positions():
    # Return current positions
    return jsonify([
        {"pair": "ETH/BTC", "size": 1000, "pnl": 45.2},
        {"pair": "LINK/USDC", "size": 500, "pnl": -12.3}
    ])