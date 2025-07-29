

CREATE TABLE Customer_Account (
    Username VARCHAR(50) PRIMARY KEY UNIQUE,
    Password VARCHAR(50) NOT NULL
);


CREATE TABLE Customers (
    Name VARCHAR(50) NOT NULL,
    Phone VARCHAR(20) NOT NULL,
    Email VARCHAR(100) PRIMARY KEY,
    Address VARCHAR (100) NOT NULL
);


CREATE TABLE Categories (
    Category_ID INT PRIMARY KEY,
    Category_Name VARCHAR(50)
);




CREATE TABLE Product_Page (
    Product_ID INT PRIMARY KEY,
    Product_Name VARCHAR(20),
    Product_price INT,
    Category_ID INT,
    FOREIGN KEY (Category_ID) REFERENCES Categories(Category_ID)
);

CREATE TABLE Inventory (
    Product_Name VARCHAR(20),
    Quantity_Left INT
);


CREATE TABLE Cart_Item (
    Quantity INT NOT NULL,
    Total_Cost INT,
    Order_ID INT PRIMARY KEY,
    Product_ID INT,
    FOREIGN KEY (Product_ID) REFERENCES Product_Page(Product_ID)
);


CREATE TABLE Payment (
    Payment_ID INT PRIMARY KEY,
    Amount INT,
    Order_ID INT,
    FOREIGN KEY (Order_ID) REFERENCES Cart_Item(Order_ID)
);


CREATE TABLE Tracking (
    Tracking_ID INT PRIMARY KEY,
    Order_ID INT,
    Customer_Address VARCHAR(50),
    Delivery_Time VARCHAR(20),
    FOREIGN KEY (Order_ID) REFERENCES Cart_Item(Order_ID)
);



CREATE INDEX idx_Email ON Customers (Email);
CREATE INDEX idx_CategoryID ON Product_Page (Category_ID);
CREATE INDEX idx_OrderID_Cart ON Cart_Item (Order_ID);
CREATE INDEX idx_OrderID_Payment ON Payment (Order_ID);
CREATE INDEX idx_OrderID_Tracking ON Tracking (Order_ID);
CREATE INDEX idx_Username ON Customer_Account (Username);





INSERT INTO Customer_Account (Username, Password)
VALUES 
    ('Tikam1', 'password123'),
    ('Tikam2', 'password123'),
    ('Tikam3', 'password123'),
    ('Tikam4', 'password123'),
    ('Tikam5', 'password123'),
    ('Tikam6', 'password123'),
    ('Tikam7', 'password123'),
    ('Tikam8', 'password123'),
    ('Tikam9', 'password123'),
    ('Tikam10', 'password123');




INSERT INTO Customers (Name, Phone, Email, Address)
VALUES 
    ('Tikam1', '123456789', 'tikam1@iiitd.ac.in', 'Hostel H1 IIIT delhi'),
    ('Tikam2', '123456789', 'tikam2@iiitd.ac.in', 'Hostel H1 IIIT delhi'),
    ('Tikam3', '123456789', 'tikam3@iiitd.ac.in', 'Hostel H1 IIIT delhi'),
    ('Tikam4', '123456789', 'tikam4@iiitd.ac.in', 'Hostel H1 IIIT delhi'),
    ('Tikam5', '123456789', 'tikam5@iiitd.ac.in', 'Hostel H1 IIIT delhi'),
    ('Tikam6', '123456789', 'tikam6@iiitd.ac.in', 'Hostel H1 IIIT delhi'),
    ('Tikam7', '123456789', 'tikam7@iiitd.ac.in', 'Hostel H1 IIIT delhi'),
    ('Tikam8', '123456789', 'tikam8@iiitd.ac.in', 'Hostel H1 IIIT delhi'),
    ('Tikam9', '123456789', 'tikam9@iiitd.ac.in', 'Hostel H1 IIIT delhi'),
    ('Tikam10', '123456789', 'tikam10@iiitd.ac.in', 'Hostel H1 IIIT delhi');


INSERT INTO Categories (Category_ID, Category_Name)
VALUES 
    (1, 'Shirt'),
    (2, 'T-Shirt'),
    (3, 'Jeans'),
    (4, 'Sweatshirts'),
    (5, 'Jackets'),
    (6, 'Innerwear'),
    (7, 'Shoes'),
    (8, 'Watches'),
    (9, 'Formal_Shirts'),
    (10, 'Formal Shoes');


INSERT INTO Product_Page (Product_ID, Product_Name, Product_price, Category_ID)
VALUES 
    (1, 'Gucci_Shirt', 50000, 1),
    (2, 'Gucci T-Shirt', 20000, 2),
    (3, 'Levi_Jeans', 3000, 3),
    (4, 'Roadster_Sweatshirts', 1000, 4),
    (5, 'Wrogn_Jackets', 3000, 5),
    (6, 'Jockey_Underwear', 500, 6),
    (7, 'Nike_Shoes', 10000, 7),
    (8, 'Rolex_Watch', 50000, 8),
    (9, 'Here&Now', 500, 9),
    (10, 'Bata', 10000, 10);


INSERT INTO Inventory (Product_Name, Quantity_Left)
VALUES 
    ('Gucci_Shirt', 100),
    ('Gucci T-Shirt', 100),
    ('Levi_Jeans', 100),
    ('Roadster_Sweatshirts', 100),
    ('Wrogn_Jackets', 100),
    ('Jockey_Underwear', 100),
    ('Nike_Shoes', 100),
    ('Rolex_Watch', 100),
    ('Here&Now', 100),
    ('Bata', 100);


INSERT INTO Cart_Item (Quantity, Total_Cost, Order_ID, Product_ID)
VALUES 
    (1, 50000, 1, 1),
    (2, 40000, 2, 2),
    (3, 9000, 3, 3),
    (4, 4000, 4, 4),
    (5, 3000, 5, 5),
    (1, 500, 6, 6),
    (2, 20000, 7, 7),
    (3, 150000, 8, 8),
    (4, 2000, 9, 9),
    (5, 50000, 10, 10);







INSERT INTO Payment (Payment_ID, Amount, Order_ID)
VALUES 
    (1, 50000, 1),
    (2, 40000, 2),
    (3, 9000, 3),
    (4, 4000, 4),
    (5, 3000, 5),
    (6, 500, 6),
    (7, 2000, 7),
    (8, 150000, 8),
    (9, 2000, 9),
    (10, 50000, 10);




INSERT INTO Tracking (Tracking_ID, Order_ID, Customer_Address, Delivery_Time)
VALUES 
    (1, 1, 'Hostel H1 IIIT delhi', '2 days'),
    (2, 2, 'Hostel H1 IIIT delhi', '2 days'),
    (3, 3, 'Hostel H1 IIIT delhi', '2 days'),
    (4, 4, 'Hostel H1 IIIT delhi', '2 days'),
    (5, 5, 'Hostel H1 IIIT delhi', '2 days'),
    (6, 6, 'Hostel H1 IIIT delhi', '2 days'),
    (7, 7, 'Hostel H1 IIIT delhi', '2 days'),
    (8, 8, 'Hostel H1 IIIT delhi', '2 days'),
    (9, 9, 'Hostel H1 IIIT delhi', '2 days'),
    (10, 10, 'Hostel H1 IIIT delhi', '2 days');


-- DROP TABLE IF EXISTS Product_Page;
-- DROP TABLE IF EXISTS Customers;
-- DROP TABLE IF EXISTS Categories;
-- DROP TABLE IF EXISTS Cstomer_Account;
-- DROP TABLE IF EXISTS Cart_Item;
-- DROP TABLE IF EXISTS Tracking;
-- DROP TABLE IF EXISTS Payment;
-- UPDATE Customer_Account SET Login_Status = 'Success' WHERE Username = 'shared_username' AND Password = 'shared_password';
-- INSERT INTO Cart (User_ID, Product_ID, Quantity) VALUES (1, 1001, 1);


/* UPDATE Customer_Accounts SET Login_Status = 'Success' WHERE Username = 'shared_username' AND Password = 'shared_password';

CREATE TABLE Customer_Accounts (
    Username VARCHAR(50) PRIMARY KEY UNIQUE,
    Password VARCHAR(50) NOT NULL,
    Login_Status VARCHAR(20)
);

CREATE TABLE Customers (
    Name VARCHAR(50) NOT NULL,
    Phone VARCHAR(20) NOT NULL,
    Email VARCHAR(100) PRIMARY KEY,
    Address VARCHAR (100) NOT NULL
);

CREATE TABLE Categories (
    Category_ID INT PRIMARY KEY,
    Category_Name VARCHAR(50)
);

CREATE TABLE Product_Page (
    Product_ID INT PRIMARY KEY,
    Product_Name VARCHAR(20),
    Product_price INT,
    Category_ID INT,
    FOREIGN KEY (Category_ID) REFERENCES Categories(Category_ID)
);

CREATE TABLE Inventory (
    Product_Name VARCHAR(20),
    Quantity_Left INT
);

CREATE TABLE Cart_Item (
    Quantity INT NOT NULL,
    Total_Cost INT,
    Order_ID INT PRIMARY KEY,
    Product_ID INT,
    FOREIGN KEY (Product_ID) REFERENCES Product_Page(Product_ID)
);

CREATE TABLE Payment (
    Payment_ID INT PRIMARY KEY,
    Amount INT,
    Order_ID INT,
    FOREIGN KEY (Order_ID) REFERENCES Cart_Item(Order_ID)
);

CREATE TABLE Tracking (
    Tracking_ID INT PRIMARY KEY,
    Order_ID INT,
    Customer_Address VARCHAR(50),
    Delivery_Time VARCHAR(20),
    FOREIGN KEY (Order_ID) REFERENCES Cart_Item(Order_ID)
);

CREATE TABLE Cart (
    User_ID INT,
    Product_ID INT,
    Quantity INT,
    FOREIGN KEY (User_ID) REFERENCES Customers(Email),
    FOREIGN KEY (Product_ID) REFERENCES Product_Page(Product_ID)
);

CREATE INDEX idx_Email ON Customers (Email);
CREATE INDEX idx_CategoryID ON Product_Page (Category_ID);
CREATE INDEX idx_OrderID_Cart ON Cart_Item (Order_ID);
CREATE INDEX idx_OrderID_Payment ON Payment (Order_ID);
CREATE INDEX idx_OrderID_Tracking ON Tracking (Order_ID);
CREATE INDEX idx_Username ON Customer_Accounts (Username);


INSERT INTO Customer_Account (Username, Password)
VALUES 
    ('Tikam1', 'password123'),
    ('Tikam2', 'password123'),
    ('Tikam3', 'password123'),
    ('Tikam4', 'password123'),
    ('Tikam5', 'password123'),
    ('Tikam6', 'password123'),
    ('Tikam7', 'password123'),
    ('Tikam8', 'password123'),
    ('Tikam9', 'password123'),
    ('Tikam10', 'password123');




INSERT INTO Customers (Name, Phone, Email, Address)
VALUES 
    ('Tikam1', '123456789', 'tikam1@iiitd.ac.in', 'Hostel H1 IIIT delhi'),
    ('Tikam2', '123456789', 'tikam2@iiitd.ac.in', 'Hostel H1 IIIT delhi'),
    ('Tikam3', '123456789', 'tikam3@iiitd.ac.in', 'Hostel H1 IIIT delhi'),
    ('Tikam4', '123456789', 'tikam4@iiitd.ac.in', 'Hostel H1 IIIT delhi'),
    ('Tikam5', '123456789', 'tikam5@iiitd.ac.in', 'Hostel H1 IIIT delhi'),
    ('Tikam6', '123456789', 'tikam6@iiitd.ac.in', 'Hostel H1 IIIT delhi'),
    ('Tikam7', '123456789', 'tikam7@iiitd.ac.in', 'Hostel H1 IIIT delhi'),
    ('Tikam8', '123456789', 'tikam8@iiitd.ac.in', 'Hostel H1 IIIT delhi'),
    ('Tikam9', '123456789', 'tikam9@iiitd.ac.in', 'Hostel H1 IIIT delhi'),
    ('Tikam10', '123456789', 'tikam10@iiitd.ac.in', 'Hostel H1 IIIT delhi');


INSERT INTO Categories (Category_ID, Category_Name)
VALUES 
    (1, 'Shirt'),
    (2, 'T-Shirt'),
    (3, 'Jeans'),
    (4, 'Sweatshirts'),
    (5, 'Jackets'),
    (6, 'Innerwear'),
    (7, 'Shoes'),
    (8, 'Watches'),
    (9, 'Formal_Shirts'),
    (10, 'Formal Shoes');


INSERT INTO Product_Page (Product_ID, Product_Name, Product_price, Category_ID)
VALUES 
    (1, 'Gucci_Shirt', 50000, 1),
    (2, 'Gucci T-Shirt', 20000, 2),
    (3, 'Levi_Jeans', 3000, 3),
    (4, 'Roadster_Sweatshirts', 1000, 4),
    (5, 'Wrogn_Jackets', 3000, 5),
    (6, 'Jockey_Underwear', 500, 6),
    (7, 'Nike_Shoes', 10000, 7),
    (8, 'Rolex_Watch', 50000, 8),
    (9, 'Here&Now', 500, 9),
    (10, 'Bata', 10000, 10);


INSERT INTO Inventory (Product_Name, Quantity_Left)
VALUES 
    ('Gucci_Shirt', 100),
    ('Gucci T-Shirt', 100),
    ('Levi_Jeans', 100),
    ('Roadster_Sweatshirts', 100),
    ('Wrogn_Jackets', 100),
    ('Jockey_Underwear', 100),
    ('Nike_Shoes', 100),
    ('Rolex_Watch', 100),
    ('Here&Now', 100),
    ('Bata', 100);


INSERT INTO Cart_Item (Quantity, Total_Cost, Order_ID, Product_ID)
VALUES 
    (1, 50000, 1, 1),
    (2, 40000, 2, 2),
    (3, 9000, 3, 3),
    (4, 4000, 4, 4),
    (5, 3000, 5, 5),
    (1, 500, 6, 6),
    (2, 20000, 7, 7),
    (3, 150000, 8, 8),
    (4, 2000, 9, 9),
    (5, 50000, 10, 10);







INSERT INTO Payment (Payment_ID, Amount, Order_ID)
VALUES 
    (1, 50000, 1),
    (2, 40000, 2),
    (3, 9000, 3),
    (4, 4000, 4),
    (5, 3000, 5),
    (6, 500, 6),
    (7, 2000, 7),
    (8, 150000, 8),
    (9, 2000, 9),
    (10, 50000, 10);




INSERT INTO Tracking (Tracking_ID, Order_ID, Customer_Address, Delivery_Time)
VALUES 
    (1, 1, 'Hostel H1 IIIT delhi', '2 days'),
    (2, 2, 'Hostel H1 IIIT delhi', '2 days'),
    (3, 3, 'Hostel H1 IIIT delhi', '2 days'),
    (4, 4, 'Hostel H1 IIIT delhi', '2 days'),
    (5, 5, 'Hostel H1 IIIT delhi', '2 days'),
    (6, 6, 'Hostel H1 IIIT delhi', '2 days'),
    (7, 7, 'Hostel H1 IIIT delhi', '2 days'),
    (8, 8, 'Hostel H1 IIIT delhi', '2 days'),
    (9, 9, 'Hostel H1 IIIT delhi', '2 days'),
    (10, 10, 'Hostel H1 IIIT delhi', '2 days');

/*

