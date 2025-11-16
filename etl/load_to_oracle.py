import csv
import oracledb
import os
from datetime import datetime

# ---------- Oracle connection details ----------
USERNAME = "uname"
PASSWORD = "pw"
HOST = "localhost"
PORT = 1111
SID = "orcl"  # Your actual database SID

# Create DSN for SID
dsn = oracledb.makedsn(HOST, PORT, sid=SID)

# Connect to Oracle
conn = oracledb.connect(user=USERNAME, password=PASSWORD, dsn=dsn)
cur = conn.cursor()

# ---------- Delete old data in dependency order ----------
cur.execute("DELETE FROM fact_sales")     # transactions first
cur.execute("DELETE FROM dim_product")    # then products
cur.execute("DELETE FROM dim_customer")   # then customers
conn.commit()
print("Old data deleted successfully!")

# ---------- Functions to load CSVs ----------
def load_products(csv_path):
    with open(csv_path, newline='') as f:
        next(f)  # skip header
        rows = [tuple(line) for line in csv.reader(f)]
    sql = "INSERT INTO dim_product (sku, name, category, quality, price) VALUES (:1,:2,:3,:4,:5)"
    cur.executemany(sql, rows)
    conn.commit()
    print("Products loaded")

def load_customers(csv_path):
    with open(csv_path, newline='') as f:
        next(f)
        rows = []
        for r in csv.reader(f):
            has_loyalty = 1 if r[2].lower() in ["true","1"] else 0
            rows.append((r[0], r[1], has_loyalty))
    sql = "INSERT INTO dim_customer (customer_uuid, name, has_loyalty) VALUES (:1,:2,:3)"
    cur.executemany(sql, rows)
    conn.commit()
    print("Customers loaded")

def load_transactions(csv_path):
    # Map SKU -> product_id
    cur.execute("SELECT product_id, sku FROM dim_product")
    sku_map = {sku: pid for pid, sku in cur.fetchall()}

    # Map customer UUID -> customer_id
    cur.execute("SELECT customer_id, customer_uuid FROM dim_customer")
    cust_map = {uuid: cid for cid, uuid in cur.fetchall()}

    with open(csv_path, newline='') as f:
        next(f)  # skip header
        rows = []
        for sku, customer_uuid, sale_ts, qty, unit_price, pc_points in csv.reader(f):
            pid = sku_map.get(sku)
            cid = cust_map.get(customer_uuid)
            if pid is None or cid is None:
                continue
            # Convert ISO 8601 string to datetime
            dt = datetime.fromisoformat(sale_ts)
            rows.append((pid, cid, dt, int(qty), float(unit_price), int(pc_points)))

    cur.executemany(
        """
        INSERT INTO fact_sales (product_id, customer_id, sale_ts, quantity, unit_price, pc_points_awarded) 
        VALUES (:1, :2, :3, :4, :5, :6)
        """,
        rows
    )
    conn.commit()
    print("Transactions loaded")

# ---------- Main ----------
if __name__ == "__main__":
    base = "C:/Users/nilee/Documents/Nileena/Resumes/latest resume for Data Engineer/Retail_Loyalty_Insight/output"

    load_products(os.path.join(base,"products.csv"))
    load_customers(os.path.join(base,"customers.csv"))
    load_transactions(os.path.join(base,"transactions.csv"))

    print("All data loaded into Oracle successfully!")
    cur.close()
    conn.close()
