import customtkinter as ctk
from navigation import NavigationFrame
from portfolio import StockPortfolioMonitor
from screener import StockScreener
from database import DatabaseManager
from main import LoginScreen

class MainApp:
    def __init__(self, root, db_manager, user_id):
        self.root = root
        self.db_manager = db_manager
        self.user_id = user_id

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        self.sidebar = NavigationFrame(
            self.root,
            on_portfolio=self.show_portfolio,
            on_screener=self.show_screener,
            on_logout=self.logout
        )
        self.sidebar.pack(side="left", fill="y")

        self.content_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.current_view = None
        self.show_portfolio()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.current_view = None

    def show_portfolio(self):
        self.clear_content()
        self.current_view = StockPortfolioMonitor(self.content_frame, self.db_manager, self.user_id)

    def show_screener(self):
        self.clear_content()
        self.current_view = StockScreener(self.content_frame, self.db_manager)

    def logout(self):
        self.root.destroy()

if __name__ == "__main__":
    root = ctk.CTk()
    db_manager = DatabaseManager(host="localhost", database="main", user="postgres", password="123")

    def start_app(user_id):
        app = MainApp(root, db_manager, user_id)
        root.protocol("WM_DELETE_WINDOW", app.logout)

    login_screen = LoginScreen(root, db_manager, start_app)
    root.mainloop()