CREATE TABLE categories (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
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

CREATE TABLE price_history (
    product_code VARCHAR(50),
    price DECIMAL(10,2),
    time DATE,
    name VARCHAR(100)
);


CREATE TABLE product_image (
    id INT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(50),
    image_url VARCHAR(255)
);


INSERT INTO categories (id, name) VALUES
(1, 'Electronics'),
(2, 'Books'),
(4, 'Home Appliances'),
(5, 'Beauty and Personal Care'),
(6, 'Sports and Fitness'),
(7, 'Toys and Games'),
(8, 'Stationery and Office Supplies'),
(9, 'Art and Craft'),
(10, 'Jewelry and Accessories'),
(11, 'Music and Instruments'),
(12, 'Baby Products');


INSERT INTO products (id, name, code, description, price, quantity, image_url, min_quantity, last_sold_date, category_id) VALUES
(1, 'Smartphone', 'ELE001', 'A high-end smartphone with a sleek design.', 700.00, 69, '/static/images/smartphone_3.jpg', 10, '2024-12-05', 1),
(2, 'Laptop', 'ELE002', 'Powerful gaming laptop with a modern design.', 1300.00, 22, '/static/images/laptop_2.jpg', 10, '2024-12-05', 1),
(3, 'Headphones', 'ELE003', 'Wireless noise-cancelling headphones.', 199.99, 96, '/static/images/headphone_2.jpg', 10, '2024-12-05', 1),
(4, 'Smartwatch', 'ELE004', 'Stylish smartwatch with health tracking.', 250.00, 73, '/static/images/smartwatch_2.jpg', 10, '2024-12-05', 1),
(5, 'Tablet', 'ELE005', 'Portable tablet with HD display.', 349.99, 60, '/static/images/tablet_1.png', 10, NULL, 1),
(6, 'Fiction Novel', 'BKS001', 'Bestselling fiction novel.', 19.99, 200, '/static/images/fiction_novel_1.jpg', 10, NULL, 2),
(7, 'Biography', 'BKS002', 'Inspiring life story of a famous individual.', 25.00, 145, '/static/images/biography_book_3.jpg', 10, '2024-12-05', 2),
(8, 'Cookbook', 'BKS003', 'Recipes from around the world.', 29.99, 96, '/static/images/cookbook_2.jpg', 10, '2024-12-05', 2),
(9, 'Science Book', 'BKS004', 'Exploring modern scientific concepts.', 39.99, 113, '/static/images/science_book_3.jpg', 10, '2024-12-05', 2),
(10, 'Children?s Book', 'BKS005', 'Illustrated storybook for kids.', 14.99, 175, '/static/images/childrens_book_2.jpg', 10, '2024-12-05', 2),
(11, 'Air Conditioner', 'HAP001', 'Energy-efficient split air conditioner.', 499.99, 20, '/static/images/air_conditioner_2.jpg', 10, NULL, 4),
(12, 'Washing Machine', 'HAP002', 'Front-load washing machine with advanced features.', 399.99, 15, '/static/images/washing_machine_1.jpg', 10, NULL, 4),
(13, 'Microwave Oven', 'HAP003', 'Compact microwave oven with smart cooking options.', 149.99, 30, '/static/images/micro_oven_2.jpg', 10, NULL, 4),
(14, 'Vacuum Cleaner', 'HAP004', 'Powerful vacuum cleaner for all surfaces.', 129.99, 9, '/static/images/vacuum_cleaner_3.jpg', 10, NULL, 4),
(15, 'Refrigerator', 'HAP005', 'Double-door refrigerator with frost-free technology.', 699.99, 10, '/static/images/Refrigerator_1.jpg', 10, NULL, 4),
(16, 'Shampoo', 'BPC001', 'Nourishing shampoo for healthy hair.', 9.99, 100, '/static/images/shampoo_bottle_3.jpg', 10, NULL, 5),
(17, 'Conditioner', 'BPC002', 'Hydrating conditioner for smooth hair.', 11.99, 80, '/static/images/conditioner_2.jpg', 10, NULL, 5),
(18, 'Face Cream', 'BPC003', 'Moisturizing face cream for glowing skin.', 19.99, 70, '/static/images/facecream_2.jpg', 10, NULL, 5),
(19, 'Body Lotion', 'BPC004', 'Rich body lotion for soft skin.', 14.99, 90, '/static/images/body_lotion_3.jpg', 10, NULL, 5),
(20, 'Lipstick', 'BPC005', 'Matte lipstick in various shades.', 7.99, 120, '/static/images/lipstick_1.jpg', 10, NULL, 5),
(21, 'Yoga Mat', 'SPF001', 'Non-slip yoga mat for home and gym use.', 19.99, 9, '/static/images/yoga_mat_1.jpg', 10, NULL, 6),
(22, 'Dumbbells', 'SPF002', 'Adjustable dumbbell set for strength training.', 49.99, 40, '/static/images/dumbell_2.jpg', 10, NULL, 6),
(23, 'Treadmill', 'SPF003', 'Electric treadmill with multiple workout modes.', 599.99, 10, '/static/images/treadmill_3.jpg', 10, NULL, 6),
(24, 'Resistance Bands', 'SPF004', 'Set of 5 resistance bands with different tension levels.', 14.99, 100, '/static/images/resistance_band_2.jpg', 10, NULL, 6),
(25, 'Football', 'SPF005', 'Premium quality leather football.', 29.99, 70, '/static/images/football_2.jpg', 10, NULL, 6),
(26, 'Building Blocks', 'TAG001', 'Creative building block set for kids.', 19.99, 100, '/static/images/building_blocks_3.jpg', 10, NULL, 7),
(27, 'Remote Control Car', 'TAG002', 'High-speed remote control car for kids.', 49.99, 40, '/static/images/remote_control_car_1.jpg', 10, NULL, 7),
(28, 'Board Game', 'TAG003', 'Classic family board game for all ages.', 29.99, 60, '/static/images/board_games_1.jpg', 10, NULL, 7),
(29, 'Dollhouse', 'TAG004', 'Fully furnished dollhouse with accessories.', 89.99, 20, '/static/images/dollhouse_1.jpg', 10, NULL, 7),
(30, 'Action Figure', 'TAG005', 'Collectible action figure with detailed features.', 24.99, 70, '/static/images/action_figure_1.jpg', 10, NULL, 7);


INSERT INTO orders (id, product_id, product_name, product_code, quantity, cost, total_price, customer_name, customer_address, payment_mode, order_date, country, age_range, gender) VALUES
(1, 1, 'Smartphone', 'ELE001', 2, 1399.98, 0.00, 'Pranesh Kumar', 'Xxx', 'Cash', '2024-12-05 03:16:21', 'India', '18-25', 'Male'),
(2, 1, 'Smartphone', 'ELE001', 5, 3499.95, 0.00, 'Pranesh Kumar', 'Xxx', 'Credit Card', '2024-12-05 03:17:19', 'Canada', '26-35', 'Female'),
(3, 1, 'Smartphone', 'ELE001', 3, 2099.97, 0.00, 'Pranesh Kumar', 'Xxx', 'Debit Card', '2024-12-05 03:17:37', 'UK', '36-55', 'Male'),
(4, 2, 'Laptop', 'ELE002', 3, 3899.97, 0.00, 'Pranesh Kumar', 'Xxx', 'UPI', '2024-12-05 03:17:56', 'UK', '36-55', 'Female'),
(5, 2, 'Laptop', 'ELE002', 2, 2599.98, 0.00, 'Pranesh Kumar', 'Xxx', 'Cash', '2024-12-05 03:18:14', 'USA', '26-35', 'Female'),
(6, 3, 'Headphones', 'ELE003', 3, 599.97, 0.00, 'Pranesh Kumar', 'Xxx', 'Debit Card', '2024-12-05 03:18:37', 'UK', 'Above 55', 'Male'),
(7, 4, 'Smartwatch', 'ELE004', 2, 499.98, 0.00, 'Manish Kumar', 'Xxx', 'UPI', '2024-12-05 03:18:56', 'UK', 'Above 55', 'Male'),
(8, 7, 'Biography', 'BKS002', 5, 124.95, 0.00, 'Pranesh Kumar', 'Xxx', 'Credit Card', '2024-12-05 03:19:59', 'Canada', 'Above 55', 'Female'),
(9, 8, 'Cookbook', 'BKS003', 4, 119.96, 0.00, 'Pranesh Kumar', 'Xxx', 'Credit Card', '2024-12-05 03:20:19', 'Canada', '26-35', 'Male'),
(10, 10, 'Children?s Book', 'BKS005', 5, 74.95, 0.00, 'Pranesh Kumar', 'Xxx', 'Debit Card', '2024-12-05 03:20:43', 'Canada', 'Above 55', 'Female'),
(11, 9, 'Science Book', 'BKS004', 7, 279.93, 0.00, 'Pranesh Kumar', 'Xxx', 'Credit Card', '2024-12-05 03:21:10', 'India', 'Above 55', 'Female'),
(12, 2, 'Laptop', 'ELE002', 3, 3899.97, 0.00, 'Pranesh Kumar', 'Xxx', 'Credit Card', '2024-12-05 08:31:35', 'India', '26-35', 'Male'),
(13, 3, 'Headphones', 'ELE003', 1, 199.99, 0.00, 'Pranesh Kumar', 'Xxx', 'Cash', '2024-12-05 08:42:55', 'Canada', '18-25', 'Male'),
(14, 1, 'Smartphone', 'ELE001', 2, 1400.00, 1400.00, 'Pranesh Kumar', 'Xxx', 'UPI', '2024-12-05 08:54:13', 'Canada', '26-35', 'Male');


INSERT INTO sales (
    id, product_id, product_name, product_code, quantity,
    payment_mode, country, total_price, order_date
) VALUES
(1, 1, 'Smartphone', 'ELE001', 2, 'Cash', NULL, 1399.98, '2024-12-02 03:16:21'),
(2, 1, 'Smartphone', 'ELE001', 5, 'Credit Card', NULL, 3499.95, '2024-12-05 03:17:19'),
(3, 1, 'Smartphone', 'ELE001', 3, 'Debit Card', NULL, 2099.97, '2024-12-05 03:17:37'),
(4, 2, 'Laptop', 'ELE002', 3, 'UPI', NULL, 3899.97, '2024-12-05 03:17:56'),
(5, 2, 'Laptop', 'ELE002', 2, 'Cash', NULL, 2599.98, '2024-12-05 03:18:14'),
(6, 3, 'Headphones', 'ELE003', 3, 'Debit Card', NULL, 599.97, '2024-12-05 03:18:37'),
(7, 4, 'Smartwatch', 'ELE004', 2, 'UPI', NULL, 499.98, '2024-12-05 03:18:56'),
(8, 7, 'Biography', 'BKS002', 5, 'Credit Card', NULL, 124.95, '2024-12-05 03:19:59'),
(9, 8, 'Cookbook', 'BKS003', 4, 'Credit Card', NULL, 119.96, '2024-12-05 03:20:19'),
(10, 10, 'Children?s Book', 'BKS005', 5, 'Debit Card', NULL, 74.95, '2024-12-05 03:20:43'),
(11, 9, 'Science Book', 'BKS004', 7, 'Credit Card', NULL, 279.93, '2024-12-05 03:21:10'),
(12, 2, 'Laptop', 'ELE002', 3, 'Credit Card', 'India', 3899.97, '2024-12-05 08:31:35'),
(13, 3, 'Headphones', 'ELE003', 1, 'Cash', 'Canada', 199.99, '2024-12-05 08:42:55'),
(14, 1, 'Smartphone', 'ELE001', 2, 'UPI', 'Canada', 1400.00, '2024-12-05 08:54:13');


INSERT INTO users (id, email, password, created_at) VALUES
(1, 'praneshvaradharaj@gmail.com', '1234', '2024-11-22 12:15:06');









INSERT INTO product_image (id, code, image_url) VALUES
(1, 'ELE001', '/static/images/smartphone_1.jpg'),
(2, 'ELE001', '/static/images/smartphone_2.jpg'),
(3, 'ELE002', '/static/images/laptop_1.jpg'),
(4, 'ELE002', '/static/images/laptop_3.jpg'),
(5, 'ELE003', '/static/images/headphone_1.jpg'),
(6, 'ELE003', '/static/images/headphone_3.jpg'),
(7, 'ELE004', '/static/images/smartwatch_1.jpg'),
(8, 'ELE004', '/static/images/smartwatch_3.jpg'),
(9, 'ELE005', '/static/images/tablet_2.jpg'),
(10, 'ELE005', '/static/images/tablet_3.jpeg'),
(11, 'BKS001', '/static/images/fiction_novel_2.jpg'),
(12, 'BKS001', '/static/images/fiction_novel_3.jpg'),
(13, 'BKS002', '/static/images/biography_book_1.jpg'),
(14, 'BKS002', '/static/images/biography_book_2.jpg'),
(15, 'BKS003', '/static/images/cookbook_1.jpg'),
(16, 'BKS003', '/static/images/cookbook_3.jpg'),
(17, 'BKS004', '/static/images/science_book_1.jpg'),
(18, 'BKS004', '/static/images/science_book_2.jpg'),
(19, 'BKS005', '/static/images/childrens_book_1.jpg'),
(20, 'BKS005', '/static/images/childrens_book_3.jpg'),
(21, 'HAP001', '/static/images/air_conditioner_1.jpg'),
(22, 'HAP001', '/static/images/air_conditioner_3.jpg'),
(23, 'HAP002', '/static/images/washing_machine_2.png'),
(24, 'HAP002', '/static/images/washing_machine_3.jpg'),
(25, 'HAP003', '/static/images/micro_oven_1.jpg'),
(26, 'HAP003', '/static/images/micro_oven_3.jpg'),
(27, 'HAP004', '/static/images/vacuum_cleaner_1.jpg'),
(28, 'HAP004', '/static/images/vacuum_cleaner_2.jpg'),
(29, 'HAP005', '/static/images/Refrigerator_2.jpg'),
(30, 'HAP005', '/static/images/Refrigerator_3.jpg'),
(31, 'BPC001', '/static/images/shampoo_bottle_1.jpg'),
(32, 'BPC001', '/static/images/shampoo_bottle_2.jpg'),
(33, 'BPC002', '/static/images/conditioner_1.jpg'),
(34, 'BPC002', '/static/images/conditioner_3.jpg'),
(35, 'BPC003', '/static/images/facecream_1.jpg'),
(36, 'BPC003', '/static/images/facecream_3.jpg'),
(37, 'BPC004', '/static/images/body_lotion_1.jpg'),
(38, 'BPC004', '/static/images/body_lotion_2.jpg'),
(39, 'BPC005', '/static/images/lipstick_2.jpg'),
(40, 'BPC005', '/static/images/lipstick_3.jpg'),
(41, 'SPF001', '/static/images/yoga_mat_2.jpg'),
(42, 'SPF001', '/static/images/yoga_mat_3.jpg'),
(43, 'SPF002', '/static/images/dumbell_1.jpg'),
(44, 'SPF002', '/static/images/dumbell_3.jpg'),
(45, 'SPF003', '/static/images/treadmill_1.jpg'),
(46, 'SPF003', '/static/images/treadmill_2.jpg'),
(47, 'SPF004', '/static/images/resistance_band_1.jpg'),
(48, 'SPF004', '/static/images/resistance_band_3.jpg'),
(49, 'SPF005', '/static/images/football_1.jpg'),
(50, 'SPF005', '/static/images/football_3.jpg'),
(51, 'TAG001', '/static/images/building_blocks_1.jpg'),
(52, 'TAG001', '/static/images/building_blocks_2.jpg'),
(53, 'TAG002', '/static/images/remote_control_car_2.jpg'),
(54, 'TAG002', '/static/images/remote_control_car_3.jpg'),
(55, 'TAG003', '/static/images/board_games_2.jpg'),
(56, 'TAG003', '/static/images/board_games_3.jpg'),
(57, 'TAG004', '/static/images/dollhouse_2.jpg'),
(58, 'TAG004', '/static/images/dollhouse_3.jpg'),
(59, 'TAG005', '/static/images/action_figure_2.jpg'),
(60, 'TAG005', '/static/images/action_figure_3.jpg'),
(61, 'SOS001', '/static/images/notebook_2.jpg'),
(62, 'SOS001', '/static/images/notebook_3.jpg'),
(63, 'SOS002', '/static/images/ballpoint_pen_2.jpg'),
(64, 'SOS002', '/static/images/ballpoint_pen_3.jpg'),
(65, 'SOS004', '/static/images/sticky_notes_1.jpg'),
(66, 'SOS004', '/static/images/sticky_notes_2.jpg'),
(67, 'SOS005', '/static/images/paperclips_2.jpg'),
(68, 'SOS005', '/static/images/paperclips_3.jpg'),
(69, 'SOS006', '/static/images/filing_folder_2.jpg'),
(70, 'SOS006', '/static/images/filing_folder_3.jpg'),
(71, 'AAC001', '/static/images/acrylic_paint_set_2.jpg'),
(72, 'AAC001', '/static/images/acrylic_paint_set_3.jpg'),
(73, 'AAC002', '/static/images/paint_brush_set_1.jpg'),
(74, 'AAC002', '/static/images/paint_brush_set_2.jpg'),
(75, 'AAC003', '/static/images/sketch_pad_1.jpg'),
(76, 'AAC003', '/static/images/sketch_pad_3.jpg'),
(77, 'AAC004', '/static/images/craft_paper_1.jpg'),
(78, 'AAC004', '/static/images/craft_paper_2.jpg'),
(79, 'AAC005', '/static/images/glue_gun_3.jpg'),
(80, 'AAC005', '/static/images/glue_gun_2.jpg'),
(81, 'JNA001', '/static/images/gold_necklace_1.jpg'),
(82, 'JNA001', '/static/images/gold_necklace_2.jpg'),
(83, 'JNA002', '/static/images/silver_bracelet_1.jpg'),
(84, 'JNA002', '/static/images/silver_bracelet_3.jpg'),
(85, 'JNA003', '/static/images/diamond_earings_2.jpg'),
(86, 'JNA003', '/static/images/diamond_earings_3.jpg'),
(87, 'JNA004', '/static/images/leather_wallet_2.jpg'),
(88, 'JNA004', '/static/images/leather_wallet_3.jpg'),
(89, 'JNA005', '/static/images/pearl_pendant_1.jpg'),
(90, 'JNA005', '/static/images/pearl_pendant_3.jpg'),
(91, 'MAI001', '/static/images/acoustic_guitar_2.jpg'),
(92, 'MAI001', '/static/images/acoustic_guitar_3.jpg'),
(93, 'MAI002', '/static/images/digital_piano_2.jpg'),
(94, 'MAI002', '/static/images/digital_piano_3.jpg'),
(95, 'MAI003', '/static/images/violin_1.jpg'),
(96, 'MAI003', '/static/images/violin_3.jpg'),
(97, 'MAI004', '/static/images/drumsticks_2.jpg'),
(98, 'MAI004', '/static/images/drumsticks_3.jpg'),
(99, 'MAI005', '/static/images/harmonica_2.jpg'),
(100, 'MAI005', '/static/images/harmonica_3.jpg'),
(101, 'BP001', '/static/images/baby_stroller_1.jpg'),
(102, 'BP001', '/static/images/baby_stroller_2.jpg'),
(103, 'BP002', '/static/images/baby_crib_3.jpg'),
(104, 'BP002', '/static/images/baby_crib_2.jpg'),
(105, 'BP003', '/static/images/baby_feeding_bottle_2.jpg'),
(106, 'BP003', '/static/images/baby_feeding_bottle_3.jpg'),
(107, 'BP004', '/static/images/baby_diaper_1.jpg'),
(108, 'BP004', '/static/images/baby_diaper_3.jpg'),
(109, 'BP005', '/static/images/baby_wipes_1.jpg'),
(110, 'BP005', '/static/images/baby_wipes_3.jpg');




















INSERT INTO price_history (product_code, price, time, name) VALUES
('ELE004', 250.00, '2024-12-05', ''),
('q4t43f', 733.00, '2024-12-05', 'summa'),
('q4t43f', 735.00, '2024-12-05', 'summa'),
('q4t43f', 700.00, '2024-12-04', 'summa'),
('q4t43f', 735.00, '2024-12-05', 'summa'),
('ELE001', 700.00, '2024-12-05', 'Smartphone'),
('ELE001', 550.00, '2024-12-03', 'Smartphone'),
('vaerfa', 584.00, '2024-12-05', 'sample2'),
('vaer', 48.00, '2024-12-05', 'sample4'),
('ELE001', 699.99, '2024-12-05', 'SmartPhone'),
('ELE002', 1300.00, '2024-12-07', 'Laptop'),
('ELE001', 700.00, '2024-12-07', 'SmartPhone');
