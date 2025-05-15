import psycopg2

conn = psycopg2.connect(
    dbname="interpol",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port="5432",
    client_encoding="utf8"
)

cur = conn.cursor()

# Tabloya iki yeni sütun ekliyoruz
cur.execute("""
    ALTER TABLE notices
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ADD COLUMN IF NOT EXISTS last_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
""")

conn.commit()
cur.close()
conn.close()

print("Tablo güncellendi ✅")