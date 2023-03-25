from flask import Flask, render_template, request, redirect, url_for, session
#from flask_session import Session

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'supersecretkey'
#ession(app)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        session['loan_amount'] = 0
        session['max_loan_amount'] = 1000
        session['pending_loan_requests'] = []
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'], loan_amount=session['loan_amount'], max_loan_amount=session['max_loan_amount'], pending_loan_requests=session['pending_loan_requests'])


@app.route('/request_loan', methods=['GET', 'POST'])
def request_loan():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        loan_amount = int(request.form['loan_amount'])
        if loan_amount > session['max_loan_amount']:
            return render_template('error.html', error='Loan amount exceeds maximum allowed amount.')
        session['pending_loan_requests'].append((session['username'], loan_amount))
        return redirect(url_for('dashboard'))
    return render_template('request_loan.html', max_loan_amount=session['max_loan_amount'])

@app.route('/approve_loan/<int:loan_id>', methods=['GET', 'POST'])
def approve_loan(loan_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        vote = request.form['vote']
        if vote == 'approve':
            loan_amount = session['pending_loan_requests'][loan_id][1]
            session['loan_amount'] += loan_amount
            session['pending_loan_requests'].pop(loan_id)
            return redirect(url_for('dashboard'))
        else:
            session['pending_loan_requests'].pop(loan_id)
            return redirect(url_for('dashboard'))
    loan_request = session['pending_loan_requests'][loan_id]
    return render_template('approve_loan.html', loan_request=loan_request)
