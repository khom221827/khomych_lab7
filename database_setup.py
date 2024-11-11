# database_setup.py
import psycopg2

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

def setup_database(connection):
    cursor = connection.cursor()

    # Створення таблиць
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Warehouses (
        warehouse_id SERIAL PRIMARY KEY,
        address VARCHAR(100),
        manager VARCHAR(50),
        phone VARCHAR(15)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Products (
        product_id SERIAL PRIMARY KEY,
        type VARCHAR(20),
        name VARCHAR(50),
        manufacturer VARCHAR(50),
        warehouse_id INTEGER REFERENCES Warehouses(warehouse_id),
        quantity INTEGER,
        price DECIMAL(10, 2)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Clients (
        client_id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        address VARCHAR(100),
        phone VARCHAR(15),
        contact_person VARCHAR(50)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Sales (
        sale_id SERIAL PRIMARY KEY,
        sale_date DATE,
        client_id INTEGER REFERENCES Clients(client_id),
        product_id INTEGER REFERENCES Products(product_id),
        quantity INTEGER,
        discount DECIMAL(5, 2)
    );
    """)

    # Заповнення таблиць тестовими даними
    cursor.execute("INSERT INTO Warehouses (address, manager, phone) VALUES "
                   "('123 Main St', 'Alice Johnson', '123-456-7890'), "
                   "('456 Broad St', 'Bob Smith', '987-654-3210'), "
                   "('789 High St', 'Charlie Lee', '555-123-4567')"
                   )

    cursor.execute("INSERT INTO Clients (name, address, phone, contact_person) VALUES "
                   "('Client A', '111 Oak St', '555-0001', 'John Doe'), "
                   "('Client B', '222 Maple St', '555-0002', 'Jane Roe'), "
                   "('Client C', '333 Pine St', '555-0003', 'Alex Smith')"
                   )

    cursor.execute("INSERT INTO Products (type, name, manufacturer, warehouse_id, quantity, price) VALUES "
                   "('жіночий', 'Dress', 'FashionCo', 1, 10, 59.99), "
                   "('чоловічий', 'Suit', 'ElegantCorp', 2, 5, 150.00), "
                   "('дитячий', 'T-Shirt', 'KidsWear', 3, 20, 19.99)"
                   )

    cursor.execute("INSERT INTO Sales (sale_date, client_id, product_id, quantity, discount) VALUES "
                   "('2024-11-01', 1, 1, 2, 10.00), "
                   "('2024-11-02', 2, 2, 1, 5.00), "
                   "('2024-11-03', 3, 3, 3, 0.00)"
                   )

    # Збереження змін
    connection.commit()
    cursor.close()
    print("Database setup complete.")

# Використання
if __name__ == "__main__":
    connection = create_connection("postgres", "admin", "root", "127.0.0.1", "5432")
    if connection:
        setup_database(connection)
        connection.close()
