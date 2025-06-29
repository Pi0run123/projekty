import customtkinter as ctk
from database import DatabaseManager

class LoginScreen:
    def __init__(self, root, db_manager, on_login):
        self.root = root
        self.db_manager = db_manager
        self.on_login = on_login

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        self.frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(self.frame, text="Username:", font=("Arial", 14)).pack(pady=5)
        self.username_entry = ctk.CTkEntry(self.frame, width=200)
        self.username_entry.pack(pady=5)

        ctk.CTkLabel(self.frame, text="Password:", font=("Arial", 14)).pack(pady=5)
        self.password_entry = ctk.CTkEntry(self.frame, width=200, show="*")
        self.password_entry.pack(pady=5)

        ctk.CTkButton(self.frame, text="Login", command=self.login, width=120).pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_id = self.db_manager.authenticate_user(username, password)
        if user_id:
            self.frame.destroy()
            self.on_login(user_id)
        else:
            ctk.CTkLabel(self.frame, text="Invalid credentials!", text_color="red", font=("Arial", 12)).pack(pady=5)

if __name__ == "__main__":
    from menu import MainApp  # <-- Import here, after LoginScreen is defined
    root = ctk.CTk()
    db_manager = DatabaseManager(host="localhost", database="main", user="postgres", password="123")

    def start_app(user_id):
        app = MainApp(root, db_manager, user_id)
        root.protocol("WM_DELETE_WINDOW", app.logout)

    login_screen = LoginScreen(root, db_manager, start_app)
    root.mainloop()