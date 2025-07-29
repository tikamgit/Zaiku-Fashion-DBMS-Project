import sqlite3
import uuid
from builtins import input

# Connect to SQLite database
conn = sqlite3.connect('Zaiku_Fashion.db')
cursor = conn.cursor()

# Function to authenticate user login
def authenticate_user(username, password):
    cursor.execute("SELECT * FROM Customer_Account WHERE Username = ? AND Password = ?", (username, password))
    user = cursor.fetchone()
    if user:
        return True
    else:
        return False

# Function to display categories
def display_categories():
    cursor.execute("SELECT * FROM Categories")
    categories = cursor.fetchall()
    print("Categories:")
    for category in categories:
        print(f"{category[0]}. {category[1]}")

# Function to display products in a category
def display_products(category_id):
    cursor.execute("SELECT * FROM Product_Page WHERE Category_ID = ?", (category_id,))
    products = cursor.fetchall()
    print("Products:")
    for product in products:
        print(f"{product[0]}. {product[1]} - Price: {product[2]}")

# Function to generate order ID
def generate_order_id():
    return str(uuid.uuid4())

# Main function
def main():
    # Define cart_items_list to store cart items
    cart_items_list = []

    # User login
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")
        if authenticate_user(username, password):
            print("Login successful!")
            break
        else:
            print("Invalid username or password. Please try again.")

    # Display categories
    display_categories()

    # Choose category
    while True:
        try:
            category_id = int(input("Enter the number of the category you want: "))
            if category_id >= 1 and category_id <= 10:
                break
            else:
                print("Invalid category number. Please choose a valid category.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Display products in the chosen category
    display_products(category_id)

    # Generate unique order ID
    order_id = generate_order_id()

    # Function to add items to the cart
    def add_to_cart(order_id):
        while True:
            try:
                product_id = int(input("Enter the product ID (0 to finish): "))
                if product_id == 0:
                   break
                quantity = int(input("Enter the quantity: "))

                # Retrieve product details from the database based on product_id
                cursor.execute("SELECT Product_Name, Product_price FROM Product_Page WHERE Product_ID = ?", (product_id,))
                product_data = cursor.fetchone()

                if product_data:
                    product_name, product_price = product_data
                    total_price = product_price * quantity
                
                item = {
                    "product_id": product_id,
                    "product_name": product_name,
                    "quantity": quantity,
                    "total_price": total_price
                }

                # Add the item to the cart_items_list
                cart_items_list.append(item)

                print("Product added to cart!")
            except ValueError:
                print("Invalid input. Please enter valid product ID and quantity.")

    # Function to display cart items and total cart price
    def display_cart(order_id):
        total_price = 0
        print("Cart Items:")
        for item in cart_items_list:
            product_name = item["product_name"]
            quantity = item["quantity"]
            total_item_price = item["total_price"]
            total_price += total_item_price
            print(f"Product: {product_name}, Quantity: {quantity}, Total Price: {total_item_price}")
        print("Total Cart Price:", total_price)

    # Add products to cart
    add_to_cart(order_id)

    # Display cart items and total cart price
    display_cart(order_id)

    # Close database connection
    conn.close()

if __name__ == "__main__":
    main()