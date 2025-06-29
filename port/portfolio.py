import customtkinter as ctk
import yfinance as yf
import threading
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class StockPortfolioMonitor:
    def __init__(self, parent, db_manager, user_id):
        self.parent = parent
        self.db_manager = db_manager
        self.user_id = user_id

        self.portfolio = {}
        self.stock_prices = {}
        self.chart_canvas = None

        self.main_frame = ctk.CTkFrame(self.parent, corner_radius=10)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.create_widgets()
        self.load_stocks()

        self.running = True
        self.update_thread = threading.Thread(target=self.update_prices)
        self.update_thread.daemon = True
        self.update_thread.start()

    def create_widgets(self):
        add_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        add_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(add_frame, text="Symbol:", font=("Arial", 14)).pack(side="left", padx=5)
        self.symbol_entry = ctk.CTkEntry(add_frame, width=150)
        self.symbol_entry.pack(side="left", padx=5)

        ctk.CTkLabel(add_frame, text="Shares:", font=("Arial", 14)).pack(side="left", padx=5)
        self.shares_entry = ctk.CTkEntry(add_frame, width=150)
        self.shares_entry.pack(side="left", padx=5)

        ctk.CTkButton(add_frame, text="Add Stock", command=self.add_stock, width=120).pack(side="left", padx=5)

        self.tree = ctk.CTkTextbox(self.main_frame, height=300, corner_radius=10)
        self.tree.pack(fill="both", expand=True, pady=10)

        self.total_label = ctk.CTkLabel(self.main_frame, text="Total Value: $0.00", font=("Arial", 16))
        self.total_label.pack(pady=10)

        edit_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        edit_frame.pack(fill="x", pady=10)

        ctk.CTkButton(edit_frame, text="Update Stock", command=self.update_stock, width=120).pack(side="left", padx=5)
        ctk.CTkButton(edit_frame, text="Delete Stock", command=self.delete_stock, width=120).pack(side="left", padx=5)

        # Dropdown for chart selection
        self.chart_type = ctk.StringVar(value="Select Chart Type")
        ctk.CTkOptionMenu(
            edit_frame,
            values=["Companies", "Sector"],
            variable=self.chart_type,
            command=self.show_chart,
            width=150
        ).pack(side="left", padx=5)

        ctk.CTkLabel(self.main_frame, text="Portfolio View", font=("Arial", 18)).pack(pady=20)

    def load_stocks(self):
        """Load stocks from the database for the logged-in user."""
        stocks = self.db_manager.get_stocks(self.user_id)
        for stock in stocks:
            symbol, shares = stock
            self.portfolio[symbol] = shares
        self.update_display()

    def add_stock(self):
        symbol = self.symbol_entry.get().upper()
        try:
            shares = float(self.shares_entry.get())
            if symbol and shares > 0:
                self.portfolio[symbol] = shares
                self.db_manager.save_stock(self.user_id, symbol, shares)
                self.update_display()
                self.symbol_entry.delete(0, ctk.END)
                self.shares_entry.delete(0, ctk.END)
        except ValueError:
            pass

    def update_stock(self):
        """Update the number of shares for a stock."""
        symbol = self.symbol_entry.get().upper()
        try:
            shares = float(self.shares_entry.get())
            if symbol in self.portfolio and shares > 0:
                self.portfolio[symbol] = shares
                self.db_manager.update_stock(self.user_id, symbol, shares)
                self.update_display()
                self.symbol_entry.delete(0, ctk.END)
                self.shares_entry.delete(0, ctk.END)
        except ValueError:
            pass

    def delete_stock(self):
        """Delete a stock from the portfolio."""
        symbol = self.symbol_entry.get().upper()
        if symbol in self.portfolio:
            del self.portfolio[symbol]
            self.db_manager.delete_stock(self.user_id, symbol)
            self.update_display()
            self.symbol_entry.delete(0, ctk.END)

    def update_prices(self):
        while self.running:
            self.update_display()
            time.sleep(60)

    def update_display(self):
        total_value = 0
        self.tree.delete("1.0", ctk.END)

        for symbol, shares in self.portfolio.items():
            try:
                stock = yf.Ticker(symbol)
                info = stock.info
                price = info.get('regularMarketPrice', 0)
                sector = info.get('sector', 'Unknown')
                self.stock_prices[symbol] = {"price": price, "sector": sector}
                currency = info.get('currency', 'USD')
                value = price * shares

                # Convert price and previous close to USD if necessary
                if currency != 'USD':
                    conversion_rate = self.get_conversion_rate(currency, 'USD')
                    price *= conversion_rate
                    prev_close = info.get('regularMarketPreviousClose', price) * conversion_rate
                else:
                    prev_close = info.get('regularMarketPreviousClose', price)

                value = price * shares
                total_value += value

                # Calculate price change percentage
                change = ((price - prev_close) / prev_close) * 100

                self.tree.insert(
                    ctk.END,
                    f"{symbol} | Shares: {shares:.2f} | Price: ${price:.2f} | Value: ${value:.2f} | Change: {change:+.2f}% | Sector: {sector} | Currency: {currency}\n"
                )
            except Exception as e:
                self.tree.insert(ctk.END, f"Error fetching data for {symbol}: {str(e)}\n")

        self.total_label.configure(text=f"Total Value: ${total_value:.2f}")

    def get_conversion_rate(self, from_currency, to_currency):
        conversion_rates = {
            'PLN': 0.26,
            'EUR': 1.10,
        }
        return conversion_rates.get(from_currency, 1)

    def show_chart(self, chart_type):
        """Display a pie chart grouped by companies or sector."""
        if self.chart_canvas:
            self.chart_canvas.get_tk_widget().destroy()
            self.chart_canvas = None

        if chart_type == "Companies":
            fig = self.create_companies_chart()
        elif chart_type == "Sector":
            fig = self.create_sector_chart()

        self.chart_canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.chart_canvas.get_tk_widget().pack()
        self.chart_canvas.draw()

    def create_companies_chart(self):
        """Create a pie chart grouped by companies."""
        labels = []
        sizes = []
        for symbol, shares in self.portfolio.items():
            price = self.stock_prices.get(symbol, {}).get("price", 0)
            value = price * shares
            labels.append(symbol)
            sizes.append(value)

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
        ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
        plt.title("Portfolio Distribution by Companies")
        return fig

    def create_sector_chart(self):
        """Create a pie chart grouped by sector."""
        labels = []
        sizes = []
        sectors = {}

        for symbol, shares in self.portfolio.items():
            price = self.stock_prices.get(symbol, {}).get("price", 0)
            sector = self.stock_prices.get(symbol, {}).get("sector", "Unknown")
            value = price * shares
            sectors[sector] = sectors.get(sector, 0) + value

        for sector, value in sectors.items():
            labels.append(sector)
            sizes.append(value)

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
        ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
        plt.title("Portfolio Distribution by Sector")
        return fig

    def get_sector_color(self, sector):
        """Return a color for the sector."""
        sector_colors = {
            'Technology': '#ff9999',
            'Healthcare': '#66b3ff',
            'Finance': '#99ff99',
            'Consumer Services': '#ffcc99',
            'Industrials': '#c2c2f0',
            'Energy': '#ffb3e6',
            'Materials': '#c2f0c2',
            'Real Estate': '#ffccff',
            'Utilities': '#ffffb3',
            'Communication Services': '#c2e0c2',
            'Consumer Staples': '#f2b2b2',
            'Transportation': '#b3b3ff',
            'Unknown': '#d9d9d9'
        }
        return sector_colors.get(sector, '#d9d9d9')

    def get_stock_color(self, symbol):
        """Return a color for the stock."""
        colors = plt.cm.viridis_r(range(len(self.portfolio)))  # Reverse the viridis colormap
        color_dict = dict(zip(self.portfolio.keys(), colors))
        return color_dict.get(symbol, '#d9d9d9')

    def on_closing(self):
        self.running = False
        self.db_manager.close_connection()
        self.root.destroy()