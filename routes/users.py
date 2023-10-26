from flask import render_template, request, session
from __main__ import app
import maxx_db
from maxx_db import MaxxConn

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        s = request.form.get('password')
        s2 =  hex_code(s)
        u = request.form.get('username')
        db_pw = maxx_db.users.get_user_pw(u)
        if db_pw[0][0] == s2:
            user_DB_id = maxx_db.users.get_user_id(u)
            user_id = user_DB_id[0][0]
                        # return f" {user_id}"  #   ((user_id[0][0],),)

            user_data = maxx_db.users.get_user_data(u)
                       # return f"user_data: {user_data}"
                     # user_data: ((7, 'malandrino', 'Malik', 'Dniro', 15),)
      #      u.user_id, u.username, u.first_name, u.last_name, u.perms, v.vk_id, v.store_name
            session['first_name'] = user_data[0][2]
            session['last_name'] = user_data[0][3]
            session['user_id'] = user_id
            session['username'] = u

            session['store_name'] = user_data[0][6]
            session['store_id'] =  user_data[0][5]

            # return f"routes/users/login() username: {session['username']}"
            return render_template("index.html")  # , user_id=user_id , username=u
                      # return f"password match: {s2}"

        else:
            return f"Nope: db_pw:{db_pw[0][0]}  s2: {s2}"

        return f"hex_code(password) {s2}"
        #----------------- KEEP  ---------
                                  # rf = dict(request.form.items())
                      #  return f"users.login: {rf}"
    return render_template("users/login.html")

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
    #---------- begin "hah function" -----------------
        p1 = request.form.get('password')
        pw_tot = 0
        enum_pw = enumerate(p1,1)
        for i, char in enum_pw:
            pw_tot += i ** ((ord(char) % 10) + 1)
        hx_pw = hex(pw_tot)
        str_hx_pw = str(hx_pw)[2:]
#--------------  end "hash function" ------------------
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


@app.route('/user_route', methods=['GET'])
def user_route():
    return 'user_route() works!'


@app.route('/list_users', methods=['GET'])
def list_users():
    ret = maxx_db.users.get_users()
    if ret:
        users = maxx_db.users.get_users()
        return render_template("users/list_users.html", users=users)
        #return "User registered"
    else:
        return "list_users() failed"

    return '55 list_users(): no request object!'


@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username')
        session.pop('user_id')
        session.pop('first_name')
        session.pop('last_name')
        session.pop('store_name')
        session.pop('store_id')

    return render_template('index.html')


from maxx_funcs import hex_code

