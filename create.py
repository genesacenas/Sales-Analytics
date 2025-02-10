import sqlite3

conn = sqlite3.connect("sales_data.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT,
    sales INTEGER)
    """)

# insert sample data
sample_data=[
    ("Product A", 150),
    ("Product B", 200),
    ("Product C", 300),
    ("Product D", 250)]

cursor.executemany("INSERT INTO sales(product, sales) VALUES(?,?)", sample_data)

conn.commit()
conn.close()