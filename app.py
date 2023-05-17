import sqlite3
from flask import Flask, render_template, request, redirect, g

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# SQLite connection per thread
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('your_database.db')
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    if 'db' in g:
        g.db.close()

# Routes and views
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        name = request.form['name']
        appointment_date = request.form['appointment_date']
        appointment_time = request.form['appointment_time']
        appointment_type = request.form['appointment_type']
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO reservations (name, appointment_date, appointment_time, appointment_type) VALUES (?, ?, ?, ?)", (name, appointment_date, appointment_time, appointment_type))
        db.commit()
        
        return redirect('/confirmation')
    
    return render_template('reservation.html')

@app.route('/confirmation')
def confirmation():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM reservations ORDER BY id DESC LIMIT 1")
    reservation = cursor.fetchone()
    return render_template('confirmation.html', reservation=reservation)

@app.route('/reservation_list')
def reservation_list():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM reservations")
    reservations = cursor.fetchall()
    return render_template('reservation_list.html', reservations=reservations)

if __name__ == '__main__':
    app.run(debug=True)
