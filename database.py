import sqlite3
import Tkinter as tk
import ttk
import tkMessageBox
import time
import threading

# Connect to SQLite database
conn = sqlite3.connect('Zaiku_Fashion.db')
cursor = conn.cursor()


# Create triggers
create_update_last_login_trigger = """
CREATE TRIGGER IF NOT EXISTS update_last_login
AFTER UPDATE ON Customer_Account
FOR EACH ROW
WHEN NEW.Login_Status = 'Success'
BEGIN
    UPDATE Customer_Account
    SET Last_Login = DATETIME('now')
    WHERE Username = NEW.Username;
END;
"""

create_log_failed_login_trigger = """
CREATE TRIGGER IF NOT EXISTS log_failed_login
AFTER UPDATE ON Customer_Account
FOR EACH ROW
WHEN NEW.Login_Status = 'Failed'
BEGIN
    INSERT INTO Login_Attempts (Username, Attempt_Time)
    VALUES (NEW.Username, DATETIME('now'));
END;
"""

# Execute trigger creation commands
cursor.execute(create_update_last_login_trigger)
cursor.execute(create_log_failed_login_trigger)

# Define a global variable to store cart items
cart_items = []
cart_lock = threading.Lock()  # Lock to control access to cart_items


class SignUpPage(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.title("Sign Up")
        self.geometry("300x150")

        self.username_label = ttk.Label(self, text="Username:")
        self.username_entry = ttk.Entry(self)
        self.password_label = ttk.Label(self, text="Password:")
        self.password_entry = ttk.Entry(self, show="*")

        self.sign_up_button = ttk.Button(self, text="Sign Up", command=self.sign_up)

        self.username_label.pack()
        self.username_entry.pack()
        self.password_label.pack()
        self.password_entry.pack()
        self.sign_up_button.pack()

    def sign_up(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if username already exists
        cursor.execute("SELECT * FROM Customer_Account WHERE Username = ?", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            tkMessageBox.showerror("Error", "Username already exists. Please choose another one.")
        else:
            # Insert new user into the database
            cursor.execute("INSERT INTO Customer_Account (Username, Password) VALUES (?, ?)", (username, password))
            conn.commit()
            tkMessageBox.showinfo("Success", "Account created successfully!")
            self.destroy()
   


# Function to authenticate user login
login_failure_count = 0
def authenticate_user(username, password):
    global login_failure_count
    cursor.execute("SELECT * FROM Customer_Account WHERE Username = ? AND Password = ?", (username, password))
    user = cursor.fetchone()
    if user:
        login_failure_count = 0  # Reset login failure count on successful login
        return True
    else:
        # Introduce a delay to simulate concurrency
        time.sleep(2)
        login_failure_count += 1  # Increment login failure count
        if login_failure_count >= 3:
            tkMessageBox.showerror("Error", "Too many login failures. Your account has been blocked.")
            # You can implement further actions here like blocking the account in the database
        else:
            tkMessageBox.showerror("Error", "Invalid username or password. Login failures: {}".format(login_failure_count))
        return False

    
# Function to display categories
def display_categories():
    cursor.execute("SELECT * FROM Categories")
    categories = cursor.fetchall()
    return categories

# Function to display products in a category
def display_products(category_id):
    cursor.execute("SELECT * FROM Product_Page WHERE Category_ID = ?", (category_id,))
    products = cursor.fetchall()
    return products

# Function to add items to the cart
def add_to_cart(product_id, quantity):
    global cart_items
    # Fetch product details from the database based on product_id
    cursor.execute("SELECT * FROM Product_Page WHERE Product_ID = ?", (product_id,))
    product = cursor.fetchone()
    if product:
        # Calculate total cost for the item
        total_cost = product[2] * quantity
        # Add item to cart
        with cart_lock:
            # Introduce a delay to simulate a race condition
            time.sleep(1)
            cart_items.append({
                "Product_ID": product_id,
                "Product_Name": product[1],
                "Quantity": quantity,
                "Total_Cost": total_cost
            })
            tkMessageBox.showinfo("Success", "Added {} {} to cart.".format(quantity, product[1]))
    else:
        tkMessageBox.showerror("Error", "Product not found.")

# Function to display cart items
def display_cart(cart_text):
    cart_text.delete(1.0, tk.END)
    if cart_items:
        cart_text.insert(tk.END, "Cart Details:\n")
        for item in cart_items:
            cart_text.insert(tk.END, "Product ID: {}, Product Name: {}, Quantity: {}, Total Cost: {}\n".format(item['Product_ID'], item['Product_Name'], item['Quantity'], item['Total_Cost']))
        total_cart_price = sum(item['Total_Cost'] for item in cart_items)
        cart_text.insert(tk.END, "Total Cart Price: {}\n".format(total_cart_price))
        cart_text.insert(tk.END, "Items added to cart successfully!")
    else:
        cart_text.insert(tk.END, "Cart is empty.")


class TrackingPage(tk.Toplevel):
    def __init__(self, master, order_id):
        tk.Toplevel.__init__(self, master)
        self.title("Tracking Details")
        self.geometry("400x200")

        print("Order ID:", order_id)  # Debugging statement

        # Retrieve tracking details from the database based on order_id
        cursor.execute("SELECT * FROM Tracking WHERE Order_ID = ?", (order_id,))
        tracking_details = cursor.fetchone()

        print("Tracking Details:", tracking_details)  # Debugging statement

        # Display tracking details
        if tracking_details:
            ttk.Label(self, text="Tracking ID: {}".format(tracking_details[0])).pack()
            ttk.Label(self, text="Order ID: {}".format(tracking_details[1])).pack()
            ttk.Label(self, text="Customer Address: {}".format(tracking_details[2])).pack()
            ttk.Label(self, text="Delivery Time: {}".format(tracking_details[3])).pack()
        else:
            ttk.Label(self, text="Tracking details not found.").pack()


class PaymentPage(tk.Toplevel):
    def __init__(self, master, total_cost, order_id):
        tk.Toplevel.__init__(self, master)
        self.title("Payment")
        self.geometry("300x150")

        self.total_cost_label = ttk.Label(self, text="Total Cost: ${}".format(total_cost))
        self.pay_button = ttk.Button(self, text="Pay", command=lambda: self.process_payment(order_id))

        self.total_cost_label.pack()
        self.pay_button.pack()

    def process_payment(self, order_id):
        # Placeholder function for payment processing
        tkMessageBox.showinfo("Payment", "Payment successful!")
        self.destroy()
        # After payment, display the tracking page
        tracking_window = TrackingPage(self.master, order_id)


class ZaikuFashionApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Zaiku Fashion")
        self.geometry("400x300")

        # Create frames
        self.login_frame = tk.Frame(self)
        self.category_frame = tk.Frame(self)
        self.product_frame = tk.Frame(self)
        self.cart_frame = tk.Frame(self)

        # Labels for frames
        self.login_label = ttk.Label(self.login_frame, text="Welcome to Zaiku Fashion!")
        self.category_label = ttk.Label(self.category_frame, text="Category Page")
        self.product_label = ttk.Label(self.product_frame, text="Product Page")
        self.cart_label = ttk.Label(self.cart_frame, text="Cart Page")

        # Entry fields for username and password
        self.username_label = ttk.Label(self.login_frame, text="Username:")
        self.username_entry = ttk.Entry(self.login_frame)
        self.password_label = ttk.Label(self.login_frame, text="Password:")
        self.password_entry = ttk.Entry(self.login_frame, show="*")

        # Button to login
        self.login_button = ttk.Button(self.login_frame, text="Login", command=self.login)

        # Pack widgets for login frame
        self.login_label.pack()
        self.username_label.pack()
        self.username_entry.pack()
        self.password_label.pack()
        self.password_entry.pack()
        self.login_button.pack()

        # Create cart_text and pack it in cart_frame
        global cart_text
        cart_text = tk.Text(self.cart_frame, width=50, height=10)
        cart_text.pack()

        # Show login frame by default
        self.show_login_frame()

        # Create a sign-up button in the login frame
        self.sign_up_button = ttk.Button(self.login_frame, text="Sign Up", command=self.open_sign_up_page)
        self.sign_up_button.pack()

    def sign_up(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        cursor.execute("SELECT * FROM Customer_Account WHERE Username = ?", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            tkMessageBox.showerror("Error", "Username already exists. Please choose another one.")
        else:
        # Insert new user into the database
            cursor.execute("INSERT INTO Customer_Account (Username, Password) VALUES (?, ?)", (username, password))
            conn.commit()
            tkMessageBox.showinfo("Success", "Account created successfully!")
            
    def open_sign_up_page(self):
        sign_up_window = SignUpPage(self)


    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Authenticate user
        if authenticate_user(username, password):
            self.show_category_frame()
        else:
            tkMessageBox.showerror("Error", "Invalid username or password.")


    def show_login_frame(self):
        self.category_frame.pack_forget()
        self.product_frame.pack_forget()
        self.cart_frame.pack_forget()
        self.login_frame.pack()

    def show_login_frame(self):
        self.category_frame.pack_forget()
        self.product_frame.pack_forget()
        self.cart_frame.pack_forget()
        self.login_frame.pack()

    def show_category_frame(self):
        self.login_frame.pack_forget()
        self.product_frame.pack_forget()
        self.cart_frame.pack_forget()
        self.category_frame.pack()

        # Create entry for category ID
        self.category_id_entry = ttk.Entry(self.category_frame)
        self.category_id_entry.pack()
        self.select_category_button = ttk.Button(self.category_frame, text="Select Category", command=self.on_select_category)
        self.select_category_button.pack()

        # Fetch and display categories
        categories = display_categories()
        for category in categories:
            ttk.Label(self.category_frame, text="Category ID: {}, Category Name: {}".format(category[0], category[1])).pack()

        # Back button
        back_button = ttk.Button(self.category_frame, text="Back", command=self.show_login_frame)
        back_button.pack()

        # Display Inventory Button
        display_inventory_button = ttk.Button(self.category_frame, text="Display Inventory", command=self.display_inventory)
        display_inventory_button.pack()

    def on_select_category(self):
        category_id = int(self.category_id_entry.get())
        self.show_product_frame(category_id)


    def show_product_frame(self, category_id):
        self.login_frame.pack_forget()
        self.category_frame.pack_forget()
        self.cart_frame.pack_forget()
        self.product_frame.pack()

        # Create labels and entry fields for product ID and quantity
        ttk.Label(self.product_frame, text="Product ID:").pack()
        self.product_id_entry = ttk.Entry(self.product_frame)
        self.product_id_entry.pack()

        ttk.Label(self.product_frame, text="Quantity:").pack()
        self.quantity_entry = ttk.Entry(self.product_frame)
        self.quantity_entry.pack()

        # Fetch and display products in the selected category
        products = display_products(category_id)
        for product in products:
            ttk.Label(self.product_frame, text="Product ID: {}, Product Name: {}, Price: {}".format(product[0], product[1], product[2])).pack()

        # Button to add product to cart
        add_to_cart_button = ttk.Button(self.product_frame, text="Add to Cart", command=self.add_product_to_cart)
        add_to_cart_button.pack()

        # Back button
        back_button = ttk.Button(self.product_frame, text="Back", command=self.show_category_frame)
        back_button.pack()

    def add_product_to_cart(self):
        product_id = int(self.product_id_entry.get())
        quantity = int(self.quantity_entry.get())
        add_to_cart(product_id, quantity)
        display_cart(cart_text)
        # Display message box with options to view cart or continue shopping
        response = tkMessageBox.askyesno("Success", "Item added to cart. View cart now?")
        if response:
            self.show_cart_frame()  # Show cart frame if user chooses to view cart
        else:
            # Reset entry fields for adding another item
            self.product_id_entry.delete(0, tk.END)
            self.quantity_entry.delete(0, tk.END)


    def show_cart_frame(self):
        self.login_frame.pack_forget()
        self.category_frame.pack_forget()
        self.product_frame.pack_forget()
        self.cart_frame.pack()

        cart_text.delete(1.0, tk.END)  # Clear the cart text widget
        display_cart(cart_text)  # Display cart details

        # Button to place the order
        place_order_button = ttk.Button(self.cart_frame, text="Place Order", command=self.place_order)
        place_order_button.pack()

        # Back button
        back_button = ttk.Button(self.cart_frame, text="Back", command=self.show_product_frame)
        back_button.pack()

        # Home button
        home_button = ttk.Button(self.cart_frame, text="Home", command=self.show_category_frame)
        home_button.pack()

        # Display Inventory Button
        display_inventory_button = ttk.Button(self.cart_frame, text="Display Inventory", command=self.display_inventory)
        display_inventory_button.pack()


    def display_inventory(self):
        # Retrieve inventory from the database
        cursor.execute("SELECT Product_Name, Quantity_Left FROM Inventory")
        inventory = cursor.fetchall()

        # Create a new window to display inventory
        inventory_window = tk.Toplevel(self)
        inventory_window.title("Inventory")
        inventory_window.geometry("300x200")

        # Display inventory in a text widget
        inventory_text = tk.Text(inventory_window, width=30, height=10)
        inventory_text.pack()

        # Insert inventory data into the text widget
        inventory_text.insert(tk.END, "Inventory:\n")
        for item in inventory:
            inventory_text.insert(tk.END, "Product Name: {}, Quantity Left: {}\n".format(item[0], item[1]))

    def place_order(self):
        global cart_items
        total_cart_price = sum(item['Total_Cost'] for item in cart_items)

    # Placeholder for generating order ID (You can replace this with your actual logic)
        order_id = 1

    # Display payment page
        payment_window = PaymentPage(self, total_cart_price, order_id)

    # Further processing of the order can be done here after payment
        self.process_order(cart_items, total_cart_price)


    def process_order(self, cart_items, total_cart_price):
        # Placeholder function to process the order
        print("Processing Order...")
        print("Order Details:")
        for item in cart_items:
            print("Product ID: {}, Product Name: {}, Quantity: {}, Total Cost: {}".format(item['Product_ID'], item['Product_Name'], item['Quantity'], item['Total_Cost']))
        
        # Placeholder for updating inventory quantity
        print("Updating inventory...")

        print("Total Cart Price: {}".format(total_cart_price))
        # Here you can add further processing such as sending confirmation emails, etc.
        print("Order processed successfully!")
        
def main():
    app = ZaikuFashionApp()
    app.mainloop()

if __name__ == "__main__":
    main()
