from flask import render_template, request, redirect, jsonify, flash
from models.pr_model import (
    get_pr_datatable,
    insert_pr_header,
    insert_pr_item,
    update_pr,
    delete_pr,
    get_reference_id,
    get_purchase_items,
    get_purchase_items_erp,
    get_edit_items,
    update_pr_model,
)


def index():
    return render_template("index.html")


def add_pr():
    reference_id = request.form["reference_id"]
    requester = request.form["requester"]
    date = request.form["date"]

    # simpan header dulu
    pr_id = insert_pr_header(reference_id, requester, date)

    # parse items
    from collections import defaultdict

    grouped = defaultdict(dict)
    for key, value in request.form.items():
        if key.startswith("items["):
            idx = key.split("[")[1].split("]")[0]
            field = key.split("[")[2].split("]")[0]
            grouped[idx][field] = value

    for idx, item in grouped.items():
        insert_pr_item(
            item.get("name"),
            int(item.get("qty", 0)),
            item.get("unit"),
            item.get("url"),
            item.get("note"),
            pr_id,
        )

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
    return jsonify({"message": f"PR {id} berhasil dihapus"}), 200



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
    columns = ["id", "reference_id", "requester", "date", "notes"]
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


def item_purchase_datatable(id):
    draw = int(request.args.get("draw", 1))
    start = int(request.args.get("start", 0))
    length = int(request.args.get("length", 10))
    search_value = request.args.get("search[value]", "")

    # ambil index kolom yang di-order
    order_column_index = request.args.get("order[0][column]", "0")
    order_dir = request.args.get("order[0][dir]", "asc")

    # mapping kolom DataTables → kolom database (item_purchases)
    columns = ["id", "item", "qty", "unit", "url", "remarks"]
    order_column = columns[int(order_column_index)]

    # ambil PR ID dari parameter
    pr_id = id  # <- gunakan id dari URL
    if not pr_id:
        return jsonify({"error": "Missing pr_id"}), 400

    # ambil data dari DB
    data, records_total, records_filtered = get_purchase_items(
        pr_id=pr_id,
        start=start,
        length=length,
        search_value=search_value,
        order_column=order_column,
        order_dir=order_dir,
    )

    return jsonify(
        {
            "draw": draw,
            "recordsTotal": records_total,
            "recordsFiltered": records_filtered,
            "data": data,
        }
    )


def item_purchase_erp_datatable(id):
    draw = int(request.args.get("draw", 1))
    start = int(request.args.get("start", 0))
    length = int(request.args.get("length", 10))
    search_value = request.args.get("search[value]", "")

    # ambil index kolom yang di-order
    order_column_index = request.args.get("order[0][column]", "0")
    order_dir = request.args.get("order[0][dir]", "asc")

    # mapping kolom DataTables → kolom database (item_purchases)
    columns = [
        "id",
        "t_rqno",
        "t_item",
        "t_nids",
        "t_qoor",
        "t_cuqp",
        "t_cnty",
        "t_prno",
    ]
    order_column = columns[int(order_column_index)]

    # ambil PR ID dari parameter
    pr_id = id  # <- gunakan id dari URL
    if not pr_id:
        return jsonify({"error": "Missing pr_id"}), 400

    # ambil data dari DB
    data, records_total, records_filtered = get_purchase_items_erp(
        pr_id=pr_id,
        start=start,
        length=length,
        search_value=search_value,
        order_column=order_column,
        order_dir=order_dir,
    )

    return jsonify(
        {
            "draw": draw,
            "recordsTotal": records_total,
            "recordsFiltered": records_filtered,
            "data": data,
        }
    )


def get_data_reference():
    new_ref = get_reference_id()
    return jsonify({"reference_id": new_ref})


def get_edit_items_controller(pr_id):
    data = get_edit_items(pr_id)
    return jsonify({"data": data})


def update_pr_controller(pr_id):
    reference_id = request.form.get("reference_id")
    requester = request.form.get("requester")
    date = request.form.get("date")

    # Parsing items dari form
    items_grouped = {}
    for key, value in request.form.items():
        if key.startswith("items["):
            idx = key.split("[")[1].split("]")[0]
            field = key.split("[")[2].split("]")[0]
            if idx not in items_grouped:
                items_grouped[idx] = {}
            items_grouped[idx][field] = value

    success, message = update_pr_model(
        pr_id, reference_id, requester, date, items_grouped
    )

    if success:
        flash(message, "success")
    else:
        flash(message, "error")

    return redirect("/")
