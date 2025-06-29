import psycopg2

class DatabaseManager:
    def __init__(self, host, database, user, password):
        try:
            self.connection = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password
            )
            self.cursor = self.connection.cursor()
            self.create_tables()
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            self.connection = None

    def create_tables(self):
        try:
            # Create users table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(50) NOT NULL
                )
            """)
            # Create stocks table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS stocks (
                    id SERIAL PRIMARY KEY,
                    user_id INT REFERENCES users(id),
                    symbol VARCHAR(10),
                    shares FLOAT,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.connection.commit()
        except Exception as e:
            print(f"Error creating tables: {e}")

    def register_user(self, username, password):
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, password)
            )
            self.connection.commit()
        except Exception as e:
            print(f"Error registering user: {e}")

    def authenticate_user(self, username, password):
        try:
            self.cursor.execute(
                "SELECT id FROM users WHERE username = %s AND password = %s",
                (username, password)
            )
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error authenticating user: {e}")
            return None

    def save_stock(self, user_id, symbol, shares):
        try:
            self.cursor.execute(
                "INSERT INTO stocks (user_id, symbol, shares) VALUES (%s, %s, %s)",
                (user_id, symbol, shares)
            )
            self.connection.commit()
        except Exception as e:
            print(f"Error saving stock to database: {e}")

    def get_stocks(self, user_id):
        try:
            self.cursor.execute("SELECT symbol, shares FROM stocks WHERE user_id = %s", (user_id,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching stocks: {e}")
            return []

    def update_stock(self, user_id, symbol, shares):
        try:
            self.cursor.execute(
                "UPDATE stocks SET shares = %s WHERE user_id = %s AND symbol = %s",
                (shares, user_id, symbol)
            )
            self.connection.commit()
        except Exception as e:
            print(f"Error updating stock: {e}")

    def delete_stock(self, user_id, symbol):
        try:
            self.cursor.execute(
                "DELETE FROM stocks WHERE user_id = %s AND symbol = %s",
                (user_id, symbol)
            )
            self.connection.commit()
        except Exception as e:
            print(f"Error deleting stock: {e}")

    def close_connection(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()