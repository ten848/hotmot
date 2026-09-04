import sqlite3
import pandas as pd

conn = sqlite3.connect("roles/p_support.db")
df = pd.read_sql("SELECT * FROM pokemon", conn)
conn.close()

print(df)