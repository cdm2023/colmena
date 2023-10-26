from flask import render_template, request, url_for
from __main__ import app
import maxx_db
from maxx_db import MaxxConn
from datetime import datetime
from datetime import date

@app.route('/why_not', methods= ['GET','POST'])
def why_not():
    if request.method == 'POST':
        cage_no = request.form.get("cage_no")
        cell_items = maxx_db.viking.get_cell_items(cage_id)

        return  render_template('viking/cell_items.html', cell_items = cell_items)
    return  render_template('viking/why_not.html')


@app.route('/choose_cell', methods= ['GET','POST'])
def choose_cell():
    if request.method == 'POST':
        cell_id = request.form.get("cell_id")
       # return f"22 choose_cell() cell_id: {cell_id} "
        cell_items = maxx_db.viking.get_items_for_cell(cell_id)

        return  render_template('viking/inv_cell_items.html', cell_items = cell_items)
    inv_cells = maxx_db.viking.get_inv_cells()
    return  render_template('viking/choose_cell.html', inv_cells = inv_cells)


@app.route('/update_counts', methods = ['GET','POST'])
def update_counts():
 #   return "32 update_counts()"
    if request.method == "POST":
        updates = []
        rqf = request.form
        for k,v in rqf.items():
             updates.append((k,v,))
#   34 update_counts() updates:
        #  updates:  [('item_id_52 ', '2'), ('item_id_53 ', '3'), ('item_id_54 ', '4'), ('item_id_55 ', '5'), ('item_id_56 ', '6'), ('item_id_57 ', '7')]
        if maxx_db.viking.update_counts(updates):
            return "<h4>41 update_counts() succeeded</h4>"
        else:
            return "<h4>43 update_counts() did NOT succeed</h4>"

        return f"34 update_counts() updates: {updates}"




@app.route('/inv_item', methods=['GET','POST'])
def inv_item():
    if request.method == "POST":
         i = request.form.get('item_id')
         return "routes/viking.view_inv_item()"


@app.route('/all_inv', methods= ["GET","POST"])
def all_inv():
    if request.method == "POST":
        id_id  = request.form.get('id_id')
        inv_item = maxx_db.viking.get_inv_item(id_id)
       # return f"inv_item: {inv_item}"
        meth = "POST"
        return render_template('viking/view_inv_item.html', inv_item=inv_item)

    meth="GET"
    inv_data = maxx_db.viking.get_inv_data()
    return render_template('viking/all_inv.html', inv_data=inv_data, meth=meth)


# <!--    if request.method == "POST":-->
# <!--        if request.form['btnDoItem'] == "move":  # check if value is "add-update"-->
# <!--            return f"50 cells.py: view_cell: move"-->
# <!--        else:-->
# <!--            return f"50 cells.py: view_cell: history"-->
@app.route('/do_inv_item', methods=["GET", "POST"])
def do_inv_item():
    if request.method == "POST":
        #b = request.form.get('btnDoInvItem')
        new_count = request.form.get('new_count')
        id_id = request.form.get('id_id')
        ret = maxx_db.viking.update_count(id_id,  new_count)
        if ret:
            return "update_count()  succeeded"
         #   return render_template("cells/list_cells.html", cells=cells)
        else:
            return "update_count()  failed"
   # item = maxx_db.items.get_item(id)  # item: ((12, 'Emerald 116', '3728196523', 'PR344MN77'),)
   #      transfers = maxx_db.items.get_item_transfers(id)
   #          #        return f"do_item() transfers: {transfers}"
   #      return render_template('items/find_inv_item.html', transfers=transfers, item=item)
    return "57 do_inv_item() GET"



@app.route('/inv_test', methods=["GET","POST"])
def inv_test():
    document = open('static/vk_needles.dat', 'r')
    inv_data = maxx_db.viking.get_inv_data()
    #  id_id,sku, sku_1,sku_2,sku_3,descr, on_hand
    #return render_template('viking/all_inv.html', inv_data=inv_data)
    list_of_strings = []
    for n in document:
        n = n.rstrip('\n')
        list_of_strings.append(n)

    params = []
    for item in list_of_strings:
        p=item.split('Z')
        params.append(p)
    document.close()
    return params[:10]
    if request.method == "POST":
            #return f"29 params: {params}"
            if maxx_db.viking.record_inv_items(params):
                inv_data = maxx_db.viking.get_inv()
                return render_template('viking/all_inv.html',  inv_data=inv_data)

        #     return "DONE"
            else:
                return "NOT YET"


    return render_template('viking/inv_test.html', params=params)


@app.route('/get_feet', methods=["GET","POST"])
def get_feet():
    if request.method == "POST":
        rf = dict(request.form.items())
        ret = maxx_db.items.insert_item(rf)
        if ret:
            items = maxx_db.items.get_items()
            return render_template("items/list_items.html", items=items)
        else:
            return "Item INSERT failed"
    rows = [ 'r0','r1','r2','r3','r4','r5','r6','r7','r8','r9','r10','r11','r12','r13','r14','r15','r16','r17']
    cols = [ 'c0','c1','c2','c3','c4','c5','c6','c7','c8','c9','c10','c11','c12','c13','c14','c15','c16','c17']

    return render_template("viking/feet.html", rows=rows, cols=cols)


@app.route('/save_inv_item', methods=['GET','POST'])
def save_inv_item():
    if request.method == 'POST':
#---------- begin "hah function" -----------------

        rf = dict(request.form.items())
        ret = maxx_db.users.register_user(rf,str_hx_pw)
        if ret:
              # items = maxx_db.items.get_items()
                # return render_template("items/list_items.html", items=items)
            return "User registered"
        else:
            return "User INSERT failed"
    #    return render_template("users/login.html")
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
       # return render_template("users/register.html", username=username, pw=str_hx_pw)
    return render_template('users/register.html')