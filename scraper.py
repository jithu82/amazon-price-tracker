import bs4,requests


def fetch_price(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text,"html.parser")
    price =soup.select('#apex-pricetopay-accessibility-label')
    return (price[0].text)
url = "https://www.amazon.in/MuscleBlaze-Performance-Clinically-Absorption-Certified/dp/B0BPCR7K7F/ref=sr_1_6?crid=K2PLN9A3WP0H&dib=eyJ2IjoiMSJ9.EOjA9t-SnD_MbkQJM6ylSuK0isYCQUnK0Ep3trO9GfKUT1ZoxQEwFY-Urx9xAosLFQ4Xpx4vg3CcqW7Rq1jZf4Yq1mcqIxKeV7RHbum0fkcdaoz6T-X8mojY09vd1ROQ4cqlmIQJqQSYIJmZSpMVoARjkzTGclzejbW376PgT0rN6sQnkLZdzPLdhY6dlfARLr_bcjqFCmanFTNdVn_pnJBzKpoKAneiI4g59cUWHZUZLJ9HjJkZsGB7w5pDktl6sGl-0_AsgqqZwUORX-vwqn0KuVsw1ty1pfiaxp8MuqI.zpdV6u3hX7ZptDRSsmDII4Ddith7PkHSRFwE-6Rq_Ag&dib_tag=se&keywords=protein%2Bpowder&qid=1780286344&sprefix=protein%2Bpow%2Caps%2C338&sr=8-6&th=1"
price = fetch_price(url)