from config import get_db_connection
from datetime import datetime

# def get_pr_datatable(start, length, search_value, order_column, order_dir):
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)

#     # Hitung total records
#     cursor.execute("SELECT COUNT(*) as cnt FROM purchase_requests")
#     total_records = cursor.fetchone()["cnt"]

#     base_query = "SELECT * FROM purchase_requests"
#     where_clause = ""
#     params = []

#     if search_value:
#         search_query = f"%{search_value}%"
#         where_clause = """
#             WHERE name LIKE %s OR requester LIKE %s OR description LIKE %s OR status LIKE %s
#         """
#         params.extend([search_query, search_query, search_query, search_query])

#     # tambahkan order by dinamis
#     query = f"""{base_query} {where_clause}
#                 ORDER BY {order_column} {order_dir}
#                 LIMIT %s OFFSET %s"""
#     params.extend([length, start])

#     cursor.execute(query, params)
#     data = cursor.fetchall()

#     # filtered count
#     if search_value:
#         cursor.execute(
#             f"SELECT COUNT(*) as cnt FROM purchase_requests {where_clause}",
#             [search_query, search_query, search_query, search_query],
#         )
#         filtered_records = cursor.fetchone()["cnt"]
#     else:
#         filtered_records = total_records

#         # Format created_at ke d-m-Y
#     for row in data:
#         if row.get("date"):
#             try:
#                 row["date"] = datetime.strptime(str(row["date"]), "%Y-%m-%d").strftime(
#                     "%Y-%m-%d"
#                 )
#             except:
#                 pass
#     cursor.close()
#     conn.close()
#     return data, total_records, filtered_records


def get_pr_datatable(start, length, search_value, order_column, order_dir):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Hitung total records
    cursor.execute("SELECT COUNT(*) as cnt FROM purchase_requests")
    total_records = cursor.fetchone()["cnt"]

    base_query = "SELECT * FROM purchase_requests"
    where_clause = ""
    params = []

    # Validasi kolom dan arah order
    allowed_columns = [
        "id",
        "name",
        "requester",
        "description",
        "date",
        "jumlah",
        "unit",
        "notes",
        "received_date",
        "status",
    ]
    allowed_dirs = ["ASC", "DESC"]

    if order_column not in allowed_columns:
        order_column = "id"
    if order_dir.upper() not in allowed_dirs:
        order_dir = "ASC"

    # Pencarian
    if search_value:
        search_query = f"%{search_value}%"
        where_clause = """
            WHERE name LIKE %s OR notes LIKE %s OR description LIKE %s OR status LIKE %s
        """
        params.extend([search_query, search_query, search_query, search_query])

    # Query utama dengan LIMIT dan OFFSET
    query = f"{base_query} {where_clause} ORDER BY {order_column} {order_dir} LIMIT %s OFFSET %s"
    params.extend([length, start])

    try:
        cursor.execute(query, params)
        data = cursor.fetchall()

        # Hitung filtered count
        if search_value:
            cursor.execute(
                f"SELECT COUNT(*) as cnt FROM purchase_requests {where_clause}",
                [search_query, search_query, search_query, search_query],
            )
            filtered_records = cursor.fetchone()["cnt"]
        else:
            filtered_records = total_records

        # Format date
        for row in data:
            if row.get("date"):
                try:
                    row["date"] = datetime.strptime(
                        str(row["date"]), "%Y-%m-%d"
                    ).strftime("%Y-%m-%d")
                except:
                    pass
                
            if row.get("received_date"):
                try:
                    row["received_date"] = datetime.strptime(
                        str(row["date"]), "%Y-%m-%d"
                    ).strftime("%Y-%m-%d")
                except:
                    pass
        

    except Exception as e:
        print("Database error:", e)
        data = []
        filtered_records = 0

    finally:
        cursor.close()
        conn.close()

    return data, total_records, filtered_records


def insert_pr(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO purchase_requests 
        (name, requester, description, date, jumlah, unit, url, status, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """,
        data,
    )
    conn.commit()
    cursor.close()
    conn.close()


def update_pr(id, data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE purchase_requests 
        SET name=%s, requester=%s, description=%s, date=%s, jumlah=%s, unit=%s, url=%s, status=%s, notes=%s
        WHERE id=%s
    """,
        (*data, id),
    )
    conn.commit()
    cursor.close()
    conn.close()


def delete_pr(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM purchase_requests WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
