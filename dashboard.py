# dashboard.py - UPDATED VERSION
from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/performance')
def get_performance():
    """Return real performance data"""
    try:
        with open('performance.json', 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except:
        # Default data if file doesn't exist
        return jsonify({
            "total_return": 0,
            "sharpe_ratio": 0,
            "max_drawdown": 0,
            "winning_trades": 0,
            "total_trades": 0
        })

if __name__ == '__main__':
    app.run(debug=True, port=5000)