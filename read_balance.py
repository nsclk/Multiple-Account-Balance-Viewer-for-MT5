# -*- coding: utf-8 -*-
import MetaTrader5 as mt5
import sys
import json
import os
from datetime import datetime, timedelta

# Get terminal path from command-line arguments
terminal_path = sys.argv[1]

# Initialize MetaTrader 5
if not mt5.initialize(path=terminal_path):
    print(json.dumps({"error": f"MT5 initialization failed: {mt5.last_error()}"}))
    sys.exit(1)

# Get account information
account = mt5.account_info()
if not account:
    print(json.dumps({"error": "Account info not found"}))
    mt5.shutdown()
    sys.exit(1)

# Get current account balance
balance_now = float(account.balance)
account_id = int(account.login)

# Create a cache directory if it doesn't exist
cache_dir = "balance_cache"
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

# File to store previous balance
cache_file = os.path.join(cache_dir, f"{account_id}_balance.txt")

# Read previous balance from cache
previous_balance = None
balance_change = 0.0
balance_change_time = None

try:
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            data = f.read().strip().split(',')
            if len(data) >= 2:
                previous_balance = float(data[0])
                # If balance has changed, calculate the difference
                if previous_balance != balance_now:
                    balance_change = round(balance_now - previous_balance, 2)
                    balance_change_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                else:
                    # Balance hasn't changed, use cached change info if available
                    if len(data) >= 4:
                        balance_change = float(data[2])
                        balance_change_time = data[3]
except:
    pass

# Save current balance and change info to cache
with open(cache_file, 'w') as f:
    f.write(f"{balance_now},{datetime.now().timestamp()},{balance_change},{balance_change_time or ''}")

# Get deal history from the last 30 days
end_time = datetime.now()
start_time = end_time - timedelta(days=30)
deals = mt5.history_deals_get(start_time, end_time)

# Initialize default values for last trade
last_trade_change = 0.0
last_trade_time = None
last_trade_type = None
last_symbol = None

# If deals exist, find the latest closed deal
if deals:
    # Sort deals from newest to oldest
    deals = sorted(deals, key=lambda d: d.time, reverse=True)
    closing_deals = [deal for deal in deals if deal.entry == mt5.DEAL_ENTRY_OUT]
    
    if closing_deals:
        last_deal = closing_deals[0]
        # Subtract 3 hours from the deal time
        adjusted_time = datetime.fromtimestamp(last_deal.time) - timedelta(hours=3)
        last_trade_time = adjusted_time.strftime('%Y-%m-%d %H:%M:%S')
        last_symbol = last_deal.symbol
        last_trade_change = round(last_deal.profit, 2)
        
        if last_deal.type == mt5.DEAL_TYPE_BUY:
            last_trade_type = "BUY"
        elif last_deal.type == mt5.DEAL_TYPE_SELL:
            last_trade_type = "SELL"
        else:
            last_trade_type = "OTHER"

# Output result as JSON
print(json.dumps({
    "id": account_id,
    "name": str(account.name),
    "server": str(account.server),
    "balance": balance_now,
    "balance_change": balance_change,
    "balance_change_time": balance_change_time,
    "last_trade_change": last_trade_change,
    "last_trade_time": last_trade_time,
    "last_trade_type": last_trade_type,
    "last_symbol": last_symbol
}))

# Shutdown MetaTrader 5 connection
mt5.shutdown()