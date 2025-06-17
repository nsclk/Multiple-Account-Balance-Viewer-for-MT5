
# 💰 MetaTrader 5 Balance Screener GUI

This project is a Python-based desktop GUI for monitoring multiple MetaTrader 5 (MT5) accounts in real-time. It displays account balances and the most recent trade result per account using a compact `tkinter` dashboard.

---

## 📸 Screenshot

![MT5 Balance Viewer Screenshot](./Screenshot%202025-06-18%20at%2001.28.23.png)

---

## ✅ Features

- 🧾 Displays account name, server, and balance
- 📉 Tracks the most recent closed trade (profit/loss, symbol, time)
- 📈 Color-coded result:
  - 🟢 Green = Profit
  - 🔴 Red = Loss
  - ⚪ Gray = No recent activity
- 🔁 Auto-refresh every 10 seconds
- 📌 Always-on-top window for trading sessions
- 🗃️ Stores balance changes in local cache
- 🧩 Easily extendable for alerts or logs

---

## 🗂️ Project Structure

```
📁 mt5-balance-screener/
├── main_widget.py         # GUI interface to display balances & trades
├── read_balance.py        # Extracts MT5 account info and trade data
├── balance_cache/         # Stores previous balance states (auto-created)
├── Screenshot 2025-06-18 at 01.28.23.png  # Example GUI output
└── README.md              # This file
```

---

## 🧰 Requirements

- Python 3.7+
- MetaTrader 5 installed locally
- Required packages:
  - `MetaTrader5`
  - `tkinter` (comes with most Python installations)

Install dependencies:

```bash
pip install MetaTrader5
```

---

## ⚙️ Usage

1. **Install and log into all MT5 terminals** you want to track.
2. Open `main_widget.py` and update the list of terminal paths:

```python
terminal_paths = [
    r"C:\Program Files\MetaTrader 5 Alpha 5k Eur\terminal64.exe",
    r"C:\Program Files\MetaTrader 5 Ftmo 100k Gbp\terminal64.exe",
    ...
]
```

3. Run the GUI:

```bash
python main_widget.py
```

The GUI will launch and display all configured account statuses.

---

## 🧠 How It Works

- `main_widget.py` spawns `read_balance.py` for each terminal.
- `read_balance.py` initializes the MT5 API, retrieves account balance and closed deal history, and checks for any balance change (using local cache).
- The GUI receives this data and displays it in a table format.
- If a balance change is detected, it overrides trade history with the change timestamp.

---

## 🛡️ Notes

- Ensure all terminals are logged in with valid accounts.
- Cached balances are stored in `balance_cache/` using account login as filename.
- The code subtracts **3 hours** from MT5 deal times to reflect local time. You can adjust or remove this depending on your timezone.

---

## 📜 License

MIT License

---

## 🙋‍♂️ Author

Developed by [Your Name or GitHub Handle]

---

## 🚀 Future Ideas

- Telegram/email alerts on balance change
- Export to CSV/Excel for history tracking
- Candlestick chart of equity growth
