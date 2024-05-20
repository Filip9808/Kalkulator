import sqlite3
from sympy import sympify, sin, cos, tan, log, sqrt
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application, parse_expr


def connect_to_db(db_name):
    """Łączy się z bazą danych SQLite"""
    conn = sqlite3.connect(db_name)
    return conn


def create_table(conn):
    """Tworzy tabelę w bazie danych"""
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS calculations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        expression TEXT NOT NULL,
                        result TEXT NOT NULL)''')
    conn.commit()


def insert_calculation(conn, expression, result):
    """Wstawia obliczenia do tabeli"""
    cursor = conn.cursor()
    cursor.execute('INSERT INTO calculations (expression, result) VALUES (?, ?)', (expression, result))
    conn.commit()


def fetch_calculations(conn):
    """Pobiera obliczenia z tabeli"""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM calculations')
    rows = cursor.fetchall()
    return rows


def main():
    db_name = 'calculations.db'
    conn = connect_to_db(db_name)
    create_table(conn)

    transformations = (standard_transformations + (implicit_multiplication_application,))

    while True:
        expression = input("Podaj wyrażenie do obliczenia (lub 'koniec' aby zakończyć): ")
        if expression.lower() == 'koniec':
            break

        try:
            parsed_expression = parse_expr(expression, transformations=transformations)
            result = parsed_expression.evalf()
            insert_calculation(conn, expression, str(result))
            print(f"Wynik: {result}")
        except Exception as e:
            print(f"Błąd: {e}")

    print("Zapisane obliczenia:")
    calculations = fetch_calculations(conn)
    for row in calculations:
        print(f"ID: {row[0]}, Wyrażenie: {row[1]}, Wynik: {row[2]}")

    conn.close()


if __name__ == '__main__':
    main()
