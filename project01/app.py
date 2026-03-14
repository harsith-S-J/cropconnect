import os
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        location = request.form['location']
        contact = request.form['contact']
        
        if not username or not password or not location or not contact:
            flash('All fields are required!', 'danger')
        else:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            if user:
                flash('Username already exists. Please choose another one.', 'danger')
                conn.close()
            else:
                hashed_password = generate_password_hash(password)
                conn.execute('INSERT INTO users (username, password, location, contact) VALUES (?, ?, ?, ?)',
                             (username, hashed_password, location, contact))
                conn.commit()
                conn.close()
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login'))
                
    return render_template('login.html', action='register')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user is None or not check_password_hash(user['password'], password):
            flash('Invalid username or password.', 'danger')
        else:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['location'] = user['location']
            return redirect(url_for('dashboard'))
            
    return render_template('login.html', action='login')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    # Fetch all crops globally, joined with user info
    crops = conn.execute('''
        SELECT crops.id, crops.crop_name, crops.planted_date, crops.area_size, crops.protection_strategy, crops.status, crops.quantity_info, crops.created_at,
               users.username, users.location, users.contact, users.id as user_id
        FROM crops
        JOIN users ON crops.user_id = users.id
        ORDER BY crops.created_at DESC
    ''').fetchall()
    conn.close()
    
    return render_template('dashboard.html', crops=crops, current_user_id=session['user_id'])

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    # Fetch purely this farmer's personal 'diary' crops
    my_crops = conn.execute('''
        SELECT * FROM crops
        WHERE user_id = ?
        ORDER BY created_at DESC
    ''', (session['user_id'],)).fetchall()
    conn.close()
    
    return render_template('profile.html', crops=my_crops)

@app.route('/add_crop', methods=('POST',))
def add_crop():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    crop_name = request.form['crop_name']
    planted_date = request.form['planted_date']
    area_size = request.form['area_size']
    protection_strategy = request.form['protection_strategy']
    status = request.form['status']
    quantity_info = request.form['quantity_info']
    
    if not crop_name or not status:
        flash('Crop Name and Status are required!', 'danger')
    else:
        conn = get_db_connection()
        conn.execute('INSERT INTO crops (user_id, crop_name, planted_date, area_size, protection_strategy, status, quantity_info) VALUES (?, ?, ?, ?, ?, ?, ?)',
                     (session['user_id'], crop_name, planted_date, area_size, protection_strategy, status, quantity_info))
        conn.commit()
        conn.close()
        flash('Crop added to your diary successfully.', 'success')
        
    return redirect(url_for('profile'))

@app.route('/delete_crop/<int:id>', methods=('POST',))
def delete_crop(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    crop = conn.execute('SELECT * FROM crops WHERE id = ?', (id,)).fetchone()
    
    if crop is None:
        flash('Crop not found.', 'danger')
    elif crop['user_id'] != session['user_id']:
        flash('You are not authorized to delete this entry.', 'danger')
    else:
        conn.execute('DELETE FROM crops WHERE id = ?', (id,))
        conn.commit()
        flash('Crop diary entry deleted.', 'info')
        
    conn.close()
    return redirect(url_for('profile'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
