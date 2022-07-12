from flask import (
    abort,
    Flask,
    g,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from functions import *

app = Flask(__name__)
app.secret_key = 'my_secretkey_for_test'

class User:
    #class for user session

    def __init__(self, id, username):
        self.id = id
        self.username = username
    
    def __str__(self):
        return self.username

@app.before_request
def before_request():
    #function to check the user session if exists

    if 'user_id' in session:
        user = session['user_id']
        g.user = user
    else:
        g.user = None

@app.route('/', methods=['GET','POST'])
def login():
    #function log in with methods GET and POST

    if request.method == 'GET':
        if g.user:
            return redirect(url_for('index'))

        return render_template('login.html')
    
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        sql = '''
        SELECT * FROM users
        WHERE username='%s'
        AND password='%s'
        ''' %(username,password)
        
        conn = db_connection()
        auth = conn.execute(sql).fetchall()
        conn.close()

        if auth == []:
            message = 'Invalid username or password !'
            return render_template('login.html', message=message)

        user = User(id=auth[0][0], username=auth[0][1])
        session['user_id'] = user.id
        
        return redirect(url_for('index'))

@app.route('/logout', methods=['GET'])
def logout():
    #log out function

    if not g.user:
        abort(403)

    session.pop('user_id', None)

    return redirect(url_for('login'))

@app.route('/index', methods=['GET'])
def index():
    #index page

    if not g.user:
        abort(403)
    
    return render_template('index.html')

@app.route('/patients', methods=['GET'])
def get_patients():
    #GET request for patient information

    if not g.user:
        abort(403)

    filter = request.args.get('filter', default = '*', type = str).upper()

    conn = db_connection()
    patients = conn.execute('SELECT * FROM patients').fetchall()
    conn.close()

    for p in range(len(patients)):
        patients[p] = list(patients[p])
        patients[p][3] = patients[p][3].replace(' 00:00:00.000000','')

    patients = function_filter(patients,filter)

    if patients == []:
        return jsonify({'message': 'No results for filter = %s' %filter})

    return jsonify(patients)

@app.route('/pharmacies', methods=['GET'])
def get_pharmacies():
    #GET request for pharmacy information

    if not g.user:
        abort(403)

    filter = request.args.get('filter', default = '*', type = str).upper()

    conn = db_connection()
    pharmacies = conn.execute('SELECT * FROM pharmacies').fetchall()
    conn.close()

    pharmacies = function_filter(pharmacies,filter)

    if pharmacies == []:
        return jsonify({'message': 'No results for filter = %s' %filter})
    
    return jsonify(pharmacies)

@app.route('/transactions', methods=['GET'])
def get_transactions():
    #GET request for transaction information

    if not g.user:
        abort(403)

    filter = request.args.get('filter', default = '*', type = str).upper()

    sql = '''
    SELECT p.*,ph.*,t.uuid,t.amount,t.timestamp
    FROM patients AS p
    INNER JOIN transactions AS t
    ON t.patient_uuid==p.uuid
    INNER JOIN pharmacies AS ph
    ON t.pharmacy_uuid=ph.uuid    
    '''

    conn = db_connection()
    transactions = conn.execute(sql).fetchall()
    conn.close()

    for t in range(len(transactions)):
        transactions[t] = list(transactions[t])
        transactions[t][3] = transactions[t][3].replace(' 00:00:00.000000','')
        transactions[t][-1] = transactions[t][-1].replace('.000000','')

    transactions = function_filter(transactions,filter)

    if transactions == []:
        return jsonify({'message': 'No results for filter = %s' %filter})
    
    return jsonify(transactions)

if __name__ == '__main__':
    app.run()
