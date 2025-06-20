import sqlite3
import os, io
import qrcode
import func as fn

path_db = "database.db"

if os.path.isfile(path_db):
    os.remove(path_db)


def export_qr_to_bytes(id):
    img = qrcode.make(f"https://{fn.get_private_wifi_ip()}:5000/product/{id}")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


conn = sqlite3.connect(path_db)
cursor = conn.cursor()

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    price REAL,
    stock INTEGER,
    spec TEXT,
    qr_code BLOB
)
"""
)

products = [
    (1, "iPhone 11", 80.92, 5, "Storage:64GB RAM:4GB", export_qr_to_bytes(1)),
    (2, "Samsung Galaxy A36 5G", 399.0, 5, "Storage:128GB RAM:6GB", export_qr_to_bytes(2)),
    (3, "ASUS Zenbook A14 (2025)", 999.9, 5, "Storage:512GB RAM:16GB", export_qr_to_bytes(3)),
]

cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?)", products)
conn.commit()
conn.close()
