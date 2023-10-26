from flask import render_template, request
from __main__ import app
import maxx_db
from maxx_db import MaxxConn

@app.route('/do_item', methods=["GET","POST"])
def do_item():
    if request.method == "POST":
        b = request.form.get('btnDoItem')
        id = request.form.get('item_id')
        cell_id = request.form.get('cell_id')
        if b == 'history':
            item = maxx_db.items.get_item(id)   # item: ((12, 'Emerald 116', '3728196523', 'PR344MN77'),)
            transfers = maxx_db.items.get_item_transfers(id)
    #        return f"do_item() transfers: {transfers}"
            return render_template('items/item_history.html', transfers=transfers, item=item)

        elif b == 'move':
           # return f"20  do_item(): /routes/cells/propose_transfer() MOVE {id} to {cell_id}"
            item_data = (('alpha','a'),)
            from_cell_data = (('beta','b'),)
            to_cell_data = (('gamma', 'g'),)
          #  return f"23 items.py id: {item_data}  fcd: {from_cell_data} tcd: {to_cell_data}"
            return render_template("cells/propose_transfer.html", item_data=item_data, from_cell_data=from_cell_data,
                           to_cell_data=to_cell_data)

    return "Apparently this is do_item GET"
#
# def get_items():
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT i.item_id,i.item_name, i.serial_number, i.product_number, c.cell_name FROM items i JOIN cells c ON (i.cell_id=c.cell_id) ORDER BY 2")
#     items = cur.fetchall()
#     cur.close()
#     return items


@app.route('/list_items', methods=["GET","POST"])
def list_items():
    items = maxx_db.items.get_items()
    cells = maxx_db.cells.get_bare_cells()
    return render_template("items/list_items.html", items=items,cells=cells)

@app.route('/route_test2', methods=['GET'])
def route_test2():
    return 'it works here, too!'

@app.route('/add_item', methods=["GET","POST"])
def add_item():
    if request.method == "POST":
        rf = dict(request.form.items())
        ret = maxx_db.items.insert_item(rf)
        if ret:
            items = maxx_db.items.get_items()
            return render_template("items/list_items.html", items=items)
        else:
            return "Item INSERT failed"
    return render_template("items/add_item.html")


@app.route("/item_search", methods=["GET","POST"])
def item_search():
    # if not (session['user_can_search']):
    #     return "<h3 style='color:#9C3020'> 797 User not permitted to search for items</h3>"
    if request.method == "POST":
      #  curSearch = mysql.connection.cursor()
        search_by_in = request.form.get('search_term')
        search_by_param = search_by_in.upper()
       # return f"68 search_by_param: {search_by_param}"
        param = '%'+ search_by_param + '%'

        found_items = maxx_db.items.search_items(param)
        return render_template("items/found_items.html", search_by=search_by_in, found_items=found_items)
    return render_template("items/item_search.html")


@app.route("/show_item", methods=['GET', 'POST'])
def show_item():
    #  =========== get the item details to display  ==================
    itemID = request.form.get('item_id')
    item = maxx_db.items.get_item(itemID)
    cells = maxx_db.cells.get_transfer_cells()
    transfers = maxx_db.items.get_item_transfers(itemID)
    return render_template('items/show_item.html', item=item, cells=cells, transfers=transfers)


@app.route('/transfer_item', methods=["GET","POST"])
def transfer_item():
    if request.method == "POST":
#        item_id = dict(request.form.get('item_id'))
#         item_id = request.form.get('item_id')
#         cell_id = request.form.get('cell_id')
#        # return  render_template('items/item_transfered.html', item_id=item_id, cell_id=cell_id)
        rf = dict(request.form.items())  #NOT   "form.cells()  !!
        #return f"94 routes/items.py transfer_item() rf: {rf} "
        ret = maxx_db.items.transfer_item(rf)
        if ret:
           # return "97 items.py transfer_item():  Transfer ready to confirm"
            cells = maxx_db.cells.get_cells()
            return render_template("items/blank.html", cells=cells)
        else:
            return "Cell TRANSFER failed"
    return render_template("items/blank.html")

@app.route('/add_to_catalog', methods=["GET","POST"])
def add_to_catalog():
    if request.method == "POST":
        rf = dict(request.form.items())
        ret = maxx_db.items.insert_catalog(rf)
        if ret:
            return render_template("items/add_to_catalog.html")
        else:
            return "Item INSERT failed"
    return render_template("items/add_to_catalog.html")


@app.route('/list_catalog', methods=["GET","POST"])
def list_catalog():
    catalog = maxx_db.items.get_catalog()
    return render_template("items/list_catalog.html", catalog=catalog)

@app.route('/list_scan', methods=["GET","POST"])
def list_scan():
    cage_items = {'alpha': [1234, 5678], 'beta': [9876, 5432]}
#    items = maxx_db.items.get_catalog()
    return render_template("items/list_scan.html", cage_items=cage_items)



@app.route('/scan_cells', methods=['GET','POST'])
def scan_cells():
    if request.method == "POST":
        cages = {}
        cage_ids = []
        cell_ids = [100001,100002,100003,100004,100005,100006,100007,100008,100009,100010,100011,100012]
        for id in cell_ids:
            cage_ids.append(str(id))
      #  cage_ids = [100001,100002,100003,100004,100005,100006,100007,100008,100009,100010,100011,100012]
 #  SO: strings:  cage_ids = ['100001','100002','100003','100004','100005','100006','100007','100008','100009','100010','100011','100012']
        data_in = request.form.get('clicks')
        barcodes = data_in.split()
        #return f"136 /routes/items/scan_cells(): clicks as list: {barcodes}"
        current_c_id = 0
        for bc in barcodes:
  #  possibilities:    123456789   or   BX123456
            if bc.isdigit():
                int_bc = int(bc)
                if int_bc in cell_ids:
                    current_c_id = str(int_bc)
                    # because this will be a new cell_id, by the nature of the data,
                    # and we need the key, to avoid "key error"
                    cages[current_c_id]=[]
                else:
                    # not in cage_ids, so will never be a new {key}
                    cages[current_c_id].append(bc)
            else:
                cages[current_c_id].append(bc)

        if cages:   # There is at least one cell with something (item) in it
          #  return f"159 We have cage_items: {cages}"
            cage_items = []
      #  INSERT THE BASE SCAN object:
            ret_tuple = maxx_db.items.insert_cell_scan(1)   # user==1
            insert_scan_id = ret_tuple[0][0]
            for key in cages.keys():   #  164 cage_items.keys(): (['100001', '100002'])
      # INSERT THE ITEMS of this scan:
            #    id_test = []
                for sn in cages[key]:
                 # insert each into cell_scans:
                    scan_item_id = maxx_db.items.get_scan_item_id(sn)
                    item_id = scan_item_id[0][0]
               #     id_test.append((ret_item_id,item_id,))
                    #id_test.append(ret_item_id)

                    z=int(key)
                    ok = maxx_db.items.insert_scan_item(insert_scan_id,item_id,z)
                    if not ok:
                        return f"175 NOPE scan: {insert_scan_id}, item: {item_id}, cell: {z}"

               #                           def get_scan_items(scan_id):
            scan_items = maxx_db.items.get_scan_items(insert_scan_id)
            if scan_items:
                    # if found:
                    #     cage_items.append(found)
                # return f"182 id_test list={id_test}"
                return render_template("items/list_scan.html", scan_items=scan_items)
            else:
                return "189 /routes/items:  no scan_items"
    return render_template("items/scan_cells.html")

