import sqlite3
from flask import (
    abort,
    Flask,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for
)

app = Flask(__name__)
app.secret_key = 'my_secretkey_for_test'

class User:
    #class for user session

    def __init__(self, id, username):
        self.id = id
        self.username = username
    
    def __str__(self):
        return self.username

def db_connection():
    #function to open a database connection

    conn = sqlite3.connect('backend_test.db')
    cursor = conn.cursor()

    return cursor

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

    conn = db_connection()
    patients = conn.execute('SELECT * FROM patients').fetchall()
    conn.close()

    return jsonify(patients)

@app.route('/pharmacies', methods=['GET'])
def get_pharmacies():
    #GET request for pharmacy information

    if not g.user:
        abort(403)

    conn = db_connection()
    pharmacies = conn.execute('SELECT * FROM pharmacies').fetchall()
    conn.close()
    
    return jsonify(pharmacies)

@app.route('/transactions', methods=['GET'])
def get_transactions():
    #GET request for transaction information

    if not g.user:
        abort(403)

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
    
    return jsonify(transactions)

if __name__ == '__main__':
    app.run()
