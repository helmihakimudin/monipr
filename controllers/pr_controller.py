from flask import render_template, request, redirect, jsonify
from models.pr_model import get_pr_datatable, insert_pr, update_pr, delete_pr


def index():
    return render_template("index.html")


def add_pr():
    data = (
        request.form["name"],
        request.form["requester"],
        request.form["description"],
        request.form["date"],
        request.form["jumlah"],
        request.form["unit"],
        request.form["url"],
        request.form["status"],
        request.form["notes"],
    )
    insert_pr(data)
    return redirect("/")


def edit_pr(id):
    data = (
        request.form["name"],
        request.form["requester"],
        request.form["description"],
        request.form["date"],
        request.form["jumlah"],
        request.form["unit"],
        request.form["url"],
        request.form["status"],
        request.form["notes"],
    )
    
    print("DEBUG data:", data)  # <--- ini akan muncul di console / terminal

    update_pr(id, data)
    return redirect("/")


def remove_pr(id):
    delete_pr(id)
    return redirect("/")


# 🔹 Endpoint untuk DataTables AJAX
def datatable():
    draw = int(request.args.get("draw", 1))
    start = int(request.args.get("start", 0))
    length = int(request.args.get("length", 10))
    search_value = request.args.get("search[value]", "")

    # ambil index kolom yang di-order
    order_column_index = request.args.get("order[0][column]", "0")
    order_dir = request.args.get("order[0][dir]", "asc")

    # mapping kolom DataTables → kolom database
    columns = ["id", "name", "description", "date", "jumlah", "unit", "url", "received_date", "status", "notes", "name"]
    order_column = columns[int(order_column_index)]

    data, records_total, records_filtered = get_pr_datatable(
        start, length, search_value, order_column, order_dir
    )

    return jsonify(
        {
            "draw": draw,
            "recordsTotal": records_total,
            "recordsFiltered": records_filtered,
            "data": data,
        }
    )
