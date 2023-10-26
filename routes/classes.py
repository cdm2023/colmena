from flask import render_template, request
from __main__ import app
import maxx_db
from maxx_db import MaxxConn

@app.route('/add_class', methods=["GET","POST"])
def add_class():
    #return "RETURN add_class() "
    if request.method=="POST":

        rf = dict(request.form.items())
        ret = maxx_db.classes.insert_class(rf)
        if ret:
            classes = maxx_db.classes.get_classes()
            return render_template("classes/confirm_class.html", classes=classes)
        else:
            return "Schedule failed"

    users= maxx_db.users.get_users()
    return render_template("classes/add_class.html", users=users)


@app.route('/list_classes', methods=['GET'])
def list_classes():
    ret = maxx_db.classes.get_classes()
    if ret:
        classes = maxx_db.classes.get_classes()
        return render_template("classes/list_classes.html", classes=classes)

    else:
        return "list_classes() failed"

    return '33 list_classes(): no request object!'