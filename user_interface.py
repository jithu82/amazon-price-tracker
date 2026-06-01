import scraper
import datetime
import sqlite3
conn = sqlite3.connect("amazon_products_data.db",isolation_level=None)
conn.execute("CREATE TABLE IF NOT EXISTS products(product_name TEXT,product_url TEXT)STRICT")
conn.execute("CREATE TABLE IF NOT EXISTS prices(product_id INTEGER,price TEXT,timestamp TEXT,FOREIGN KEY(product_id) REFERENCES products(rowid))STRICT")
def add_product():
    product_name = None
    while (product_name==None):
        product_name = input("enter product name:")
    product_url = None
    while (product_url==None):
        product_url = input("enter product url:")
    conn.execute("INSERT INTO PRODUCTS VALUES(?,?)",(product_name,product_url))
def show_products():
    products = conn.execute("SELECT product_name FROM PRODUCTS").fetchall()
    for i,product in enumerate(products):
        print(f"{i+1}.",product[0])
def price_of_single_product():
    product_name = input("enter product name:")
    row_id = conn.execute("SELECT rowid FROM PRODUCTS WHERE product_name = ?",[product_name]).fetchone()
    url = conn.execute("SELECT product_url FROM PRODUCTS WHERE product_name = ?",[product_name]).fetchone()
    if url[0] is None:
        print("no such product")
    else:
        price = scraper.fetch_price(url[0])
        print(f"{product_name} {price}")
    time_now = datetime.datetime.now()
    formated_time = datetime.datetime.strftime(time_now,"%d/%m/%Y %H:%M:%S")
    conn.execute("INSERT INTO PRICES VALUES(?,?,?)",(row_id[0],price,formated_time))

def delete_product():
    product_name = input("enter product name:")
    conn.execute("DELETE FROM PRODUCTS WHERE product_name = ?",(product_name,))
    print("product deleted from the data base")
def price_of_all_products():
    data = conn.execute("SELECT rowid,product_url FROM PRODUCTS").fetchall()
    for i in data :
        row_id = i[0]
        product_url = i[1]
        price = scraper.fetch_price(product_url)
        print(price)
        time_now = datetime.datetime.now()
        formated_time = datetime.datetime.strftime(time_now,"%d/%m/%Y %H:%M:%S")
        conn.execute("INSERT INTO PRICES VALUES(?,?,?)",(row_id,price,formated_time))



while (True):
    print("\nMAIN MENU")
    choice = input("1.add product\n2.show all products \n3.price of product\n4.delete product\n5.price of all products\n6.exit\nEnter choice:")
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
            print("quitting program")
            break