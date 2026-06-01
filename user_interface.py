import scraper
import sqlite3
conn = sqlite3.connect("amazon_products_data.db",isolation_level=None)
conn.execute("CREATE TABLE IF NOT EXISTS products(product_name TEXT,product_url TEXT)STRICT")
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
    url = conn.execute("SELECT product_url FROM PRODUCTS WHERE product_name = ?",[product_name]).fetchone()
    if url[0] is None:
        print("no such product")
    else:
        price = scraper.fetch_price(url[0])
        print(f"{product_name} {price[0:-3]}")
def delete_product():
    product_name = input("enter product name:")
    conn.execute("DELETE FROM PRODUCTS WHERE product_name = ?",(product_name,))
    print("product deleted from the data base")
while (True):
    print("\nMAIN MENU")
    choice = input("1.add product\n2.show all products \n3.price of product\n4.delete product\n5.exit\nEnter choice:")
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
            print("quitting program")
            break