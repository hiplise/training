import sqlite3

def init_db():
    conn = sqlite3.connect('budget_v2.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budget (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            income REAL,
            expenses REAL,
            goal_name TEXT,
            goal_amount REAL,
            deposit_rate REAL,
            inflation_rate REAL
        )
    ''')
    cursor.execute("SELECT COUNT(*) FROM budget")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO budget (income, expenses, goal_name, goal_amount, deposit_rate, inflation_rate) VALUES (100000, 60000, 'Автомобиль', 400000, 0.01, 0.005)")
        conn.commit()
    conn.close()

def run_experiment():
    conn = sqlite3.connect('budget_v2.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT income, expenses, goal_name, goal_amount, deposit_rate, inflation_rate FROM budget ORDER BY id DESC LIMIT 1")
    data = cursor.fetchone()
    conn.close()

    if not data:
        return

    income, expenses, goal_name, goal_amount, deposit_rate, inflation_rate = data
    monthly_savings = income - expenses

    print(f"=== Вычислительный эксперимент V2 (С инфляцией и % по вкладу) ===")
    print(f"Ежемесячно откладывается: {monthly_savings} руб.")

    if monthly_savings <= 0:
        print("Результат: Накопить невозможно.")
        return

    current_savings = 0
    months = 0
    max_months = 120

    while current_savings < goal_amount and months < max_months:
        months += 1
        current_savings = current_savings * (1 + deposit_rate) + monthly_savings
        goal_amount = goal_amount * (1 + inflation_rate)

    if current_savings >= goal_amount:
        print(f"Результат: С учетом процентов и инфляции вы накопите на цель за {months} мес.")
        print(f"Итоговая стоимость цели с учетом инфляции: {goal_amount:.2f} руб.")
    else:
        print("Результат: За 10 лет накопить не удалось, инфляция опережает сбережения.")


if __name__ == "__main__":
    init_db()
    run_experiment()
