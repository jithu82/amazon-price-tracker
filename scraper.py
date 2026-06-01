import bs4,requests
import time
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-IN,en;q=0.9",  # Requests the page with Indian regional formatting
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://google.com"
    }

def fetch_price(url):
    time.sleep(2)
    response = requests.get(url,headers=headers)
    soup = bs4.BeautifulSoup(response.text,"html.parser")
    price =soup.select_one('#apex-pricetopay-accessibility-label').text
    return price.split()[0]
