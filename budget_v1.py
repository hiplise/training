import sqlite3


def init_db():
    conn = sqlite3.connect('budget_v1.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budget (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            income REAL,
            expenses REAL,
            goal_name TEXT,
            goal_amount REAL
        )
    ''')
    cursor.execute("SELECT COUNT(*) FROM budget")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO budget (income, expenses, goal_name, goal_amount) VALUES (100000, 60000, 'Автомобиль', 400000)")
        conn.commit()
    conn.close()

def run_experiment():
    conn = sqlite3.connect('budget_v1.db')
    cursor = conn.cursor()
    cursor.execute("SELECT income, expenses, goal_name, goal_amount FROM budget ORDER BY id DESC LIMIT 1")
    data = cursor.fetchone()
    conn.close()

    if not data:
        print("Данные в БД отсутствуют!")
        return

    income, expenses, goal_name, goal_amount = data
    monthly_savings = income - expenses

    print(f"=== Вычислительный эксперимент V1 ===")
    print(f"Доход: {income} руб. | Расходы: {expenses} руб.")
    print(f"Ежемесячно откладывается: {monthly_savings} руб.")
    print(f"Цель: {goal_name} ({goal_amount} руб.)")

    if monthly_savings <= 0:
        print("Результат: С такими расходами накопить на цель невозможно!")
    else:
        months = goal_amount / monthly_savings
        print(f"Результат: Вы накопите на '{goal_name}' за {months:.1f} мес.")


if __name__ == "__main__":
    init_db()
    run_experiment()
