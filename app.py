from flask import Flask
from controllers import pr_controller

app = Flask(__name__)

# Routing
app.add_url_rule('/', 'index', pr_controller.index)
app.add_url_rule('/add', 'add_pr', pr_controller.add_pr, methods=['POST'])
app.add_url_rule('/update/<int:id>', 'edit_pr', pr_controller.edit_pr, methods=['POST'])
app.add_url_rule('/delete/<int:id>', 'remove_pr', pr_controller.remove_pr)
app.add_url_rule("/prs/data", "datatable", pr_controller.datatable)


if __name__ == '__main__':
    app.run(debug=True)
