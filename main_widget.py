# -*- coding: utf-8 -*-
import tkinter as tk
import subprocess
import json
from datetime import datetime as dt

# List of MetaTrader 5 terminal paths
terminal_paths = [
    r"C:\Program Files\MetaTrader 5 Alpha 5k Eur\terminal64.exe",
    r"C:\Program Files\MetaTrader 5 Ftmo 100k Gbp\terminal64.exe",
    r"C:\Program Files\MetaTrader 5 FundedNext 200k Gbp\terminal64.exe",
    r"C:\Program Files\MetaTrader 5 The5ers 7.5k Gbp\terminal64.exe",
    r"C:\Program Files\Metatrader 5 Asia Manipulation\terminal64.exe",
]

# Set up the main window
root = tk.Tk()
root.title("Balance Screener")
root.geometry("600x450")
root.configure(bg="#c0c0c0")  # Classic gray background
root.attributes('-topmost', True)  # Always on top

# Header label
header = tk.Label(root, text="Account Balances", font=("Arial", 16, "bold"),
                  bg="#000080", fg="white", padx=10, pady=5, relief="ridge", bd=3)
header.pack(fill="x", pady=(5, 10), padx=5)

# Create column headers
header_frame = tk.Frame(root, bg="#c0c0c0")
header_frame.pack(fill="x", padx=10, pady=(0, 5))

tk.Label(header_frame, text="Account Info", font=("Courier New", 10, "bold"),
         bg="#c0c0c0", anchor="w").pack(side="left", padx=(10, 0))
tk.Label(header_frame, text="Current Balance", font=("Courier New", 10, "bold"),
         bg="#c0c0c0", anchor="e").pack(side="right", padx=(0, 20))

# Frame to hold account rows
table_frame = tk.Frame(root, bg="#c0c0c0")
table_frame.pack(fill="both", expand=True, padx=10)

# Store label widgets for updates
labels = []

# Create one row for each terminal
for _ in terminal_paths:
    panel = tk.Frame(table_frame, bg="#e0e0e0", bd=2, relief="sunken")
    panel.pack(fill="x", pady=3)

    # Create a frame for the main content
    content_frame = tk.Frame(panel, bg="#e0e0e0")
    content_frame.pack(fill="x", padx=10, pady=5)

    # Account info label (left side)
    info_label = tk.Label(content_frame, text="Loading...", font=("Courier New", 11),
                          fg="black", bg="#e0e0e0", anchor="w", justify="left")
    info_label.pack(side="left", fill="x", expand=True)

    # Current balance label (right side)
    balance_label = tk.Label(content_frame, text="", font=("Courier New", 11, "bold"),
                             fg="black", bg="#e0e0e0", anchor="e", justify="right", width=12)
    balance_label.pack(side="right", padx=(5, 0))

    # Trade history label (below main content)
    trade_label = tk.Label(panel, text="", font=("Courier New", 9),
                           fg="gray40", bg="#e0e0e0", anchor="w", justify="left")
    trade_label.pack(fill="x", padx=10, pady=(0, 5))

    labels.append((info_label, balance_label, trade_label))

# Label for last updated time
last_updated_label = tk.Label(root, text="Last updated: --", font=("Courier New", 9),
                              fg="gray10", bg="#c0c0c0", anchor="e")
last_updated_label.pack(fill="x", padx=10, pady=(5, 10))

# Function to update all account balances and trade results
def update_balances():
    for i, path in enumerate(terminal_paths):
        info_label, balance_label, trade_label = labels[i]
        try:
            # Run the read_balance.py script with the terminal path
            result = subprocess.run(["python", "read_balance.py", path], capture_output=True, text=True, timeout=10)
            
            # Parse the output
            try:
                data = json.loads(result.stdout.strip())
            except json.JSONDecodeError:
                info_label.config(text="[PARSING ERROR]", fg="red")
                balance_label.config(text="")
                trade_label.config(text="")
                continue

            # Display error message if any
            if "error" in data:
                info_label.config(text=f"[ERROR] {data['error']}", fg="red")
                balance_label.config(text="")
                trade_label.config(text="")
            else:
                # Display account info
                info_label.config(text=f"{data['name']} | {data['server']}", fg="black")
                balance_label.config(text=f"${data['balance']:.2f}", fg="black")

                # Check if we should use balance change or last trade data
                balance_change = data.get("balance_change", 0.0)
                balance_change_time = data.get("balance_change_time", "")
                trade_change = data.get("last_trade_change", 0.0)
                trade_time = data.get("last_trade_time", "")
                symbol = data.get("last_symbol", "--")
                
                # If balance has EVER changed (we have a timestamp), always show it as last trade
                if balance_change_time:
                    # Use balance change as the "last trade" (even if current change is 0)
                    if balance_change > 0:
                        trade_text = f"Last trade: +${balance_change:.2f} {symbol} ({balance_change_time})"
                        trade_color = "green"
                    elif balance_change < 0:
                        trade_text = f"Last trade: -${abs(balance_change):.2f} {symbol} ({balance_change_time})"
                        trade_color = "red"
                    else:
                        # Balance hasn't changed since last recorded change
                        trade_text = f"Last trade: $0.00 {symbol} ({balance_change_time})"
                        trade_color = "gray40"
                    
                    trade_label.config(text=trade_text, fg=trade_color)
                
                # Only show actual trade history if balance has NEVER changed
                elif trade_time and trade_time != "--":
                    if trade_change > 0:
                        trade_text = f"Last trade: +${trade_change:.2f} {symbol} ({trade_time})"
                        trade_color = "green"
                    elif trade_change < 0:
                        trade_text = f"Last trade: -${abs(trade_change):.2f} {symbol} ({trade_time})"
                        trade_color = "red"
                    else:
                        trade_text = f"Last trade: $0.00 {symbol} ({trade_time})"
                        trade_color = "gray40"
                    
                    trade_label.config(text=trade_text, fg=trade_color)
                else:
                    trade_label.config(text="Last trade: No recent trades", fg="gray40")

        except Exception as e:
            info_label.config(text=f"[CONNECTION ERROR] {str(e)}", fg="red")
            balance_label.config(text="")
            trade_label.config(text="")

    # Update the timestamp label
    now = dt.now().strftime("%Y-%m-%d %H:%M:%S")
    last_updated_label.config(text=f"Last updated: {now}")
    root.after(10000, update_balances)  # Refresh every 10 seconds

# Start GUI update loop
update_balances()
root.mainloop()