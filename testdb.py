import os, psycopg2, traceback

url = os.environ.get("DATABASE_URL")
print("DATABASE_URL:", url)

try:
    conn = psycopg2.connect(url)
    print("✅ Connected OK")
    conn.close()
except Exception:
    traceback.print_exc()
