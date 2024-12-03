from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, make_response
import mysql.connector
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from werkzeug.utils import secure_filename
import os 

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
            return redirect(url_for('main'))
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
@app.route('/main')
def main():
    return render_template('main.html')

# Inventory Page
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Allowed extensions


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    UPLOAD_FOLDER = 'static/images'
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # Define your upload folder
    items_per_page = 55
    page = request.args.get('page', 1, type=int)
    
    if request.method == 'POST':
        action = request.form['action']
        product_id = request.form['id']

        conn = get_db_connection()
        cursor = conn.cursor()
        # Pagination settings
        

        # Initialize image_url variable (default to None)
        image_url = None

        # Handle image upload
        if 'image' in request.files:
            image = request.files['image']
            if image and image.filename != '':
                # Fetch the current image_url from the database
                cursor.execute("SELECT image_url FROM products WHERE id = %s", (product_id,))
                current_image_url = cursor.fetchone()[0]  # Fetch the existing image_url
                
                # If an old image exists, delete it
                if current_image_url:
                    old_image_path = current_image_url.lstrip('/')  # Remove leading '/' for the correct path
                    if os.path.exists(old_image_path):
                        try:
                            os.remove(old_image_path)
                            print(f"Deleted old image: {old_image_path}")
                        except Exception as e:
                            print(f"Error deleting old image: {e}")

                # Save the new image
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                print(f"Saving image to: {image_path}")  # Debug: Check the path where the image is saved
                image.save(image_path)
                image_url = f"/{UPLOAD_FOLDER}/{filename}"
                print(f"Image URL: {image_url}")  # Debug: Check the image URL being stored

        # Modify product details in the database
        if action == 'modify':
            name = request.form['name']
            code = request.form['code']
            price = request.form['price']
            quantity = request.form['quantity']
            description = request.form['description']
            category_id = request.form['category_id']
            
            cursor.execute("SELECT price FROM products WHERE id = %s", (product_id,))
            current_price = cursor.fetchone()[0]  

            if image_url:  # Update image_url only if a new image was uploaded
                cursor.execute('''
                    UPDATE products
                    SET name = %s, code = %s, price = %s, quantity = %s, description = %s, category_id = %s, image_url = %s, last_updated = NOW()
                    WHERE id = %s
                ''', (name, code, price, quantity, description, category_id, image_url, product_id))
            else:  # If no image uploaded, only update other fields
                cursor.execute('''
                    UPDATE products
                    SET name = %s, code = %s, price = %s, quantity = %s, description = %s, category_id = %s, last_updated = NOW()
                    WHERE id = %s
                ''', (name, code, price, quantity, description, category_id, product_id))

            if float(price) != current_price:
                cursor.execute('''
                    INSERT INTO price_history (product_code, price, time)
                    VALUES (%s, %s, CURDATE())
                ''', (code, price))


        elif action == 'delete':
            cursor.execute('DELETE FROM products WHERE id = %s', (product_id,))

        conn.commit()  # Commit the changes to the database
        cursor.close()
        conn.close()

        return redirect(url_for('inventory'))

    # GET request - Fetch categories and products
    selected_category = request.args.get('category', '').strip()
    search_query = request.args.get('search', '').strip().lower()

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch categories for the dropdown
    cursor.execute("SELECT id, name FROM categories")
    categories = [{'id': row[0], 'name': row[1]} for row in cursor.fetchall()]

    # Fetch products based on selected category and search query
    query = '''
        SELECT p.id, p.name, p.code, p.description, p.price, p.quantity, p.image_url, c.name AS category_name, p.category_id
        FROM products p
        JOIN categories c ON p.category_id = c.id
    '''
    params = []

    if selected_category:
        query += " WHERE p.category_id = %s"
        params.append(selected_category)

    if search_query:
        if selected_category:
            query += " AND (LOWER(p.name) LIKE %s OR LOWER(p.code) LIKE %s)"
        else:
            query += " WHERE LOWER(p.name) LIKE %s OR LOWER(p.code) LIKE %s"
        params.extend([f"%{search_query}%", f"%{search_query}%"])
    
    # Add pagination
    query += " LIMIT %s OFFSET %s"
    params.extend([items_per_page, (page - 1) * items_per_page])

    cursor.execute(query, params)
    products = cursor.fetchall()

    # Fetch the total number of products for pagination
    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]
    total_pages = (total_products + items_per_page - 1) // items_per_page  # Calculate total pages

    cursor.close()
    conn.close()
    product_list = [{
        'id': product[0],
        'name': product[1],
        'code': product[2],
        'description': product[3],
        'price': product[4],
        'quantity': product[5],
        'image_url': product[6],
        'category_name': product[7],
        'category_id': product[8]
    } for product in products]

    return render_template('inventory.html', products=product_list, categories=categories, page=page, total_pages=total_pages)



import time
# ADD or Delete Product Page
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    app.logger.debug(f"Request method: {request.method}")
    UPLOAD_FOLDER = 'static/images'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure folder exists

    if request.method == 'POST':
        # Retrieve form details
        product_name = request.form['name']
        product_code = request.form['code']
        product_description = request.form['description']
        product_price = request.form['price']
        product_quantity = request.form['quantity']
        category_id = request.form['category_id']
        
        # Handle image upload
        image_file = request.files['image']
        if image_file and image_file.filename != '':
            secure_name = secure_filename(image_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_name)
            image_file.save(file_path)
        else:
            flash('Image upload failed.', 'danger')
            return redirect(url_for('add_product'))
        
        # Save product details to database
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Fetch category name
            cursor.execute("SELECT name FROM categories WHERE id = %s", (category_id,))
            category_name = cursor.fetchone()
            category_name = category_name[0] if category_name else "Unknown"

            # Insert product details
            cursor.execute('''
                INSERT INTO products (name, code, description, price, quantity, image_url, category_id, category_name)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (product_name, product_code, product_description, product_price, product_quantity, 
                  f'/static/images/{secure_name}', category_id, category_name))

            conn.commit()  # Commit transaction

            cursor.execute('''
                INSERT INTO price_history (product_code, price, time)
                VALUES (%s, %s, CURDATE())
            ''', (product_code, product_price))

            conn.commit()

        except Exception as e:
            app.logger.error(f"Error: {e}")
            conn.rollback()  # Rollback on error
            flash('Error while adding product.', 'danger')
        finally:
            cursor.close()
            conn.close()
        time.sleep(3)
        return redirect(url_for('add_product'))

    # Fetch categories for dropdown
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM categories")
        categories = cursor.fetchall()
    except Exception as e:
        app.logger.error(f"Error fetching categories: {e}")
        categories = []
    finally:
        cursor.close()
        conn.close()

    return render_template('add_product.html', categories=categories)



@app.route('/ordering', methods=['GET', 'POST'])
def ordering():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Pagination settings
    items_per_page = 50
    page = request.args.get('page', 1, type=int)

    # Fetch all products with pagination
    cursor.execute('SELECT COUNT(*) FROM products')
    total_products = cursor.fetchone()[0]
    total_pages = (total_products + items_per_page - 1) // items_per_page  # Calculate total pages

    offset = (page - 1) * items_per_page

    # Fetch products with their primary image and additional images
    cursor.execute('''
        SELECT p.id, p.name, p.code, p.price, p.description, p.category_name, p.image_url, pi.image_url AS additional_image
        FROM products p
        LEFT JOIN product_image pi ON p.code = pi.code
        LIMIT %s OFFSET %s
    ''', (items_per_page, offset))

    products = cursor.fetchall()

    # Fetch distinct categories
    cursor.execute('SELECT name FROM categories')
    categories = cursor.fetchall()

    cursor.close()
    conn.close()

    # Organize products by ID to group images
    product_dict = {}
    for product in products:
        product_id = product[0]
        if product_id not in product_dict:
            product_dict[product_id] = {
                'id': product[0],
                'name': product[1],
                'code': product[2],
                'price': product[3],
                'description': product[4],
                'category_name': product[5],
                'primary_image': product[6],
                'additional_images': []
            }
        # Append additional image URL if it exists
        if product[7]:
            product_dict[product_id]['additional_images'].append(product[7])

    # Convert back to a list
    products = list(product_dict.values())

    return render_template('ordering.html', products=products, categories=categories, page=page, total_pages=total_pages)




@app.route('/place_order', methods=['POST'])
def place_order():
    # Data from the ordering page
    selected_products = request.form.getlist('product_id')
    quantities = request.form.getlist('quantity')
    
    conn = get_db_connection()
    cursor = conn.cursor()

    selected_product_details = []
    total_cost = 0

    for product_id, quantity in zip(selected_products, quantities):
        if int(quantity) > 0:
            cursor.execute('SELECT id, name, code, price FROM products WHERE id = %s', (product_id,))
            product = cursor.fetchone()
            if product:
                product_id, product_name, product_code, product_price = product
                
                # Ensure product_price is float
                product_price = float(product_price)
                
                # Convert quantity to an integer
                quantity = int(quantity)  # This ensures quantity is an integer
                
                cost = quantity * product_price  # Now this should work without errors
                total_cost += cost
                selected_product_details.append({
                    'id': product_id,
                    'name': product_name,
                    'code': product_code,
                    'price': product_price,
                    'quantity': quantity,
                    'cost': cost
                })



    cursor.close()
    conn.close()
    return render_template('place_order.html', products=selected_product_details, total_cost=total_cost)


@app.route('/confirm_order', methods=['POST'])
def confirm_order():
    # Fetch form data
    customer_name = request.form['customer_name']
    customer_address = request.form['customer_address']
    payment_mode = request.form['payment_mode']
    country = request.form['country']  # New Field
    age_range = request.form['age_range']  # New Field
    gender = request.form['gender'] 
    selected_products = request.form.getlist('product_id[]')
    quantities = request.form.getlist('quantity[]')
    
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        if not selected_products or not quantities:
            flash("No products selected.")
            return redirect(url_for('order_page'))

        total_price = 0  # Initialize total price for the order

        for product_id, quantity in zip(selected_products, quantities):
            # Ensure valid inputs
            if not product_id or not quantity or int(quantity) <= 0:
                flash("Invalid product or quantity.")
                continue

            # Fetch product details
            cursor.execute('SELECT price, name, code, quantity FROM products WHERE id = %s', (product_id,))
            product = cursor.fetchone()

            if product:
                price, name, code, available_quantity = product

                # Check stock availability
                if int(quantity) > available_quantity:
                    flash(f"Not enough stock for {name}. Available: {available_quantity}.")
                    continue

                cost = float(price) * int(quantity)  # Calculate cost for this product
                total_price += cost  # Add to total price

                # Insert into orders table
                cursor.execute('''
                    INSERT INTO orders (product_id, product_name, product_code, quantity, cost, customer_name,
                                        customer_address, payment_mode, country, age_range, gender, order_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                ''', (product_id, name, code, quantity, cost, customer_name, customer_address, payment_mode, country, age_range,gender))

                # Update product quantity and last_sold_date
                cursor.execute('''
                    UPDATE products 
                    SET quantity = quantity - %s, last_sold_date = NOW() 
                    WHERE id = %s
                ''', (quantity, product_id))

                # Insert into sales table
                cursor.execute('''
                    INSERT INTO sales (product_id, product_name, product_code, quantity, payment_mode, total_price, order_date)
                    VALUES (%s, %s, %s, %s, %s, %s, NOW())
                ''', (product_id, name, code, quantity, payment_mode, cost))

        # Commit changes
        conn.commit()
        print("Database changes committed.")  # Debugging

        # Flash success message and redirect
        flash("Order has been placed successfully!")
        return redirect(url_for('ordering'))

    except Exception as e:
        conn.rollback()  # Rollback changes on error
        print(f"Error: {e}")  # Log error
        flash(f"An error occurred: {e}")
        return redirect(url_for('ordering'))

    finally:
        cursor.close()
        conn.close()



@app.route('/order_management', methods=['GET'])
def order_management():
    page = int(request.args.get('page', 1))  # Get the page number from query params, default to 1
    per_page = 10  # Number of orders per page
    offset = (page - 1) * per_page  # Calculate the offset

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the total number of orders for pagination info
    cursor.execute('SELECT COUNT(*) FROM orders')
    total_orders = cursor.fetchone()[0]

    # Fetch orders for the current page
    cursor.execute('''
        SELECT 
            orders.id, product_name, product_code, quantity, cost, customer_name, 
            customer_address, payment_mode, country, order_date 
        FROM orders 
        ORDER BY order_date DESC
        LIMIT %s OFFSET %s
    ''', (per_page, offset))
    orders = cursor.fetchall()

    cursor.close()
    conn.close()

    # Calculate total pages
    total_pages = (total_orders + per_page - 1) // per_page

    return render_template('order_management.html', orders=orders, page=page, total_pages=total_pages)


@app.route('/report')
def report():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        print("Starting to generate the report.")

        # Existing Queries
        print("Querying product price changes...")
        cursor.execute('''
            SELECT 
                ph1.name,
                ph1.price AS current_price,
                ph2.price AS previous_price,
                ph1.time AS last_updated
            FROM 
                price_history ph1
            JOIN 
                price_history ph2 ON ph1.product_code = ph2.product_code 
                                AND ph1.time > ph2.time
            WHERE 
                ph1.time = (
                    SELECT MAX(time) 
                    FROM price_history 
                    WHERE product_code = ph1.product_code
                )
                AND ph2.time = (
                    SELECT MAX(time) 
                    FROM price_history 
                    WHERE product_code = ph1.product_code 
                    AND time < ph1.time
                )
            ORDER BY 
                ph1.product_code;
            ''')
        price_changes = cursor.fetchall()

        print("Querying products at minimum quantity...")
        cursor.execute('''
            SELECT name, quantity
            FROM products
            WHERE quantity <= min_quantity;
        ''')
        min_quantity_alerts = cursor.fetchall()

        print("Querying unsold products...")
        cursor.execute('''
            SELECT p.id, p.name, p.code
            FROM products p
            LEFT JOIN sales s ON p.id = s.product_id
            WHERE s.product_id IS NULL;
        ''')
        unsold_products = cursor.fetchall()

        print("Querying most sold product categories...")
        cursor.execute('''
            SELECT c.name AS category_name, SUM(s.quantity) AS total_quantity
            FROM sales s
            JOIN products p ON s.product_id = p.id
            JOIN categories c ON p.category_id = c.id
            GROUP BY c.id, c.name
            ORDER BY total_quantity DESC
            LIMIT 1;
        ''')
        most_sold_category = cursor.fetchone()

        print("Querying restock alerts for most sold products...")
        cursor.execute('''
            SELECT p.name, SUM(s.quantity) AS total_sold, p.quantity
            FROM sales s
            JOIN products p ON s.product_id = p.id
            WHERE MONTH(s.order_date) = MONTH(CURRENT_DATE)
            AND YEAR(s.order_date) = YEAR(CURRENT_DATE)
            GROUP BY p.id, p.name, p.quantity
            HAVING p.quantity < 10
            ORDER BY total_sold DESC;
        ''')
        restock_alerts = cursor.fetchall()

        print("Querying monthly sales growth rate...")
        cursor.execute('''
            SELECT EXTRACT(MONTH FROM order_date) AS month, SUM(total_price) AS total_sales
            FROM sales
            GROUP BY month
            ORDER BY month;
        ''')
        monthly_sales = cursor.fetchall()

        monthly_sales_growth_rate = []
        for i in range(1, len(monthly_sales)):
            previous_month_sales = monthly_sales[i - 1]['total_sales']
            current_month_sales = monthly_sales[i]['total_sales']
            growth_rate = ((current_month_sales - previous_month_sales) / previous_month_sales) * 100 if previous_month_sales > 0 else 0
            monthly_sales_growth_rate.append(round(growth_rate, 2))

        # New Query: Lowest-priced products for the current month
        print("Querying lowest-priced products for the current month...")
        cursor.execute('''
            SELECT p.name, p.price, c.name AS category_name
            FROM products p
            JOIN categories c ON p.category_id = c.id
            ORDER BY p.price ASC
            LIMIT 5;
        ''')
        lowest_priced_products = cursor.fetchall()

        print("Report generation completed successfully.")

        return render_template('report.html',
                               price_changes=price_changes,
                               min_quantity_alerts=min_quantity_alerts,
                               unsold_products=unsold_products,
                               most_sold_category=most_sold_category,
                               restock_alerts=restock_alerts,
                               monthly_sales_growth_rate=monthly_sales_growth_rate,
                               lowest_priced_products=lowest_priced_products)

    except Exception as e:
        print(f"Error in report route: {e}")
        flash("An error occurred while generating the report.")
        return redirect(url_for('dashboard'))

    finally:
        cursor.close()
        conn.close()
        print("Database connection closed.")




SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

def send_email(name, user_email, grievance_type, description):
    """Compose and send the grievance email."""

    SENDER_EMAIL = "praneshpk2005@gmail.com"  # Replace with your email
    SENDER_PASSWORD = "ccng olgn kisi ygkc" 
    RECEIVER_EMAIL = SENDER_EMAIL    #Replace this with the one who will see their grieviances
    


    try:
        # Email content
        subject = f"Grievance Submission: {grievance_type}"
        body = f"""
        Grievance Details:
        
        Name: {name}
        Email: {user_email}
        Grievance Type: {grievance_type}
        Description:
        {description}
        """

        # Set up email message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject
        msg['Reply-To'] = user_email
        msg.attach(MIMEText(body, 'plain'))

        # Connect to SMTP server and send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

        return True
    except Exception as e:
        print(f"Error while sending email: {e}")
        return False


@app.route('/grievance', methods=['GET', 'POST'])
def grievance():
    """Handle both rendering and submission of the grievance form."""
    if request.method == 'POST':
        # Fetch form data
        name = request.form.get('name')
        user_email = request.form.get('email')
        grievance_type = request.form.get('grievance_type')
        description = request.form.get('description')

        # Validate form inputs
        if not all([name, user_email, grievance_type, description]):
            flash('All fields are required. Please fill in the form completely.', 'danger')
            return redirect(url_for('grievance'))

        # Send email
        if send_email(name, user_email, grievance_type, description):
            flash('Your grievance has been submitted successfully!', 'success')
        else:
            flash('An error occurred while submitting your grievance. Please try again.', 'danger')

        return redirect(url_for('grievance'))

    # Render the form for GET requests
    return render_template('grievance.html')


@app.route('/analysis')
def analysis():
    return render_template('analysis.html')


@app.route('/overall_analysis')
def overall_analysis():
    return render_template('overall_analysis.html')


@app.route('/get-stock-distribution')
def get_stock_distribution():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    SELECT categories.name, SUM(products.quantity)
    FROM products
    JOIN categories ON products.category_id = categories.id
    GROUP BY categories.name
    """
    cursor.execute(query)
    data = cursor.fetchall()

    # Adjust for tuple structure
    categories = [row[0] for row in data]  # Access the first element of each tuple (category name)
    values = [int(row[1]) for row in data]  # Access the second element of each tuple (quantity) and cast to int

    return jsonify({
        'categories': categories,
        'values': values
    })


@app.route('/get-sales-trends')
def get_sales_trends():
    period = request.args.get('period', 'daily')  # Default to 'daily'
    conn = get_db_connection()
    cursor = conn.cursor()

    if period == 'monthly':
        query = """
        SELECT DATE_FORMAT(order_date, '%Y-%m') AS date, SUM(total_price)
        FROM sales
        GROUP BY DATE_FORMAT(order_date, '%Y-%m')
        ORDER BY DATE_FORMAT(order_date, '%Y-%m') ASC
        """
    elif period == 'yearly':
        query = """
        SELECT YEAR(order_date) AS date, SUM(total_price)
        FROM sales
        GROUP BY YEAR(order_date)
        ORDER BY YEAR(order_date) ASC
        """
    else:  # Default to daily
        query = """
        SELECT DATE(order_date) AS date, SUM(total_price)
        FROM sales
        GROUP BY DATE(order_date)
        ORDER BY DATE(order_date) ASC
        """

    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()

    dates = [row[0].strftime('%Y-%m-%d') if period == 'daily' else row[0] for row in data]
    sales = [row[1] for row in data]

    return jsonify({'dates': dates, 'sales': sales})


@app.route('/get-payment-methods')
def get_payment_methods():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    SELECT payment_mode, COUNT(*)
    FROM sales
    GROUP BY payment_mode
    """
    cursor.execute(query)
    data = cursor.fetchall()
    print (data)
    cursor.close()

    methods = [row[0] for row in data]
    values = [row[1] for row in data]

    return jsonify({'methods': methods, 'values': values})


@app.route('/get-regional-sales')
def get_regional_sales():
    country = request.args.get('country')  # Get the country from query parameters
    conn = get_db_connection()
    cursor = conn.cursor()

    if country:
        query = """
        SELECT country, SUM(total_price)
        FROM sales
        WHERE country LIKE %s
        GROUP BY country
        """
        cursor.execute(query, (f'%{country}%',))  # Use LIKE for partial matches
    else:
        query = """
        SELECT country, SUM(total_price)
        FROM sales
        GROUP BY country
        """
        cursor.execute(query)

    data = cursor.fetchall()
    cursor.close()

    regions = [row[0] for row in data]
    sales = [row[1] for row in data]

    return jsonify({'regions': regions, 'sales': sales})



@app.route('/get-customer-gender')
def get_customer_gender():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    SELECT 
        SUM(CASE WHEN gender = 'Male' THEN 1 ELSE 0 END) AS male,
        SUM(CASE WHEN gender = 'Female' THEN 1 ELSE 0 END) AS female,
        SUM(CASE WHEN gender = 'Other' THEN 1 ELSE 0 END) AS other
    FROM orders
    """
    cursor.execute(query)
    data = cursor.fetchone()
    cursor.close()

    return jsonify({'male': data[0], 'female': data[1], 'other': data[2]})






@app.route('/specific_product_analysis')
def specific_product_analysis():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, code FROM products")
        products = cursor.fetchall()

        # Convert to a list of dictionaries
        products = [{"name": product[0], "code": product[1]} for product in products]
        return render_template('specific_product_analysis.html', products=products)

    except Exception as e:
        return {"error": "Failed to fetch product data"}, 500

    finally:
        cursor.close()
        conn.close()


@app.route('/get-product-price-time/<code>', methods=['GET'])
def get_price_time_data(code):
    granularity = request.args.get('granularity', 'monthly')  # Default to daily if not specified
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        if granularity == 'daily':
            cursor.execute("""
            SELECT DATE_FORMAT(time, '%Y-%m-%d') AS period, price
            FROM price_history
            WHERE product_code = %s
            ORDER BY time
            """, (code,))
        
        elif granularity == 'yearly':
            cursor.execute("""
            SELECT DATE_FORMAT(time, '%Y') AS period, price
            FROM price_history
            WHERE product_code = %s
            ORDER BY time
            """, (code,))
        
        else:  # Default to monthly
            cursor.execute("""
            SELECT DATE_FORMAT(time, '%Y-%m') AS period, price
            FROM price_history
            WHERE product_code = %s
            ORDER BY time
            """, (code,))
        
        rows = cursor.fetchall()
        
        # Prepare the data for JSON response
        price_time = {
            "labels": [row['period'] for row in rows],
            "values": [float(row['price']) for row in rows]
        }
        return jsonify(price_time)

    except Exception as e:
        return {"error": str(e)}, 500

    finally:
        cursor.close()
        conn.close()



@app.route('/get-product-units-sold/<code>', methods=['GET'])
def get_units_sold_data(code):
    interval = request.args.get('interval', 'monthly')  # Default to monthly if not specified
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        if interval == 'daily':
            cursor.execute("""
            SELECT DATE_FORMAT(order_date, '%Y-%m-%d') AS day, SUM(quantity) AS units_sold
            FROM orders
            WHERE product_code = %s
            GROUP BY day
            ORDER BY day
            """, (code,))
        elif interval == 'yearly':
            cursor.execute("""
            SELECT DATE_FORMAT(order_date, '%Y') AS year, SUM(quantity) AS units_sold
            FROM orders
            WHERE product_code = %s
            GROUP BY year
            ORDER BY year
            """, (code,))
        else:  # Default to monthly
            cursor.execute("""
            SELECT DATE_FORMAT(order_date, '%Y-%m') AS month, SUM(quantity) AS units_sold
            FROM orders
            WHERE product_code = %s
            GROUP BY month
            ORDER BY month
            """, (code,))
        
        rows = cursor.fetchall()
        if not rows:
            return jsonify({"labels": [], "values": []})  # Return empty data if no records found

        units_sold = {
            "labels": [row['day'] if interval == 'daily' else row['month'] if interval == 'monthly' else row['year'] for row in rows],
            "values": [int(row['units_sold']) if row['units_sold'] else 0 for row in rows]
        }
        return jsonify(units_sold)

    except Exception as e:
        return {"error": str(e)}, 500

    finally:
        cursor.close()
        conn.close()

@app.route('/get-product-revenue/<code>', methods=['GET'])
def get_revenue_data(code):
    interval = request.args.get('interval', 'monthly')  # Default to monthly if not specified
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        if interval == 'daily':
            cursor.execute("""
            SELECT DATE_FORMAT(order_date, '%Y-%m-%d') AS day, SUM(total_price) AS revenue
            FROM orders
            WHERE product_code = %s
            GROUP BY day
            ORDER BY day
            """, (code,))
        elif interval == 'yearly':
            cursor.execute("""
            SELECT DATE_FORMAT(order_date, '%Y') AS year, SUM(total_price) AS revenue
            FROM orders
            WHERE product_code = %s
            GROUP BY year
            ORDER BY year
            """, (code,))
        else:  # Default to monthly
            cursor.execute("""
            SELECT DATE_FORMAT(order_date, '%Y-%m') AS month, SUM(total_price) AS revenue
            FROM orders
            WHERE product_code = %s
            GROUP BY month
            ORDER BY month
            """, (code,))
        
        rows = cursor.fetchall()
        revenue = {
            "labels": [row['day'] if interval == 'daily' else row['month'] if interval == 'monthly' else row['year'] for row in rows],
            "values": [float(row['revenue']) if row['revenue'] else 0.0 for row in rows]
        }
        return jsonify(revenue)

    except Exception as e:
        return {"error": str(e)}, 500

    finally:
        cursor.close()
        conn.close()


@app.route('/get-product-country-distribution/<code>', methods=['GET'])
def get_country_distribution(code):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
        SELECT country, COUNT(*) AS count
        FROM orders
        WHERE product_code = %s
        GROUP BY country
        """, (code,))
        
        rows = cursor.fetchall()
        country_distribution = {
            "labels": [row['country'] for row in rows],
            "values": [row['count'] for row in rows]
        }
        return jsonify(country_distribution)

    except Exception as e:
        return {"error": str(e)}, 500

    finally:
        cursor.close()
        conn.close()


@app.route('/get-product-time-of-purchase/<code>', methods=['GET'])
def get_time_purchase_data(code):
    interval = request.args.get('interval', 'monthly')  # Default to monthly if not specified
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        if interval == 'daily':
            cursor.execute("""
            SELECT DATE(order_date) AS date, COUNT(*) AS purchases
            FROM orders
            WHERE product_code = %s
            GROUP BY date
            ORDER BY date
            """, (code,))
            rows = cursor.fetchall()
            time_purchase = {
                "labels": [row['date'] for row in rows],
                "values": [row['purchases'] for row in rows]
            }

        elif interval == 'yearly':
            cursor.execute("""
            SELECT YEAR(order_date) AS year, COUNT(*) AS purchases
            FROM orders
            WHERE product_code = %s
            GROUP BY year
            ORDER BY year
            """, (code,))
            rows = cursor.fetchall()
            time_purchase = {
                "labels": [row['year'] for row in rows],
                "values": [row['purchases'] for row in rows]
            }

        else:  # Default to monthly
            cursor.execute("""
            SELECT DATE_FORMAT(order_date, '%Y-%m') AS month, COUNT(*) AS purchases
            FROM orders
            WHERE product_code = %s
            GROUP BY month
            ORDER BY month
            """, (code,))
            rows = cursor.fetchall()
            time_purchase = {
                "labels": [row['month'] for row in rows],
                "values": [row['purchases'] for row in rows]
            }

        return jsonify(time_purchase)

    except Exception as e:
        return {"error": str(e)}, 500

    finally:
        cursor.close()
        conn.close()

@app.route('/get-product-payment-modes/<code>', methods=['GET'])
def get_payment_modes(code):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
        SELECT payment_mode, COUNT(*) AS count
        FROM orders
        WHERE product_code = %s
        GROUP BY payment_mode
        """, (code,))
        
        rows = cursor.fetchall()
        payment_modes = {
            "labels": [row['payment_mode'] for row in rows],
            "values": [row['count'] for row in rows]
        }
        return jsonify(payment_modes)

    except Exception as e:
        return {"error": str(e)}, 500

    finally:
        cursor.close()
        conn.close()


@app.route('/get-product-age-distribution/<code>', methods=['GET'])
def get_age_distribution(code):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
        SELECT age_range AS age_group, COUNT(*) AS count
        FROM orders
        WHERE product_code = %s
        GROUP BY age_range
        """, (code,))
        
        rows = cursor.fetchall()
        age_distribution = {
            "labels": [row['age_group'] for row in rows],
            "values": [row['count'] for row in rows]
        }
        return jsonify(age_distribution)

    except Exception as e:
        return {"error": str(e)}, 500

    finally:
        cursor.close()
        conn.close()

@app.route('/get-product-gender-distribution/<code>', methods=['GET'])
def get_gender_distribution(code):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
        SELECT gender, COUNT(*) AS count
        FROM orders
        WHERE product_code = %s
        GROUP BY gender
        """, (code,))
        
        rows = cursor.fetchall()
        gender_distribution = {
            "labels": [row['gender'] for row in rows],
            "values": [row['count'] for row in rows]
        }
        return jsonify(gender_distribution)

    except Exception as e:
        return {"error": str(e)}, 500

    finally:
        cursor.close()
        conn.close()


@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Fetch top 5 most sold products
        cursor.execute('''
            SELECT p.id, p.name, p.description, p.image_url, SUM(s.quantity) AS total_sold
            FROM sales s
            JOIN products p ON s.product_id = p.id
            GROUP BY p.id, p.name, p.description, p.image_url
            ORDER BY total_sold DESC
            LIMIT 5;
        ''')
        top_sold_products = cursor.fetchall()

        # Fetch top 5 minimum cost products
        cursor.execute('''
            SELECT id, name, description, image_url, price
            FROM products
            ORDER BY price ASC
            LIMIT 5;
        ''')
        min_cost_products = cursor.fetchall()

        # Fetch top-selling product for each category
        cursor.execute('''
            SELECT 
                p.category_name,
                p.id AS product_id,
                p.name AS product_name,
                p.description,
                p.image_url,
                SUM(s.quantity) AS total_sold
            FROM sales s
            JOIN products p ON s.product_id = p.id
            GROUP BY p.category_name, p.id, p.name, p.description, p.image_url
            HAVING total_sold = (
                SELECT MAX(total_sold)
                FROM (
                    SELECT p.category_name, SUM(s.quantity) AS total_sold
                    FROM sales s
                    JOIN products p ON s.product_id = p.id
                    GROUP BY p.category_name, p.id
                ) subquery
                WHERE subquery.category_name = p.category_name
            )
            ORDER BY p.category_name;
        ''')
        top_category_sales = cursor.fetchall()

        # Fetch products that have not been sold
        cursor.execute('''
            SELECT id, name, description, image_url, price, quantity
            FROM products p
            WHERE NOT EXISTS (
                SELECT 1
                FROM orders o
                WHERE o.product_id = p.id
            );
        ''')
        unsold_products = cursor.fetchall()

        return render_template(
            'dashboard.html',
            top_sold_products=top_sold_products,
            min_cost_products=min_cost_products,
            top_category_sales=top_category_sales,
            unsold_products=unsold_products  # Pass the unsold products to the template
        )

    except Exception as e:
        print(f"Error fetching top products: {e}")
        flash("An error occurred while fetching top products.")
        return redirect(url_for('dashboard'))

    finally:
        cursor.close()
        conn.close()
'''@app.route('/get-product-data/<code>', methods=['GET'])
def get_product_data(code):
    try:
        # Debugging: Print the product code received
        print(f"Received product code: {code}")
        
        # Example query to fetch data related to the product code
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Query for product price over time
        query = """
            SELECT order_date, total_price
            FROM sales
            WHERE product_code = %s
            ORDER BY order_date
        """
        
        print(f"Executing query: {query} with product_code = {code}")
        cursor.execute(query, (code,))
        
        # Fetch the results
        results = cursor.fetchall()
        
        # Debugging: Print the results from the query
        print(f"Query results: {results}")
        
        # Check if results are empty
        if not results:
            print("No data found for this product code.")
            return jsonify({'error': 'No data found for the given product code.'})
        
        # Prepare data for the chart (assuming you want to plot price over time)
        dates = [result[0].strftime('%Y-%m-%d') for result in results]  # Format dates as strings
        prices = [result[1] for result in results]  # Extract prices
        
        # Debugging: Print the prepared data
        print(f"Prepared data - Dates: {dates}, Prices: {prices}")
        
        # Return the data as JSON for use in Chart.js
        return jsonify({'dates': dates, 'prices': prices})
    
    except Exception as e:
        # Log any exceptions
        print(f"Error occurred: {e}")
        return jsonify({'error': 'An error occurred while processing the request.'}), 500
'''

if __name__ == '__main__':
    app.run(debug=True)
