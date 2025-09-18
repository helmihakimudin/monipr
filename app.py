from flask import Flask
from controllers import pr_controller

app = Flask(__name__)
app.secret_key = "supersecretkey123"  # kasih string random panjang


# Routing
app.add_url_rule("/", "index", pr_controller.index)
app.add_url_rule("/add", "add_pr", pr_controller.add_pr, methods=["POST"])
app.add_url_rule(
    "/delete/<int:id>", 
    "remove_pr", 
    pr_controller.remove_pr, 
    methods=["POST", "DELETE"]
)

app.add_url_rule("/prs/data", "datatable", pr_controller.datatable)
app.add_url_rule("/get-reference", "get_reference_id", pr_controller.get_reference_id)
app.add_url_rule(
    "/item-purchase/data/<int:id>",
    "item_purchase_datatable",
    pr_controller.item_purchase_datatable,
)
app.add_url_rule(
    "/item-purchase-erp/data/<string:id>",
    "item_purchase_datatable_erp",
    pr_controller.item_purchase_erp_datatable,
)
app.add_url_rule(
    "/get-items-data/<int:pr_id>",
    "get_items_data",
    pr_controller.get_edit_items_controller,
)
app.add_url_rule(
    "/update/<int:pr_id>",
    "update_pr",
    pr_controller.update_pr_controller,
    methods=["POST"],
)


if __name__ == "__main__":
    app.run(debug=True)
