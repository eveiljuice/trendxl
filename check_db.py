#!/usr/bin/env python3
"""
Проверка состояния SQLite базы данных TrendXL
"""

import sqlite3
import os
from pathlib import Path


def check_database():
    """Проверка структуры и содержимого базы данных"""
    db_path = Path('trendxl.db')

    if not db_path.exists():
        print("❌ База данных не найдена!")
        return

    print(f"✅ База данных найдена: {db_path}")

    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # Получаем список таблиц
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        print("\n📊 Созданные таблицы:")
        for table in tables:
            table_name = table[0]

            # Получаем количество записей в таблице
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]

            print(f"  - {table_name}: {count} записей")

            # Для основных таблиц покажем структуру
            if table_name in ['Users', 'Trends']:
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                print(f"    Колонки: {', '.join([col[1] for col in columns])}")

        print("\n📈 Статистика базы данных:")
        if ('Users',) in tables:
            cursor.execute("SELECT COUNT(*) FROM Users")
            users_count = cursor.fetchone()[0]
            print(f"  👥 Пользователей: {users_count}")

        if ('Trends',) in tables:
            cursor.execute("SELECT COUNT(*) FROM Trends")
            trends_count = cursor.fetchone()[0]
            print(f"  📈 Трендов: {trends_count}")

        conn.close()
        print("\n✅ Проверка базы данных завершена успешно!")

    except Exception as e:
        print(f"❌ Ошибка при проверке базы данных: {e}")


if __name__ == "__main__":
    check_database()
