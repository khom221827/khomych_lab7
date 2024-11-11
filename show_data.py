import psycopg2
from prettytable import PrettyTable

def create_connection(db_name, user, password, host, port):
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print("Successfully connected to the database")
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def show_table_structure_and_data(connection):
    cursor = connection.cursor()
    
    # Отримуємо список таблиць у базі даних
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public';
    """)
    
    tables = cursor.fetchall()
    
    for table in tables:
        table_name = table[0]
        print(f"\nTable: {table_name}")
        
        # Структура таблиці: назва стовпця та його тип
        cursor.execute(f"""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = '{table_name}';
        """)
        
        columns = cursor.fetchall()
        print("Structure:")
        structure_table = PrettyTable()
        structure_table.field_names = ["Column Name", "Data Type"]
        for column in columns:
            structure_table.add_row(column)
        print(structure_table)
        
        # Дані з таблиці
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()
        print("\nData:")
        if rows:
            data_table = PrettyTable()
            data_table.field_names = [desc[0] for desc in cursor.description]  # Отримуємо назви стовпців
            for row in rows:
                data_table.add_row(row)
            print(data_table)
        else:
            print("No data in this table.")
    
    cursor.close()

# Використання
if __name__ == "__main__":
    connection = create_connection("postgres", "admin", "root", "127.0.0.1", "5432")
    if connection:
        show_table_structure_and_data(connection)
        connection.close()
