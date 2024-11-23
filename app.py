from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import mysql.connector
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '2005',
    'database': 'intern'
}

# Connect to MySQL
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# Create Account Page
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('login'))
    return render_template('create_account.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            session['user'] = email
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

# Forgot Password Page
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        otp = send_otp(email)  # Generate and send OTP

        if otp:
            session['email'] = email  # Store email in session
            session['otp'] = otp  # Store OTP in session
            return redirect(url_for('verify_otp'))  # Redirect to OTP verification page
        else:
            flash('Error sending OTP. Please try again.', 'danger')
            return redirect(url_for('forgot_password'))
    return render_template('forgot_password.html')

# Send OTP Function
def send_otp(email):
    otp = str(random.randint(100000, 999999))  # Generate a 6-digit OTP

    sender_email = "praneshpk2005@gmail.com"
    sender_password = "ccng olgn kisi ygkc"  # Use an app password
    receiver_email = email
    subject = "OTP for Password Reset"
    body = f"Your OTP is {otp}."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print(f"OTP sent successfully to {email}")
        return otp
    except Exception as e:
        print(f"Error sending OTP: {e}")
        return None

# Verify OTP Page
@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        entered_otp = request.form['otp']
        stored_otp = session.get('otp')  # Retrieve OTP from session

        if entered_otp == stored_otp:  # Validate OTP
            return redirect(url_for('reset_password'))  # Redirect to reset password page
        else:
            flash('Invalid OTP. Please try again.', 'danger')
    return render_template('verify_otp.html')

# Reset Password Page
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        new_password = request.form['new_password']
        email = session.get('email')  # Retrieve email from session

        if not email:
            flash('Session expired. Please try again.', 'danger')
            return redirect(url_for('forgot_password'))

        # Update the password in the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password = %s WHERE email = %s", (new_password, email))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Password reset successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html')

# Dashboard Page
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Inventory Page
@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Handle search query from the search bar
    search_query = request.args.get('search', '').strip()
    
    if search_query:
        # Search by name or code
        cursor.execute("""
            SELECT * FROM products
            WHERE name LIKE %s OR code LIKE %s
        """, (f"%{search_query}%", f"%{search_query}%"))
    else:
        # Fetch all products if no search query
        cursor.execute("SELECT * FROM products")
    
    products = cursor.fetchall()
    
    # Handle updates if the request is POST
    if request.method == 'POST':
        product_id = request.form.get('id')
        name = request.form.get('name')
        code = request.form.get('code')
        description = request.form.get('description')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        image_url = request.form.get('image_url')
        
        # Update the product in the database
        cursor.execute("""
            UPDATE products
            SET name = %s, code = %s, description = %s, price = %s, quantity = %s, image_url = %s
            WHERE id = %s
        """, (name, code, description, price, quantity, image_url, product_id))
        conn.commit()
        return redirect(url_for('inventory'))
    
    cursor.close()
    conn.close()
    return render_template('inventory.html', products=products)


# ADD or Delete Product Page
@app.route('/add_delete_product', methods=['GET', 'POST'])
def add_delete_product():
    if request.method == 'POST':
        action = request.form['action']  # Action to perform (add, delete, reduce_quantity)
        product_code = request.form['code']  # Product code to identify the product
        product_name = request.form['name']  # Product name for adding
        product_description = request.form['description']  # Product description for adding
        product_price = request.form['price']  # Product price for adding
        product_quantity = request.form['quantity']  # Quantity for add or reduce

        conn = get_db_connection()
        cursor = conn.cursor()

        if action == 'add':
            cursor.execute(''' 
                INSERT INTO products (name, code, description, price, quantity, image_url)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (product_name, product_code, product_description, product_price, product_quantity, 'default_image_url'))  # Add default image URL if necessary

        elif action == 'delete':
            product_code = request.form.get('product_code')  # Only accessing product_code for deletion
            delete_action = request.form.get('action')  # Can be 'delete' or 'reduce_quantity'

            if delete_action == 'delete':
            # Handle product deletion by product_code
                pass
            elif delete_action == 'reduce_quantity':
                quantity_to_reduce = request.form.get('quantity')  # Quantity to reduce
            # Handle reducing product quantity by product_code
                pass

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('add_delete_product'))  # Redirect to the same page after the operation

    return render_template('add_delete_product.html') 


if __name__ == '__main__':
    app.run(debug=True)
