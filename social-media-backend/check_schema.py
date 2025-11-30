import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Get table schema
cursor.execute("PRAGMA table_info(users)")
columns = cursor.fetchall()

print("Users table schema:")
print("=" * 80)
for col in columns:
    col_id, name, col_type, notnull, default, pk = col
    nullable = "NOT NULL" if notnull else "NULL"
    print(f"{name:20} {col_type:20} {nullable:10} default={default}")

# Check first_name specifically
print("\n" + "=" * 80)
first_name_col = [c for c in columns if c[1] == 'first_name'][0]
print(f"\nfirst_name column details:")
print(f"  Type: {first_name_col[2]}")
print(f"  NOT NULL: {bool(first_name_col[3])}")
print(f"  Default: {first_name_col[4]}")

conn.close()
