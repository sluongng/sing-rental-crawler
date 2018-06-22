import requests
import time
from bs4 import BeautifulSoup

BASE_URL = 'https://sg.carousell.com'
BASE_PATH = '/categories/property-102/housing-rentals-229'

PARAMS = {
    'sort_by': 'time_created,descending',
    'location_distance': 2.5,
    'location_unit': 0,
    'location_name': '30 Jln Kilang Barat',
    'location_latitude': '1.2843839',
    'location_longitude': '103.80940020000003',
    'collection_id': '229',
}

# Unit is seconds
REFRESH_INTERVAL = 60

def main():
    while(True):
        result = requests.get(BASE_URL + BASE_PATH, PARAMS)
        if result.ok:
            soup = BeautifulSoup(result.text, 'html.parser')
            cards = soup.findAll('figure', {'class': 'card'})
            for card in cards:
                picture = card.find('a', {'id': 'productCardThumbnail'}).find('img')
                if 'data-layzr' in picture:
                    picture = picture['data-layzr']
                else:
                    picture = picture['src']
                
                detail = card.find('figcaption')

                title = detail.find('h4').text.replace(u"\u2018", "'").replace(u"\u2019", "'")
                
                url = detail.a['href']
                url = BASE_URL + url[:url.find('?')]
                
                price = detail.find('dd')
                price = price.text[2:]
                
                print "Title:\t{}".format(title)
                print "Pic:\t{}".format(picture)
                print "URL:\t{}".format(url)
                print "Price:\t{} SGD".format(price)
                print "---"
        else:
            print result

        print 'Loop finished'
        time.sleep(REFRESH_INTERVAL)

if __name__ == '__main__':
    main()
