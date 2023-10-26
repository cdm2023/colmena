from __main__ import app

@app.route('/route_test', methods=['GET'])
def route_test():
    return 'it works!'

@app.route('/colmena_1', methods=['GET'])
def colmena_1():
    return """<div style='color:#9C162D'><h3>colmena_1()</h3><h5>#9C162D</h5></div>"""

def colmena_2(n):
    return  str(25*int(n))
    #"<div style='color:#9C162D'><h3>colmena_2()</h3><h5>" + str(n) +"</h5></div>"

@app.route('/mysql2')
def mysql2_():
    return "colmena.py mysql2_"
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM cells')
        data=cur.fetchall()
       # data = g.cursor.fetchall()
        #g.cursor.close()
        return str(data)
    except Exception as error:
        return f"No joy: {error}"