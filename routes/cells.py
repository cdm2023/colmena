from flask import render_template, request, url_for
from __main__ import app
import maxx_db
from maxx_db import MaxxConn
from datetime import datetime
from datetime import date

@app.route('/add_cell', methods=["GET","POST"])
def add_cell():
    if request.method=="POST":
        rf = dict(request.form.items())
        ret = maxx_db.cells.insert_cell(rf)
        if ret:
            cells = maxx_db.cells.get_cells()
            return render_template("cells/list_cells.html", cells=cells)
        else:
            return "add_cell()  failed"

    cells= maxx_db.cells.get_cells()
    return render_template("cells/add_cell.html", cells=cells)



@app.route('/list_inventory', methods = ["GET","POST"])
def list_inventory():
    if request.method == "POST":
        x = request.form.get('item_cell_id')
        if int(x) > 10000:
           # return f" list_inv() 29 This is a cell: cell_id= {x} "
            cell = maxx_db.cells.get_cell(x)
          #  return f" list_inv() 31 This is a cell: cell_id= {x} "

            items = maxx_db.items.get_cell_items(x)
         #   return f" list_inv() 33 This is a cell: cell_items= {items} "

            cells = maxx_db.cells.get_all_cells()
       #     return f"35 list_inventory() POST cells: {cells}"
            return render_template('cells/view_cell.html', cell = cell, items=items, cells=cells)

        else:
            return f"This is a machine: {x}"
        return f"x: {x}"

        return f"item_cell_id: {item_cell_id}"

    cells = maxx_db.cells.get_cells()
    return render_template("cells/list_inventory.html", cells_items = cells)


@app.route('/view_cell', methods=["GET","POST"])
def view_cell():
    if request.method == "POST":
        if request.form['btnDoItem'] == "move":  # check if value is "add-update"
            return f"50 cells.py: view_cell: move"
        else:
            return f"50 cells.py: view_cell: history"
    #return "<h3> view_cell()</h3>"
    cell_id = request.form.get('cell_id')
    cell = maxx_db.cells.get_cell(cell_id)
    cells = maxx_db.cells.get_all_cells()

    #return str(cell)
    return render_template("cells/view_cell.html", cell=cell, cells = cells)


@app.route('/select_cell', methods=["GET","POST"])
def select_cell():
    if request.method == 'POST':
        cell_id = request.form.get('cell_id')
        cell = maxx_db.cells.get_cell(cell_id)
        items = maxx_db.cells.get_items_for_cell(cell_id)
        if cell:
           # return url_for('list_items')
            return render_template("cells/cell_detail.html", cell=cell, items=items)
        else:
            return f"Cell not found: {cell_id}"
    cells = maxx_db.cells.get_cells()
    return render_template("cells/select_cell.html", cells=cells)


@app.route("/propose_transfer", methods=['GET', 'POST'])
def propose_transfer():
    itemID = request.form.get('item_id')
    targetCell_id = request.form.get('target_cell_id')
    fromCell_id = request.form.get('from_cell_id')

    itemSQL = "INSERT INTO items(item_name,cell_id, serial_number, product_number) VALUES (%s,%s,%s,%s) "
    itemPars = (obj['item_name'], obj['cell_id'],obj['serial_number'], obj['product_number'],)
    # ========================       GET item_name, serial_number ('item_data')  to display in confirm_transfer.html     ==================================
    # ========================       GET cell_name[s] to display ....    =====================================================
    #SELECT item_id, item_name, serial_number, product_number
    rf = dict(request.form.items())
    item_data = maxx_db.items.get_item(itemID)

    # curFactotum = mysql.connection.cursor()
    # sqlItem = "SELECT item_id, item_name, serial_number FROM  items WHERE item_id = %s"
    # curFactotum.execute(sqlItem, (itemID,))
    # item_data = curFactotum.fetchone()

    sqlCelldata = "SELECT cell_id, cell_name FROM cells WHERE cell_id = %s"
    curFactotum.execute(sqlCelldata, (fromCell_id,));
    from_cell_data = curFactotum.fetchone()

    curFactotum.execute(sqlCelldata, (targetCell_id,));
    to_cell_data = curFactotum.fetchone()

    curFactotum.close()
    return render_template("cells/propose_transfer.html", item_data=item_data, from_cell_data=from_cell_data, to_cell_data=to_cell_data)



@app.route("/confirm_transfer", methods=['GET', 'POST'])
def confirm_transfer():
    if request.method == 'POST':
        # ===========================      INSERT TRANSFER   =====================================
        itemID = request.form.get('item_id')
        targetCell_id = request.form.get('to_cell_id')
        fromCell_id = request.form.get('from_cell_id')
        notes = request.form.get('notes')
        user_id = session['user_id']
        now = datetime.now()
        t_date = now.strftime('%Y-%m-%d')
        curTransfer = mysql.connection.cursor()
        sqlTransfer = '''INSERT INTO transfers(item_id,user_id, target_cell_id, source_cell_id, trans_date, notes) VALUES (%s,%s,%s,%s,%s,%s)'''
        curTransfer.execute(sqlTransfer, (itemID, user_id, targetCell_id, fromCell_id, t_date, notes,))
        # ========================       GET item_name, serial_number ('item_data')  to display in confirm_transfer.html     ==================================
        # ========================       GET cell_name[s] to display ....    =====================================================
        curFactotum = mysql.connection.cursor()
        sqlItemID = "SELECT item_name, serial_number FROM  items WHERE item_id = %s"
        curFactotum.execute(sqlItemID, (itemID,))
        item_data = curFactotum.fetchone()

        sqlCellname = "SELECT cell_name FROM cells WHERE cell_id = %s"
        curFactotum.execute(sqlCellname, (fromCell_id,));
        from_cell_data = curFactotum.fetchone()

        curFactotum.execute(sqlCellname, (targetCell_id,));
        to_cell_data = curFactotum.fetchone()

        curFactotum.close()

        # ========================       UPDATE cell_id IN items TABLE     ==================================

        curItemUpdate = mysql.connection.cursor()
        sqlItemUpdate = "UPDATE items SET cell_id = %s WHERE item_id = %s"
        curItemUpdate.execute(sqlItemUpdate, (targetCell_id, itemID,))
        mysql.connection.commit()
        curItemUpdate.close()

        # ========================       DISPLAY DETAILS OF THE TRANSFER:  ===================================
        curLastID = mysql.connection.cursor()
        curLastID.execute('SELECT LAST_INSERT_ID()')
        last_id = curLastID.fetchone()
        curLastID.close()

        curTransfer = mysql.connection.cursor()
        sqlTransfer = "SELECT c1. cell_name as from_cell, c2.cell_name as to_cell, t.trans_date, t.notes FROM  transfers t join cells c1 on (t.source_cell_id=c1.cell_id)  join cells c2 on (t.target_cell_id=c2.cell_id)  WHERE t.transfer_id = %s"

        curTransfer.execute(sqlTransfer, (last_id,))
        db_transfer = curTransfer.fetchone()
        curTransfer.close()
        return render_template('cells/confirm_transfer.html', db_transfer=db_transfer, item_data=item_data,
                               to_cell_data=to_cell_data, from_cell_data=from_cell_data)

# @app.route('/select_cell_item', methods = ['GET','POST'])
# def select_cell_item():
#     if request.method == "POST":
#         cell_id = request.form.get('cell_id')
#         item_id = request.form.get('item_id')
#         return f"cell_id: {cell_id}  item_id: {item_id}"

