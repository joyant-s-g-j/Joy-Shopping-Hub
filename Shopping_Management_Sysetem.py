from abc import ABC
from datetime import datetime
class Product:
    def __init__(self,name,id,category,price,quantity):
        self.name = name
        self.id = id
        self.category = category
        self.price = price
        self.quantity = quantity

class User(ABC):
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class Seller(User):
    def __init__(self, name, email, password):
        super().__init__(name, email, password)

    def view_products(self, shop):
        shop.show_products()
    
    def remove_product(self, shop, product_name, product_id):
        if product_id:
            shop.remove_product(product_name,product_id)
        else:
            print("\n\tProduct is not found")
                 
class Customer(User):
    def __init__(self, name, email, password):
        super().__init__(name, email, password)
        self.pay_bill_time = {}

    def view_products(self, shop):
        shop.show_products()
    
    def quantity_reduce(self,shop):
        for cart_product in shop.prdct:
            shop_product = shop.find_product(cart_product.name, cart_product.id)
            if shop_product:
                if shop_product.quantity >= cart_product.quantity:
                    shop_product.quantity -= cart_product.quantity

    def remove_from_cart(self,shop, product_name, product_id):
        remove_product = shop.remove_product_from_cart(product_name,product_id)
        if remove_product:
            product = Joy_City_Center.find_product(product_name,product_id)
            print(f"\tProduct '{product.name}' with id '{product.id}' removed from the cart")
        else:
            print(f"\tProduct '{product.name}' with id '{product.id}' not found in the cart")

    def pay_bill(self,shop):
        if not shop.prdct:
            print("\tCart is empty.Please add any product on cart")
        else:
            total = shop.total_price()
            current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            Joy_City_Center.add_order(shop.prdct,current_time)
            self.pay_bill_time[total] = current_time
            self.quantity_reduce(Joy_City_Center)
            print(f"Total {total} Paid Successfully")
            shop.clear()

class Admin(User):
    def __init__(self, name, email, password):
        super().__init__(name, email, password)

    def remove_product(self, shop, product_name, product_id):
        if product_name and product_id:
            shop.remove_product(product_name, product_id)
        else:
            print("\n\tProduct is not found")
    
    def add_seller(self, shop, seller):
        shop.add_seller(seller)

    def show_sellers(self, shop):
        shop.show_sellers()

class Shop:
    def __init__(self, name):
        self.name = name
        self.products = []
        self.customers = []
        self.sellers = []
        self.users = []
        self.orders = []
        self.orders_times = {}
        self.prdct = {}
    
    def remove_product_from_cart(self, product_name, product_id):
        for product,quantity in self.prdct.items():
            if product.name == product_name and product.id == product_id:
                removed_product = Product(product.name, product.id, product.category, product.price, quantity)
                del self.prdct[product]
                return removed_product
        return None
    
    def total_price(self):
        return sum(product.price * quantity for product, quantity in self.prdct.items())
    
    def clear(self):
        self.prdct = {}

    def add_order(self, order, order_time):
        self.orders.append(order)
        self.orders_times[order_time] = order

    def find_product(self, product_name,product_id):
        if not self.products:
            print("\tProduct list is empty")
            return
        else:
            for product in self.products:
                if product.name == product_name and product.id == product_id:
                    return product
            return None
    def add_product_to_cart(self, product):
        if product in self.products:
            self.prdct[product] += product.quantity
        else:
            self.prdct[product] = product.quantity
    
    def view_cart(self):
        if not self.prdct:
            print("\tCart is empty")
        else:
            print("\t*****View Cart****")
            print("\tName\tPrice\tQuantity")
            for product, quantity in self.prdct.items():
                print(f"\t{product.name}\t{product.price}\t{quantity}")
            print(f"\tTotal Price: {self.total_price()}")

    def add_to_cart(self,product_name, product_id, quantity):
        product = self.find_product(product_name,product_id)
        if product:
            if quantity > product.quantity:
                print("\tProduct Quantity Exceed")
            else:
                product_in_cart = Product(product.name, product.id, product.category, product.price, quantity)
                self.add_product_to_cart(product_in_cart)
                print(f"\t{product_name.capitalize()} added to the cart")
        else:
            print(f"\t{product_name} not found in the shop")

    def remove_product(self, product_name, product_id):
        product = self.find_product(product_name,product_id)
        if product:
            self.products.remove(product)
            print(f"\t'{product_name}' with '{product_id}'removed from the product list")
        else:
            print(f"\t{product_name.capitalize()} with '{product_id}' is not found on the product list")

    def view_order_history(self):
        if self.orders == []:
            print("\tOrder list is empty")
        else:
            if self.orders:
                for order in self.orders:
                    for product, quantity in order.items():
                        order_time = next(key for key, value in self.orders_times.items() if value == order)
                        print(f"\tProduct: {product.name},\n\t Quantity: {quantity},\n\t Total: {product.price*quantity},\n\t Order time: {order_time}")
    
    def add_user(self, name, email, password):
        user = Admin(name, email, password)
        self.users.append(user)

    def add_product(self, name, id, category,price, quantity):
        product = Product(name, id, category, price, quantity)
        self.products.append(product)
        print(f"\n\t{name.capitalize()} added as a product")
    
    def show_products(self):
        if not self.products:
            print("\tNo products available")
            return
        print("\tProduct list")
        for product in self.products:
            print(f"\tProduct Name: {product.name}")
            print(f"\tProduct id: {product.id}")
            print(f"\tCategory: {product.category}")
            print(f"\tPrice: {product.price}")
            print(f"\tQuantity: {product.quantity}\n")

    def add_customer(self, name, email, password):
        customer = Customer(name, email, password)
        self.customers.append(customer)

    def show_customers(self):
        if self.customers == []:
            print("\n\tThere are no customer")
        else:
            print("\nCustomer List")
            for customer in self.customers:
                print(f"\tCustomer Name: {customer.name}")
                print(f"\tCustomer Email: {customer.email}")
    
    def add_seller(self, name, email, password):
        seller = Seller(name, email, password)
        self.sellers.append(seller)

    def show_sellers(self):
        if self.sellers == []:
            print("\n\tThere are no seller")
        else:
            print("Seller List")
            for slr in self.sellers:
                print(f"\tSeller Name: {slr.name}")
                print(f"\tSeller email: {slr.email}")
    
    def update_product_info(self):
        if self.products == []:
            print("\tProduct list is empty")
            return
        while True:
            try:
                product_id = int(input("Enter the product id: "))
            except ValueError:
                print("\tInvalid value.Please enter an integer value")
                continue

            product_found = False
            for product in self.products:
                if product.id == product_id:
                    product_found = True
                    break
            
            if not product_found:
                print(f"\tNo product found with id {product_id}")
                return
            while True:
                print("\nSelect option which information want to you update")
                print("1 : Product name")
                print("2 : Product id")
                print("3 : Product category")
                print("4 : Product price")
                print("5 : Product quantity")
                print("6 : Back")
                try:
                    option = int(input("Enter your option: "))
                except ValueError:
                    print("\tInvalid value.Please enter an integer value")
                    continue
                if option == 1:
                    old_name = input("Enter the current product name: ")
                    if not old_name.isalpha():
                        print("\tInvalid value.Please enter alphabetic characters only")
                        continue
                    new_name = input("Enter the new product name: ")
                    if not new_name.isalpha():
                        print("\tInvalid value.Please enter alphabetic characters only")
                        continue
                    for product in self.products:
                        if product.name == old_name:
                            product.name = new_name
                            print("\tProduct name successfully updated")
                            break
                        else:
                            print("\tProduct old name is not matched")
                elif option == 2:
                    try:
                        old_id = int(input("Enter the old product id: "))
                    except ValueError:
                        print("\tInvalid value.Please enter an integer value")
                        continue
                    try:
                        new_id = int(input("Enter the old product id: "))
                    except ValueError:
                        print("\tInvalid value.Please enter an integer value")
                        continue
                    for product in self.products:
                        if product.id == old_id:
                            product.id = new_id
                            print("\tProduct id successfully updated")
                            break
                        else:
                            print("\tProduct old id is not matched")
                elif option == 3:
                    old_category = input("Enter the old product category: ")
                    if not old_category.isalpha():
                        print("\tInvalid value.Please enter alphabetic characters only")
                        continue
                    new_category = input("Enter the new product category: ")
                    if not new_category.isalpha():
                        print("\tInvalid value.Please enter alphabetic characters only")
                        continue
                    for product in self.products:
                        if product.category == old_category:
                            product.category = new_category
                            print("\tProduct category successfully updated")
                            break
                        else:
                            print("\tProduct old category is not matched")
                elif option == 4:
                    try:
                        old_price = float(input("Enter the old product price: "))
                    except ValueError:
                        print("\tInvalid value.Please enter an float value")
                        continue
                    try:
                        new_price = float(input("Enter the new product price: "))
                    except ValueError:
                        print("\tInvalid value.Please enter an integer value")
                        continue
                    for product in self.products:
                        if product.price == old_price:
                            product.price = new_price
                            print("\tProduct price successfully updated")
                            break
                        else:
                            print("\tProduct old price is not matched")
                elif option == 5:
                    try:
                        old_quantity = int(input("Enter the old product quantity: "))
                    except ValueError:
                        print("\tInvalid value.Please enter an integer value")
                        continue
                    try:
                        new_quantity = int(input("Enter the new product quantity: "))
                    except ValueError:
                        print("\tInvalid value.Please enter an integer value")
                        continue
                    for product in self.products:
                        if product.quantity == old_quantity:
                            product.quantity = new_quantity
                            print("\tProduct quantity successfully updated")
                            break
                        else:
                            print("\tProduct old quantity is not matched")
                elif option == 6:
                    return
                else:
                    print("\tInvalid option")

Joy_City_Center = Shop('Joy City Center')
customer = Joy_City_Center.add_customer('nupur','nupur@gmail.com','1234')

def customer_menu():
    while True:
        print("\nOptions: ")
        print("1 : Registration")
        print("2 : Login")
        print("3 : Exit")
        try:
            option = int(input("Enter the option: "))
        except ValueError:
            print("\tInvalid value.Please enter an integer value")
            continue
        if option == 1:
            name = input("\nEnter your name: ")
            if not name.isalpha():
                print("\tInvalid value.Please enter alphabetic characters only")
                continue
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            customer = Customer(name=name, email=email, password=password)
            Joy_City_Center.add_customer(name, email, password)
            print(f"\t{name.capitalize()}, your registration completed. Now you can login as a customer")
            continue
        elif option == 2:
            name = input("Enter your name: ")
            if not name.isalpha():
                print("\tInvalid value.Please enter alphabetic characters only")
                continue
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            match = False
            for user in Joy_City_Center.customers:
                if user.email == email and user.password == password:
                    match = True
                    break
            if match == False:
                print("\n\tNo user found")
                while True:
                    option = input("Are you want to continue or back? (C/B): ")
                    if option == 'C' or option == 'c':
                        break
                    elif option == 'B' or option == 'b':
                        return
                    else:
                        print(f"\t'{option}' is an invalid command")
                continue
            customer = Customer(name=name, email=email, password=password)
            while True:
                print(f"\nWelcome {name.capitalize()}")
                print("1 : View Product")
                print("2 : Add product to cart")
                print("3 : View cart")
                print("4 : Remove from cart")
                print("5 : Pay Bill")
                print("6 : Exit")
                try:
                    option = int(input("Enter option: "))
                except ValueError:
                    print("\tInvalid value. Please enter an integer value")
                    while True:
                        option = input("Are you want to continue or back? (C/B): ")
                        if option == 'C' or option == 'c':
                            break
                        elif option == 'B' or option == 'b':
                            return
                        else:
                            print(f"\t'{option}' is an invalid command")
                    continue
                if option == 1:
                    customer.view_products(Joy_City_Center)
                elif option == 2:
                    product_name = input("Enter the product name: ")
                    if not product_name.isalpha():
                        print("\tInvalid value.Please enter alphabetic characters only")
                        continue
                    try:
                        product_id = int(input("Enter the product id: "))
                    except ValueError:
                        print("\tInvalid value. Please enter an integer value")
                        continue
                    try:
                        quantity = int(input("Enter the product quantity: "))
                    except ValueError:
                        print("\tInvalid value. Please enter an integer value")
                        continue
                    Joy_City_Center.add_to_cart(product_name,product_id, quantity)
                elif option == 3:
                    Joy_City_Center.view_cart()
                elif option == 4:
                    if Joy_City_Center.prdct == {}:
                        print("\tProduct cart is empty")
                        continue
                    else:
                        product_name = input("Enter the product name: ")
                        try:
                            product_id = int(input("Enter the product id: "))
                        except ValueError:
                            print("\tInvalid value. Please enter an integer value")
                            continue
                        customer.remove_from_cart(Joy_City_Center,product_name,product_id)
                elif option == 5:
                    customer.pay_bill(Joy_City_Center)
                elif option == 6:
                    break
                else:
                    print("\tInvalid input")
        elif option == 3:
            return
        else:
            print("\tInvalid Option")

seller = Joy_City_Center.add_seller('sheikhar', 'sheikhar@gmail.com', '1111')
cur_user = seller
def seller_menu():
    while True:
        print("\nOption: ")
        print("1 : Registration")
        print("2 : Login")
        print("3 : Exit")
        try:
            option = int(input("Enter the option: "))
        except ValueError:
            print("\tInvalid value. Please enter an integer value")
            continue
        if option == 1:
            name = input("Enter your name: ")
            if not name.isalpha():
                print("\tInvalid value.Please enter alphabetic characters only")
                continue
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            seller = Seller(name=name, email=email, password=password)
            Joy_City_Center.add_seller(name,email,password)
            print(f"\t{name.capitalize()}, your registration completed. Now you can login as a seller")
            continue
        elif option == 2:
            name = input("Enter your name: ")
            if not name.isalpha():
                print("\tInvalid value.Please enter alphabetic characters only")
                continue
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            match = False
            for user in Joy_City_Center.sellers:
                if user.email == email and user.password == password:
                    cur_user = user
                    match = True
                    break
            if match == False:
                print("\n\tNo user found")
                while True:
                    option = input("Are you want to continue or back? (C/B): ")
                    if option == 'C' or option == 'c':
                        break
                    elif option == 'B' or option == 'b':
                        return
                    else:
                        print(f"\t'{option}' is an invalid command")
                continue
            seller = Seller(name=name, email=email, password=password)
            while True:
                print(f"\nWelcome {cur_user.name}")
                print("1 : Add Product")
                print("2 : View Product")
                print("3 : Update Product")
                print("4 : Remove Product")
                print("5 : View Orders")
                print("6 : Logout")
                try:
                    option = int(input("Enter option: "))
                except ValueError:
                    print("\tInvalid value. Please enter an integer value")
                    continue
                if option == 1:
                    name = input("Enter the product name: ")
                    if not name.isalpha():
                        print("\tInvalid value.Please enter alphabetic characters only")
                        continue
                    try:
                        id = int(input("Enter the product id: "))
                    except ValueError:
                        print("\tInvalid value. Please enter an integer value")
                        continue
                    category = input("Enter the product category: ")
                    if not category.isalpha():
                        print("\tInvalid value.Please enter alphabetic characters only")
                        continue
                    try:
                        price = float(input("Enter the product price: "))
                    except ValueError:
                        print("\tInvalid value. Please enter an integer value")
                        continue
                    try:
                        quantity = int(input("Enter the product quantity: "))
                    except ValueError:
                        print("\tInvalid value. Please enter an integer value")
                        continue
                    Joy_City_Center.add_product(name, id, category, price, quantity)
                elif option == 2:
                    seller.view_products(Joy_City_Center)                    
                elif option == 3:
                    Joy_City_Center.update_product_info()
                elif option == 4:
                    if Joy_City_Center.products == []:
                        print("\tProduct list is empty. No product is available for remove")
                        continue
                    else:
                        product_name = input("Enter the product name: ")
                        try:
                            product_id = int(input("Enter the product id: "))
                        except ValueError:
                            print("\tInvalid value. Please enter an integer value")
                            continue
                        seller.remove_product(Joy_City_Center, product_name, product_id)
                elif option == 5:
                    Joy_City_Center.view_order_history()
                elif option == 6:
                    break
                else:
                    print("\tInvalid Input")
        elif option == 3:
            return
        else:
            print("\tInvalid value")

admin = Joy_City_Center.add_user('Joy', 'joyantogupto4@gmail.com', 'admin')
cur_user = admin
def admin_menu():
    while True:
        print("\nPlease Login")
        name = input("Enter the name: ")
        if not name.isalpha():
            print("\tInvalid value.Please enter alphabetic characters only")
            continue
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        match = False
        for user in Joy_City_Center.users:
            if user.email == email and user.password == password:
                cur_user = user
                match = True
                admin = Admin(name=name, email=email, password=password)
                break
        if match == False:
            print("\tNo user found")
            while True:
                option = input("Are you want to continue or back? (C/B): ")
                if option == 'C' or option == 'c':
                    break
                elif option == 'B' or option == 'b':
                    return
                else:
                    print(f"\t'{option}' is an invalid command")
            continue
        
        while True:
            print(f"\nWelcome {cur_user.name}")
            print("Options")
            print("1 : Add Product")
            print("2 : Show Products")
            print("3 : Show Customers")
            print("4 : Show Sellers")
            print("5 : Update Products")
            print("6 : Remove Product")
            print("7 : Logout")
            try:
                option = int(input("\nEnter Option: "))
            except ValueError:
                print("\tInvalid value. Please enter an integer value")
                continue
            if option == 1:
                name = input("Enter the product name: ")
                if not name.isalpha():
                    print("\tInvalid value.Please enter alphabetic characters only")
                    continue
                try:
                    id = int(input("Enter the product id: "))
                except ValueError:
                    print("\tInvalid value. Please enter an integer value")
                    continue
                category = input("Enter the product category: ")
                if not category.isalpha():
                    print("\tInvalid value.Please enter alphabetic characters only")
                    continue
                try:
                    price = float(input("Enter the product price: "))
                except ValueError:
                    print("\tInvalid value. Please enter an float value")
                    continue
                try:
                    quantity = int(input("Enter the product quantity: "))
                except ValueError:
                    print("\tInvalid value. Please enter an integer value")
                    continue
                Joy_City_Center.add_product(name, id, category, price, quantity)
            elif option == 2:
                Joy_City_Center.show_products()
            elif option == 3:
                Joy_City_Center.show_customers()
            elif option == 4:
                admin.show_sellers(Joy_City_Center)
            elif option == 5:
                Joy_City_Center.update_product_info()
            elif option == 6:
                if Joy_City_Center.products == []:
                    print("\tProduct list is empty. No product is available for remove")
                    continue
                else:
                    product_name = input("Enter the product name: ")
                    try:
                        product_id = int(input("Enter the product id: "))
                    except ValueError:
                        print("\tInvalid value. Please enter an integer value")
                        continue
                    admin.remove_product(Joy_City_Center,product_name, product_id)
            elif option == 7:
                return
            else:
                print("\tInvalid value")

import os
def clear_screen():
    os.system('cls')
clear_screen()
while True:
    if cur_user == None:
        print("""\t\t\t
           *********************************
           *                               *
           *  Welcome to Joy Shopping Hub  *
           *                               *
           *********************************
            \n""")
        option = input("Use this as a Customer or Seller or Admin or Exit (C/S/A/E): ")
        if option == 'C' or option == 'c':
            customer_menu()
        elif option == 'A' or option == 'a':
            admin_menu()
        elif option == 'S' or option == 's':
            seller_menu()
        elif option == 'E' or option == 'e':
            print("\n\tExiting the system. Have a nice day!")
            break
        else:
            print("Invalid Input")