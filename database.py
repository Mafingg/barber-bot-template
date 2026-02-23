import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def create_table(self):
        with self.connection:
            return self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS users ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "user_id INTEGER UNIQUE, "
                "username TEXT, "
                "full_name TEXT, "
                "phone TEXT, "  # Новое поле
                "signup_date DATETIME DEFAULT CURRENT_TIMESTAMP)"
            )

    # Добавь новый метод для обновления телефона
    def update_phone(self, user_id, phone):
        with self.connection:
            return self.cursor.execute(
                "UPDATE users SET phone = ? WHERE user_id = ?",
                (phone, user_id)
            )

    def add_user(self, user_id, username, full_name):
        """Добавляем пользователя в базу"""
        with self.connection:
            return self.cursor.execute(
                "INSERT OR IGNORE INTO users (user_id, username, full_name) VALUES (?, ?, ?)",
                (user_id, username, full_name)
            )

    def get_users_count(self):
        """Считаем общее количество клиентов"""
        with self.connection:
            return self.cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]

    def get_all_users(self):
        """Возвращает список всех строк из таблицы users"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM users").fetchall()


# Инициализируем объект базы данных
db = Database('bot_database.db')