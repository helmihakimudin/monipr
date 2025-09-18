from datetime import datetime
from config import get_db_connection
from config_erp import get_erp_connection
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


# def get_pr_datatable(start, length, search_value, order_column, order_dir):
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)

#     # Hitung total records
#     cursor.execute("SELECT COUNT(*) as cnt FROM purchase_requests")
#     total_records = cursor.fetchone()["cnt"]

#     base_query = "SELECT * FROM purchase_requests"
#     where_clause = ""
#     params = []

#     # Validasi kolom dan arah order
#     allowed_columns = [
#         "id",
#         "reference_id",
#         "requester",
#         "date",
#         "notes",
#     ]
#     allowed_dirs = ["ASC", "DESC"]

#     if order_column not in allowed_columns:
#         order_column = "id"
#     if order_dir.upper() not in allowed_dirs:
#         order_dir = "ASC"

#     # Pencarian
#     if search_value:
#         search_query = f"%{search_value}%"
#         where_clause = """
#             WHERE name LIKE %s OR notes LIKE %s OR description LIKE %s OR status LIKE %s
#         """
#         params.extend([search_query, search_query, search_query, search_query])

#     # Query utama dengan LIMIT dan OFFSET
#     query = f"{base_query} {where_clause} ORDER BY {order_column} {order_dir} LIMIT %s OFFSET %s"
#     params.extend([length, start])

#     try:
#         cursor.execute(query, params)
#         data = cursor.fetchall()

#         # Hitung filtered count
#         if search_value:
#             cursor.execute(
#                 f"SELECT COUNT(*) as cnt FROM purchase_requests {where_clause}",
#                 [search_query, search_query, search_query, search_query],
#             )
#             filtered_records = cursor.fetchone()["cnt"]
#         else:
#             filtered_records = total_records

#         # Format date
#         for row in data:
#             if row.get("date"):
#                 try:
#                     row["date"] = datetime.strptime(
#                         str(row["date"]), "%Y-%m-%d"
#                     ).strftime("%Y-%m-%d")
#                 except:
#                     pass

#             if row.get("received_date"):
#                 try:
#                     row["received_date"] = datetime.strptime(
#                         str(row["date"]), "%Y-%m-%d"
#                     ).strftime("%Y-%m-%d")
#                 except:
#                     pass

#     except Exception as e:
#         print("Database error:", e)
#         data = []
#         filtered_records = 0

#     finally:
#         cursor.close()
#         conn.close()

#     return data, total_records, filtered_records



def get_pr_datatable(start, length, search_value, order_column, order_dir):
    # koneksi ke database MySQL lokal
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # hasil query dict

    # hitung total data tanpa filter
    cursor.execute("SELECT COUNT(*) as cnt FROM purchase_requests")
    total_records = cursor.fetchone()["cnt"]

    base_query = "SELECT * FROM purchase_requests"
    where_clause = ""
    params = []

    allowed_columns = ["id", "reference_id", "requester", "date", "notes"]
    allowed_dirs = ["ASC", "DESC"]

    # validasi order column & direction
    if order_column not in allowed_columns:
        order_column = "id"
    if order_dir.upper() not in allowed_dirs:
        order_dir = "ASC"

    # search
    if search_value:
        search_query = f"%{search_value}%"
        where_clause = """
            WHERE requester LIKE %s OR notes LIKE %s OR reference_id LIKE %s
        """
        params.extend([search_query, search_query, search_query])

    # query utama dengan limit & offset
    query = f"{base_query} {where_clause} ORDER BY {order_column} {order_dir} LIMIT %s OFFSET %s"
    params.extend([length, start])

    try:
        cursor.execute(query, params)
        data = cursor.fetchall()

        # hitung filtered count
        if search_value:
            cursor.execute(
                f"SELECT COUNT(*) as cnt FROM purchase_requests {where_clause}",
                [search_query, search_query, search_query],
            )
            filtered_records = cursor.fetchone()["cnt"]
        else:
            filtered_records = total_records

        # ambil PR Number & Status dari ERP SQL Server
        if data:
            erp_conn = get_erp_connection()
            erp_cursor = erp_conn.cursor()

            reference_ids = [
                row["reference_id"] for row in data if row.get("reference_id")
            ]

            if reference_ids:
                placeholders = ",".join("?" for _ in reference_ids)
                erp_query = f"""
                    SELECT t_refb, t_rqno, t_rqst
                    FROM ttdpur200700
                    WHERE t_refb IN ({placeholders})
                """
                erp_cursor.execute(erp_query, reference_ids)

                # ambil semua hasil ERP
                erp_raw = erp_cursor.fetchall()

                # mapping ERP + cek duplicated
                erp_data = {}
                for row_erp in erp_raw:
                    ref = row_erp[0]
                    pr_no = row_erp[1]
                    pr_status = row_erp[2]
                    if ref in erp_data:
                        existing = erp_data[ref]
                        if isinstance(existing, list):
                            existing.append(
                                {"pr_number": pr_no, "pr_status": pr_status}
                            )
                        else:
                            erp_data[ref] = [
                                existing,
                                {"pr_number": pr_no, "pr_status": pr_status},
                            ]
                    else:
                        erp_data[ref] = {"pr_number": pr_no, "pr_status": pr_status}

                # gabungkan hasil ERP ke data utama
                for row_main in data:
                    ref = row_main["reference_id"]
                    if ref in erp_data:
                        val = erp_data[ref]
                        if isinstance(val, list):
                            # duplicated → bisa alert
                            row_main["pr_number"] = ", ".join(
                                [v["pr_number"] for v in val]
                            )
                            row_main["pr_status"] = 99
                        else:
                            row_main["pr_number"] = val["pr_number"]
                            row_main["pr_status"] = val["pr_status"]
                    else:
                        row_main["pr_number"] = None
                        row_main["pr_status"] = None

            # tutup koneksi ERP
            erp_cursor.close()
            erp_conn.close()

        # format tanggal
        for row in data:
            if row.get("date"):
                try:
                    row["date"] = datetime.strptime(
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
        (item, reference_id, requester, date, jumlah, unit, url, status, notes)
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
    cursor.execute("""DELETE FROM item_purchases WHERE pr_id=%s""", (id,))
    cursor.execute("""DELETE FROM purchase_requests WHERE id=%s""", (id,))
    conn.commit()
    cursor.close()
    conn.close()


def get_reference_id():
    conn = get_db_connection()
    cursor = conn.cursor()

    year_short = datetime.now().strftime("%y")

    cursor.execute("START TRANSACTION")

    cursor.execute(
        """
        SELECT reference_id
        FROM purchase_requests
        WHERE reference_id LIKE %s
        ORDER BY reference_id DESC
        LIMIT 1
        FOR UPDATE
        """,
        (f"PR-{year_short}%",),
    )
    row = cursor.fetchone()

    if row:
        last_ref = row[0]
        last_number = int(last_ref[6:])
        next_number = last_number + 1
    else:
        next_number = 1

    new_ref = f"PR-{year_short}{next_number:05d}"
    return new_ref  # jangan lupa commit setelah insert


def insert_pr_header(reference_id, requester, date):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO purchase_requests (reference_id, requester, date)
        VALUES (%s, %s, %s)
        """,
        (reference_id, requester, date),
    )

    pr_id = cursor.lastrowid  # ✅ ambil id terakhir dari insert

    conn.commit()
    cursor.close()
    conn.close()
    return pr_id


def insert_pr_item(item, qty, unit, url, remarks, pr_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO item_purchases (item, qty, unit, url, remarks, pr_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (item, qty, unit, url, remarks, pr_id),
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_purchase_items(
    pr_id, start=0, length=10, search_value=None, order_column="id", order_dir="ASC"
):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Kolom yang boleh di-order
    allowed_columns = ["id", "item", "qty", "unit", "remarks", "url"]
    allowed_dirs = ["ASC", "DESC"]

    if order_column not in allowed_columns:
        order_column = "id"
    if order_dir.upper() not in allowed_dirs:
        order_dir = "ASC"

    params = [pr_id]

    # Hitung total records untuk pr_id ini
    cursor.execute(
        "SELECT COUNT(*) as cnt FROM item_purchases WHERE pr_id = %s", (pr_id,)
    )
    total_records = cursor.fetchone()["cnt"]

    # Filter pencarian
    where_clause = "WHERE pr_id = %s"
    if search_value:
        search_query = f"%{search_value}%"
        where_clause += " AND (item LIKE %s OR remarks LIKE %s OR unit LIKE %s)"
        params.extend([search_query, search_query, search_query])

    # Query utama
    query = f"""
        SELECT id, item, qty, unit, url, remarks
        FROM item_purchases
        {where_clause}
        ORDER BY {order_column} {order_dir}
        LIMIT %s OFFSET %s
    """
    params.extend([length, start])

    try:
        cursor.execute(query, params)
        data = cursor.fetchall()

        # Hitung filtered count
        if search_value:
            cursor.execute(
                f"SELECT COUNT(*) as cnt FROM item_purchases {where_clause}",
                params[:-2],  # buang limit+offset
            )
            filtered_records = cursor.fetchone()["cnt"]
        else:
            filtered_records = total_records

        # === Ambil PR Number dari ERP SQL Server ===
        if data:  # hanya kalau ada data
            erp_conn = get_erp_connection()  # koneksi ke ERP SQL Server
            erp_cursor = erp_conn.cursor()

            # ambil semua reference_id dari hasil query lokal
            reference_ids = [
                row["reference_id"] for row in data if row.get("reference_id")
            ]

            if reference_ids:  # kalau ada reference_id yang valid
                # buat placeholder sesuai jumlah reference_id -> ?,?,?,...
                placeholders = ",".join("?" for _ in reference_ids)

                # query ERP berdasarkan reference_id
                erp_query = f"""
                    SELECT t_refb, t_rqno, t_rqst
                    FROM ttdpur200700
                    WHERE t_refb IN ({placeholders})
                """

                # eksekusi query ERP
                erp_cursor.execute(erp_query, reference_ids)

                # hasil query ERP dimapping ke dict {t_refb: t_rqno}
                erp_data = {
                    row[0]: {"pr_number": row[1], "pr_status": row[2]}
                    for row in erp_cursor.fetchall()
                }
                print("data", erp_data)
                # gabungkan hasil ERP ke data utama
                for row in data:
                    ref = row["reference_id"]
                    if ref in erp_data:
                        row["pr_number"] = erp_data[ref]["pr_number"]
                        row["pr_status"] = erp_data[ref]["pr_status"]
                    else:
                        row["pr_number"] = None
                        row["pr_status"] = None

            # tutup koneksi ERP
            erp_cursor.close()
            erp_conn.close()

    except Exception as e:
        print("Database error:", e)
        data = []
        filtered_records = 0

    finally:
        cursor.close()
        conn.close()

    return data, total_records, filtered_records


def get_purchase_items_erp(
    pr_id, start=0, length=10, search_value=None, order_column="t_item", order_dir="ASC"
):
    conn = get_erp_connection()
    cursor = conn.cursor()

    allowed_columns = [
        "t_rqno",
        "t_item",
        "t_nids",
        "t_qoor",
        "t_cuqp",
        "t_cnty",
        "t_prno",
    ]
    allowed_dirs = ["ASC", "DESC"]

    if order_column not in allowed_columns:
        order_column = "a.t_item"
    if order_dir.upper() not in allowed_dirs:
        order_dir = "ASC"

    # pastikan pr_id berupa list
    if isinstance(pr_id, str):
        pr_id = [x.strip() for x in pr_id.split(",")]

    placeholders = ",".join("?" for _ in pr_id)
    params = pr_id[:]

    # Hitung total records
    cursor.execute(
        f"""
        SELECT COUNT(*) as cnt
        FROM ttdpur201700 a
        LEFT JOIN ttdpur202700 b ON a.t_rqno = b.t_rqno
        WHERE a.t_rqno IN ({placeholders})
        """,
        params,
    )
    total_records = cursor.fetchone()[0]

    # Filter pencarian
    where_clause = f"WHERE a.t_rqno IN ({placeholders})"
    if search_value:
        search_query = f"%{search_value}%"
        where_clause += " AND (a.t_nids LIKE ?)"
        params.append(search_query)

    # Query utama
    query = f"""
        SELECT a.t_rqno, a.t_item, a.t_nids, a.t_qoor, a.t_cuqp, a.t_cnty, b.t_prno
        FROM ttdpur201700 a
        LEFT JOIN ttdpur202700 b ON a.t_rqno = b.t_rqno
        {where_clause}
        ORDER BY {order_column} {order_dir}
        OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
    """
    params.extend([start, length])

    try:
        cursor.execute(query, params)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        data = [dict(zip(columns, row)) for row in rows]

        # Hitung filtered count
        if search_value:
            cursor.execute(
                f"""
                SELECT COUNT(*) as cnt
                FROM ttdpur201700 a
                LEFT JOIN ttdpur202700 b ON a.t_rqno = b.t_rqno
                {where_clause}
                """,
                params[:-2],  # buang offset+limit
            )
            filtered_records = cursor.fetchone()[0]
        else:
            filtered_records = total_records

    except Exception as e:
        print("Database error:", e)
        data = []
        filtered_records = 0

    finally:
        cursor.close()
        conn.close()

    return data, total_records, filtered_records


def get_edit_items(pr_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT item, qty, unit, url, remarks
        FROM item_purchases
        WHERE pr_id = %s
    """
    # param HARUS tuple → (pr_id,)
    cursor.execute(query, (pr_id,))
    rows = cursor.fetchall()

    result = []
    for row in rows:
        result.append(
            {
                "name": row[0],
                "qty": row[1],
                "unit": row[2],
                "url": row[3],
                "note": row[4],
            }
        )

    cursor.close()
    conn.close()
    return result


def update_pr_model(pr_id, reference_id, requester, date, items_grouped):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Update header PR
        update_header = """
            UPDATE purchase_requests
            SET reference_id=%s, requester=%s, date=%s
            WHERE id=%s
        """
        cursor.execute(update_header, (reference_id, requester, date, pr_id))

        # Hapus item lama
        cursor.execute("DELETE FROM item_purchases WHERE pr_id=%s", (pr_id,))

        # Insert item baru
        insert_item = """
            INSERT INTO item_purchases (pr_id, item, qty, unit, url, remarks)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        for _, item in items_grouped.items():
            cursor.execute(
                insert_item,
                (
                    pr_id,
                    item.get("name", ""),
                    item.get("qty", 0),
                    item.get("unit", ""),
                    item.get("url", ""),
                    item.get("note", ""),
                ),
            )

        conn.commit()
        return True, "PR updated successfully!"

    except Exception as e:
        conn.rollback()
        return False, str(e)

    finally:
        cursor.close()
        conn.close()
