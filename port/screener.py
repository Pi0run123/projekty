import customtkinter as ctk
import yfinance as yf

class StockScreener:
    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager

        self.frame = ctk.CTkFrame(self.parent, corner_radius=10)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(self.frame, text="Stock Screener", font=("Arial", 16)).pack(pady=10)
        ctk.CTkLabel(self.frame, text="Enter Ticker:", font=("Arial", 14)).pack(pady=5)
        self.ticker_entry = ctk.CTkEntry(self.frame, width=200)
        self.ticker_entry.pack(pady=5)

        self.tree = ctk.CTkTextbox(self.frame, height=400, corner_radius=10)
        self.tree.pack(fill="both", expand=True, pady=10)

        ctk.CTkButton(self.frame, text="Search Ticker", command=self.search_ticker, width=200).pack(pady=10)

    def search_ticker(self):
        self.tree.delete("1.0", ctk.END)
        ticker = self.ticker_entry.get().strip().upper()
        if not ticker:
            self.tree.insert(ctk.END, "Please enter a valid ticker.\n")
            return

        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            self.tree.insert(
                ctk.END,
                f"{ticker}\n"
                f"Close Price: {info.get('previousClose', 'N/A')}\n"
                f"Open Price: {info.get('open', 'N/A')}\n"
                f"Day High: {info.get('dayHigh', 'N/A')}\n"
                f"Day Low: {info.get('dayLow', 'N/A')}\n"
                f"Volume: {info.get('volume', 'N/A')}\n"
                f"Market Cap: {info.get('marketCap', 'N/A')}\n"
                f"Operating Margin: {info.get('operatingMargins', 'N/A')}\n"
                f"Debt/Equity: {info.get('debtToEquity', 'N/A')}\n"
                f"P/B: {info.get('priceToBook', 'N/A')}\n"
                f"P/E: {info.get('trailingPE', 'N/A')}\n"
                f"PEG: {info.get('pegRatio', 'N/A')}\n"
                f"Insider Transactions: {info.get('insiderTransactions', 'N/A')}\n"

            )
        except Exception as e:
            self.tree.insert(ctk.END, f"Error fetching data for {ticker}: {str(e)}\n")

class StockPortfolioMonitor:
    def __init__(self, parent, db_manager, user_id):
        self.parent = parent
        self.db_manager = db_manager
        self.user_id = user_id
        # ... rest of your code ...