import scraper
import datetime
import sqlite3
import smtplib,os
from email.message import EmailMessage
conn = sqlite3.connect("amazon_products_data.db",isolation_level=None)
conn.execute('PRAGMA foreign_keys=ON')
conn.execute("CREATE TABLE IF NOT EXISTS products(product_id INTEGER PRIMARY KEY,product_name TEXT,product_url TEXT)STRICT")
conn.execute("CREATE TABLE IF NOT EXISTS prices(product_id INTEGER,price TEXT,timestamp TEXT,FOREIGN KEY(product_id) REFERENCES products(product_id))STRICT")
conn.execute("CREATE TABLE IF NOT EXISTS categories(category_id INTEGER PRIMARY KEY,category_name TEXT)STRICT")
conn.execute("CREATE TABLE IF NOT EXISTS product_categories(product_id INT ,category_id INT,FOREIGN KEY(product_id) REFERENCES products(product_id),FOREIGN KEY(category_id) REFERENCES categories(category_id))STRICT")
try :
    conn.execute("ALTER products ADD COLUMN THRESHOLD DEFAULT None")
except sqlite3.OperationalError :
    pass
def add_product():
    product_name = None
    while (product_name==None):
        product_name = input("enter product name:")
    product_url = None
    while (product_url==None):
        product_url = input("enter product url:")
    while (threshold==None):
        threshold = input("enter product threshold:")
    conn.execute("INSERT INTO PRODUCTS (product_name,product_url,threshold) VALUES(?,?,?)",(product_name,product_url,threshold))
def show_products():
    products = conn.execute("SELECT product_id,product_name FROM PRODUCTS").fetchall()
    print("\nPRODUCTS")
    for product in products:
        print(f"{product[0]}.",product[1])
def check_threshold(product_name,price):
    price_whole = int(price.replace("₹", "").replace(",", "")[0:-3])
    threshold_e = conn.execute("SELECT threshold FROM PRODUCTS WHERE product_name=?",(product_name,)).fetchone()[0]
    threshold = int(threshold_e.replace("₹","").replace(",",""))
    if price_whole < threshold :
        send_mail(product_name,price,threshold_e)

def price_of_single_product():
    product_name = input("enter product name:")
    product_id = conn.execute("SELECT product_id FROM PRODUCTS WHERE product_name = ?",[product_name]).fetchone()
    url = conn.execute("SELECT product_url FROM PRODUCTS WHERE product_name = ?",[product_name]).fetchone()
    if url[0] is None:
        print("no such product")
    else:
        price = scraper.fetch_price(url[0])
        print(f"{product_name} {price}")
    time_now = datetime.datetime.now()
    formated_time = datetime.datetime.strftime(time_now,"%d/%m/%Y %H:%M:%S")
    conn.execute("INSERT INTO PRICES VALUES(?,?,?)",(product_id[0],price,formated_time))
    check_threshold(product_name,price)


def delete_product():
    product_name = input("enter product name:")
    conn.execute("DELETE FROM PRODUCTS WHERE product_name = ?",(product_name,))
    print("product deleted from the data base")

def price_of_all_products():
    data = conn.execute("SELECT product_id,product_url,product_name FROM PRODUCTS").fetchall()
    for i in data :
        product_id = i[0]
        product_url = i[1]
        price = scraper.fetch_price(product_url)
        print(i[2])
        print(price)
        time_now = datetime.datetime.now()
        formated_time = datetime.datetime.strftime(time_now,"%d/%m/%Y %H:%M:%S")
        conn.execute("INSERT INTO PRICES VALUES(?,?,?)",(product_id,price,formated_time))
        check_threshold(i[2],price)

def tracking_history():
    product_ids = conn.execute("SELECT product_id,product_name FROM PRODUCTS").fetchall()
    for i in product_ids:
        product_id = i[0]
        product_name = i[1]
        data = conn.execute("SELECT PRICE,TIMESTAMP FROM PRICES WHERE PRODUCT_ID=?",[product_id]).fetchall()
        for tuple in data :
            print(product_name,tuple[1],tuple[0])
def show_categories():
    category_name = conn.execute("SELECT category_id,category_name FROM categories").fetchall()
    print("\nCATEGORIES")
    for category in category_name:
        print(f"{category[0]}.",category[1])
def send_mail(product_name,price,threshold):
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    password = os.getenv("gmailapppassword")
    server.login("fakejithu07@gmail.com",password)
    msg = EmailMessage()
    msg["from"] = "fakejithu07@gmail.com"
    msg["to"] = "jithendrameruga@gmail.com"
    msg["subject"] = "product price fluctuated"
    msg.set_content(f"price drop.{product_name}'s price has droped to {price} , the threshold you have set is {threshold}")
    server.send_message(msg)
    server.quit()

def show_threshold():
    products = conn.execute("SELECT product_id,product_name,threshold FROM PRODUCTS").fetchall()
    print("\nPRODUCTS")
    print("no product_name     threshold")
    for product in products:
        print(f"{product[0]}.",product[1],f"     ({product[2]})")
while (True):
    print("\nMAIN MENU")
    choice = input("1.add product\n2.show all products \n3.price of product\n4.delete product\n5.price of all products" \
    "\n6.tracking history\n7.create category\n8.show categories\n9.add product to category\n10.delete category\n" \
    "11.show products based on category\n12.fetch price for category\n13.send mail\n14.update threshold\n15.exit\nEnter choice:")
    match choice:
        case "1":
            add_product()
        case "2": 
            show_products()
        case "3":
            price_of_single_product()
        case "4":
            delete_product()
        case "5":
            price_of_all_products()
        case "6":
            tracking_history()
        case "7":
            category_name = input("enter category name:")
            conn.execute("INSERT INTO CATEGORIES (category_name) VALUES(?)",(category_name,))
        case "8":
            show_categories()
        case "9":
            show_products()
            show_categories()
            tuple = input("enter product id first in format 1,2:").strip()
            conn.execute("INSERT INTO product_categories VALUES(?,?)",(tuple[0],tuple[-1]))
        case "10":
            category_name = input("enter category name:")
            conn.execute("DELETE FROM categories WHERE category_name = ?",(category_name,))
            print("category deleted from the data base")
        case "11":
            categories = conn.execute("SELECT * FROM categories").fetchall()
            for category in categories:
                print("\n",category[1])
                products = conn.execute("SELECT product_name FROM products p JOIN product_categories pc ON p.product_id = pc.product_id JOIN categories c ON pc.category_id = c.category_id WHERE category_name = ?",(category[1],)).fetchall()
                for i,product in enumerate(products):
                    print(f"{i+1}.",product[0])
        case "12":
            category_name = input("enter category name:")
            products = conn.execute("SELECT product_name FROM products p JOIN product_categories pc ON p.product_id = pc.product_id JOIN categories c ON pc.category_id = c.category_id WHERE category_name = ?",(category_name,)).fetchall()
            print(products)
            for product in products:
                data = conn.execute("SELECT product_id,product_url FROM PRODUCTS WHERE product_name=?",(product[0],)).fetchall()[0]
                product_id = data[0]
                product_url = data[1]
                price = scraper.fetch_price(product_url)
                print(product[0])
                print(price)
                time_now = datetime.datetime.now()
                formated_time = datetime.datetime.strftime(time_now,"%d/%m/%Y %H:%M:%S")
                conn.execute("INSERT INTO PRICES (product_id, price, timestamp) VALUES(?,?,?)",(product_id,price,formated_time))
                check_threshold(product[0],price)
        case "13":
            send_mail()
        case "14":
            show_threshold()
            product_name = input("enter product name:")
            threshold = input("enter threshold (ex:1,23,300):")
            conn.execute("UPDATE PRODUCTS SET threshold = ? WHERE product_name =?",(threshold,product_name))
            
        case "15":
            print("quitting program")
            break