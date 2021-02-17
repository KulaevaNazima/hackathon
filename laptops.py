from bs4 import BeautifulSoup
import requests
import csv

CSV = 'SulpakLaptops.csv'
HOST = 'https://www.sulpak.kg'
URL = 'https://www.sulpak.kg/f/noutbuki'
HEADERS = { 
    'Accept' : 'image/webp,*/*',    
    'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0'
}

def get_html(url, params=''):
    r = requests.get(url, headers = HEADERS, params=params)     
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('div', class_ = 'product-container-right-side')
    LaptopList = []

    for item in items:
        LaptopList.append({
            'name': item.find('a').find('h3', class_ = 'title').get_text(strip = True),
            'Prce': item.find('div', class_ = 'price-block').get_text(strip = True),
        })
    return LaptopList 
def new_save(items, path):
    with open(path, 'a') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Name', 'Link'])
        for item in items:    
            writer.writerow([item['name'], item['Prce']])

def parser():
    PAGENATION = input("Введите количество страниц: ")
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        new_list = []
        for page in range(1, PAGENATION):
            print(f'Страница №{page} готова')
            html = get_html(URL, params={'page' : page})
            new_list.extend(get_content(html.text))
        new_save(new_list, CSV)
        print('Парсинг готов')
    else:
        print('Error')

parser()
