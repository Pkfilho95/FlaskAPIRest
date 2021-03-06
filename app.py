from flask import Flask, jsonify, make_response, request
from functions import *
from functools import wraps
import datetime
import jwt

app = Flask(__name__)
app.secret_key = 'mysecretkey'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing !'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], 'HS256')
        except:
            return jsonify({'message': 'Token is invalid !'}), 401

        return f(*args, **kwargs)
    
    return decorated

@app.route('/')
def login():
    #auth user with JWT

    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could verify !', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    
    conn = db_connection()
    user = conn.execute('SELECT * FROM users WHERE username="%s" and password="%s"' %(auth.username, auth.password)).fetchall()
    conn.close()
    
    if user != []:
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token})

    return make_response('Could verify !', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

@app.route('/patients', methods=['GET'])
@token_required
def get_patients():
    #GET request for patient information

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
@token_required
def get_pharmacies():
    #GET request for pharmacy information

    filter = request.args.get('filter', default = '*', type = str).upper()

    conn = db_connection()
    pharmacies = conn.execute('SELECT * FROM pharmacies').fetchall()
    conn.close()

    pharmacies = function_filter(pharmacies,filter)

    if pharmacies == []:
        return jsonify({'message': 'No results for filter = %s' %filter})
    
    return jsonify(pharmacies)

@app.route('/transactions', methods=['GET'])
@token_required
def get_transactions():
    #GET request for transaction information

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
