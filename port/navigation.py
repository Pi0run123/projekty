import customtkinter as ctk

class NavigationFrame(ctk.CTkFrame):
    def __init__(self, parent, on_portfolio, on_screener, on_logout):
        super().__init__(parent, width=180, corner_radius=0)
        self.pack_propagate(False)
        ctk.CTkLabel(self, text="MENU", font=("Arial", 18, "bold")).pack(pady=(30, 20))
        ctk.CTkButton(self, text="Portfolio", command=on_portfolio, width=160).pack(pady=10)
        ctk.CTkButton(self, text="Stock Screener", command=on_screener, width=160).pack(pady=10)
        ctk.CTkButton(self, text="Logout", command=on_logout, width=160).pack(side="bottom", pady=30)