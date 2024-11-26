database structure 

create database intern;


use intern;


CREATE TABLE categories (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);


CREATE TABLE orders (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    product_code VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    cost DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    customer_name VARCHAR(255) NOT NULL,
    customer_address TEXT NOT NULL,
    payment_mode VARCHAR(50) NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    country VARCHAR(255),
    age_range VARCHAR(50),
    gender VARCHAR(50),
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);


CREATE TABLE products (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    quantity INT NOT NULL,
    image_url VARCHAR(255),
    min_quantity INT DEFAULT 10,
    last_sold_date DATE,
    last_updated DATETIME,
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
);


CREATE TABLE sales (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    product_code VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    payment_mode VARCHAR(30),
    country VARCHAR(255),
    total_price DECIMAL(10,2) NOT NULL,
    order_date DATETIME NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);


CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE password_reset_requests (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    otp VARCHAR(6) NOT NULL,
    request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO products (id, name, code, description, price, quantity, image_url, min_quantity, last_sold_date, last_updated, category_id)
VALUES
(14, 'Smartphone', 'ELEC001', 'A high-end smartphone with 128GB storage.', 700.00, 45, 'https://example.com/images/smartphone.jpg', 10, '2024-11-26', '2024-11-25 11:41:53', 1),
(15, 'Laptop', 'ELEC002', 'Lightweight laptop with Intel i7 processor.', 1000.00, 27, 'https://example.com/images/laptop.jpg', 10, '2024-11-26', '2024-11-25 11:42:07', 1),
(16, 'Bluetooth Speaker', 'ELEC003', 'Portable Bluetooth speaker with great sound.', 49.99, 96, 'https://example.com/images/speaker.jpg', 10, '2024-11-26', NULL, 1),
(17, 'Headphones', 'ELEC004', 'Noise-cancelling over-ear headphones.', 129.99, 40, 'https://example.com/images/headphones.jpg', 10, NULL, NULL, 1),
(18, 'Fiction Book', 'BOOK001', 'Bestselling fiction novel.', 15.99, 198, 'https://example.com/images/fiction_book.jpg', 10, '2024-11-25', NULL, 2),
(19, 'Programming Guide', 'BOOK002', 'Comprehensive guide to Python programming.', 49.99, 148, 'https://example.com/images/programming_guide.jpg', 10, '2024-11-25', NULL, 2),
(20, 'History Textbook', 'BOOK003', 'A detailed history textbook.', 25.99, 120, 'https://example.com/images/history_textbook.jpg', 10, NULL, NULL, 2),
(21, 'Cookbook', 'BOOK004', 'Delicious recipes from around the world.', 19.99, 300, 'https://example.com/images/cookbook.jpg', 10, NULL, NULL, 2),
(22, 'T-Shirt', 'CLOT001', 'Cotton t-shirt available in multiple colors.', 9.99, 498, 'https://example.com/images/tshirt.jpg', 10, '2024-11-25', NULL, 3),
(23, 'Jeans', 'CLOT002', 'Denim jeans with a relaxed fit.', 40.00, 247, 'https://example.com/images/jeans.jpg', 10, '2024-11-25', '2024-11-25 11:42:39', 3),
(24, 'Jacket', 'CLOT003', 'Waterproof jacket for outdoor activities.', 79.99, 96, 'https://example.com/images/jacket.jpg', 10, '2024-11-25', NULL, 3),
(25, 'Sneakers', 'CLOT004', 'Comfortable sneakers for daily wear.', 59.99, 195, 'https://example.com/images/sneakers.jpg', 10, '2024-11-25', NULL, 3),
(26, 'Microwave Oven', 'HOME001', '700W microwave oven with multiple settings.', 100.00, 5, 'https://example.com/images/microwave.jpg', 10, '2024-11-25', '2024-11-25 11:52:54', 4),
(27, 'Vacuum Cleaner', 'HOME002', 'Bagless vacuum cleaner with HEPA filter.', 129.99, 60, 'https://example.com/images/vacuum_cleaner.jpg', 10, NULL, NULL, 4),
(28, 'Blender', 'HOME003', 'Powerful blender for smoothies and soups.', 50.00, 150, 'https://example.com/images/blender.jpg', 10, NULL, '2024-11-25 11:42:50', 4),
(29, 'Air Purifier', 'HOME004', 'HEPA air purifier for clean indoor air.', 199.99, 9, 'https://example.com/images/air_purifier.jpg', 10, '2024-11-25', NULL, 4);


INSERT INTO sales (id, product_id, product_name, product_code, quantity, payment_mode, country, total_price, order_date)
VALUES
(1, 14, 'Smartphone', 'ELEC001', 2, NULL, NULL, 1399.98, '2024-11-25 11:36:15'),
(2, 15, 'Laptop', 'ELEC002', 2, NULL, NULL, 1999.98, '2024-11-25 11:36:42'),
(3, 16, 'Bluetooth Speaker', 'ELEC003', 2, NULL, NULL, 99.98, '2024-11-25 11:37:17'),
(4, 18, 'Fiction Book', 'BOOK001', 2, NULL, NULL, 31.98, '2024-11-25 11:37:43'),
(5, 19, 'Programming Guide', 'BOOK002', 2, NULL, NULL, 99.98, '2024-11-25 11:38:10'),
(6, 22, 'T-Shirt', 'CLOT001', 2, NULL, NULL, 19.98, '2024-11-25 11:38:31'),
(7, 24, 'Jacket', 'CLOT003', 2, NULL, NULL, 159.98, '2024-11-25 11:38:55'),
(8, 23, 'Jeans', 'CLOT002', 3, NULL, NULL, 119.97, '2024-11-25 11:39:15'),
(9, 25, 'Sneakers', 'CLOT004', 5, NULL, NULL, 299.95, '2024-11-25 11:39:35'),
(10, 26, 'Microwave Oven', 'HOME001', 7, NULL, NULL, 629.93, '2024-11-25 11:40:14'),
(11, 29, 'Air Purifier', 'HOME004', 21, NULL, NULL, 4199.79, '2024-11-25 11:44:34'),
(12, 24, 'Jacket', 'CLOT003', 2, NULL, NULL, 159.98, '2024-11-25 12:01:11'),
(13, 14, 'Smartphone', 'ELEC001', 3, NULL, NULL, 2100.00, '2024-11-26 00:04:21'),
(14, 16, 'Bluetooth Speaker', 'ELEC003', 2, 'Cash', NULL, 99.98, '2024-11-26 00:47:50'),
(15, 15, 'Laptop', 'ELEC002', 1, 'Card', NULL, 1000.00, '2024-11-26 00:51:55');


INSERT INTO orders (id, product_id, product_name, product_code, quantity, cost, total_price, customer_name, customer_address, payment_mode, order_date, country, age_range, gender)
VALUES
(11, 14, 'Smartphone', 'ELEC001', 2, 15000.00, 30000.00, 'Alice Johnson', '123 Elm Street, NY', 'Cash', '2024-11-01 10:15:30', 'USA', '18-25', 'Female'),
(12, 14, 'Smartphone', 'ELEC001', 1, 15000.00, 15000.00, 'John Doe', '456 Oak Avenue, LA', 'Card', '2024-11-05 14:45:00', 'USA', '26-35', 'Male'),
(13, 15, 'Laptop', 'ELEC002', 1, 60000.00, 60000.00, 'Jane Smith', '789 Pine Road, SF', 'UPI', '2024-11-02 16:30:00', 'USA', '26-35', 'Female'),
(14, 15, 'Laptop', 'ELEC002', 1, 60000.00, 60000.00, 'Tom Baker', '321 Maple Lane, TX', 'Cash', '2024-11-07 09:10:15', 'Canada', '36-45', 'Male'),
(15, 16, 'Tablet', 'ELEC003', 3, 25000.00, 75000.00, 'Emily Davis', '654 Birch Blvd, FL', 'Card', '2024-11-03 11:20:25', 'USA', '18-25', 'Female'),
(16, 16, 'Tablet', 'ELEC003', 2, 25000.00, 50000.00, 'David Lee', '987 Cedar St, NJ', 'UPI', '2024-11-09 13:45:30', 'India', '26-35', 'Male'),
(17, 17, 'Headphones', 'ELEC004', 5, 2000.00, 10000.00, 'Chris Evans', '123 Elm Street, NY', 'Cash', '2024-11-04 17:30:45', 'USA', '36-45', 'Male'),
(18, 17, 'Headphones', 'ELEC004', 10, 2000.00, 20000.00, 'Linda Green', '456 Oak Avenue, LA', 'Card', '2024-11-08 20:15:00', 'USA', '46-55', 'Female');


INSERT INTO users (id, email, password, created_at)
VALUES (1, 'praneshvaradharaj@gmail.com', '2005', '2024-11-22 12:15:06');
