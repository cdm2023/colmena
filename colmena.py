import yaml
from flask import Flask, render_template, request, g
from flask_mysqldb import MySQL
import multidict
db_conf = yaml.safe_load(open('db.yaml'))

app = Flask(__name__)
#from routes.items import item_route1

mysql = MySQL(app)
# maxxCur = None

app.config['SECRET_KEY'] = '0us0ntlesne1ges'
app.config['MYSQL_HOST'] = db_conf['mysql_host']
app.config['MYSQL_USER'] = db_conf['mysql_user']
app.config['MYSQL_PASSWORD'] = db_conf['mysql_password']
app.config['MYSQL_DB'] = db_conf['mysql_db']
app.config['DEBUG'] = db_conf['debug']

import maxx_db
from maxx_db import items
from maxx_db import cells
from maxx_db import users
from maxx_db import classes
from maxx_db import viking

from routes import colmena
from routes import items
from routes import users
from routes import classes
from routes import cells
from routes import viking


# @app.before_request
# def before_request():
#     maxxCur = mysql.connection.cursor()
#    g.conn = mysql.connection
#    g.cursor = g.conn.cursor()

# @app.teardown_request
# def teardown_request(exception):
#     if hasattr(g, 'cursor'):
#         g.cursor.close()
#     if hasattr(g, 'conn'):
#         g.conn.close()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mysql2')
def mysql2():
    rf = {'item_name':'item1714',
          'cell_id':'2',
          'serial_number':'SN23423444',
          'product_number':'P23439023'}
    #        ret = maxx_db.cells.insert_cell(rf)
    ret = maxx_db.items.insert_item(rf)
    if ret:
        return f'inserted: {rf} '


@app.route('/mysql')
def mysql_():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM cells')
        data=cur.fetchall()
       # data = g.cursor.fetchall()
        #g.cursor.close()
        return str(data)
    except Exception as error:
        return f"No joy: {error}"
        #cursor.close()


@app.route('/select_item', methods=["GET","POST"])
def select_item():
    if request.method == 'POST':
        item_id = request.form.get('item_id')
        item = maxx_db.items.get_item(item_id)
        if item:
           # return url_for('list_items')
            return render_template("items/item_detail.html", item=item)
        else:
            return f"Item not found: {item_id}"
    items = maxx_db.items.get_items()
    return render_template("items/select_item.html", items=items)

# @app.route('/transfer_item', methods=["GET","POST"])
# def transfer_item():
#     if request.method == "POST":
# #        item_id = dict(request.form.get('item_id'))
# #         item_id = request.form.get('item_id')
# #         cell_id = request.form.get('cell_id')
# #        # return  render_template('items/item_transfered.html', item_id=item_id, cell_id=cell_id)
#         rf = dict(request.form.items())  #NOT   "form.cells()  !!
#         ret = maxx_db.items.transfer_item(rf)
#         if ret:
#             cells = maxx_db.cells.get_cells()
#             return render_template("cells/list_cells.html", cells=cells)
#         else:
#             return "Cell TRANSFER failed"
#     return render_template("cells/list_cells.html")
#


    #     ret = maxx_db.items.insert_item(rf)
    #     if ret:
    #         items = maxx_db.items.get_items()
    #         return render_template("items/list_items.html", items=items)
    #     else:
    #         return "Item INSERT failed"
    # return render_template("items/add_item.html")

# @app.route('/add_cell', methods=["GET","POST"])
# def add_cell():
#     if request.method == "POST":
#         rf = dict(request.form.items())  #NOT   "form.cells()  !!
#         ret = maxx_db.cells.insert_cell(rf)
#         if ret:
#             cells = maxx_db.cells.get_cells()
#             return render_template("cells/list_cells.html", cells=cells)
#         else:
#             return "Cell INSERT failed"
#     return render_template("cells/add_cell.html")





# @app.route('/view_cell', methods=["GET","POST"])
# def view_cell():
#     #return "<h3> view_cell()</h3>"
#     cell_id = request.form.get('cell_id')
#     cell = maxx_db.cells.get_cell(cell_id)
#     #return str(cell)
#     return render_template("cells/cell_detail.html", cell=cell)


@app.route('/list_transfers', methods=["GET","POST"])
def list_transfers():
    transfers = maxx_db.items.get_transfers()
    return render_template("items/list_transfers.html", cells=cells)



@app.route('/testX', methods=["GET","POST"])
def testX():
    if request.method == "POST":
        rqf = request.form.getlist('cb_test')
        perms=0
        if rqf:
            for p in rqf:
                perms +=int(p)
        return f"perms: {perms}"

       # rf = dict(request.form.items())  # NOT   "form.cells()  !!

        return render_template('testx.html',rqf=rqf )
    return render_template('testx.html')


@app.route('/blank', methods = ["GET","POST"])
def blank():
    if request.method == "POST":
        item_id = request.form.get('item_id')
        item = maxx_db.items.get_item(item_id)
        return render_template("items/blank.html", item=item)
    return render_template("items/blank.html" )

@app.route('/oct16')
def oct16():
    return render_template('oct16.html')


if __name__ == '__main__':
    app.run(debug=True, port=5002)