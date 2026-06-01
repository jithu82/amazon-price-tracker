import bs4,requests
import time

def fetch_price(url):
    time.sleep(2)
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text,"html.parser")
    price =soup.select_one('#apex-pricetopay-accessibility-label').text
    return price.split()[0]
