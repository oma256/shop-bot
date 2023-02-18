import requests
from bs4 import BeautifulSoup


def send(url):
    response = requests.get(url)

    if response.status_code != 200:
        return None
    
    return response.text


def get_product_categories_from_site(url):
    response_data = send(url=url)
    soup = BeautifulSoup(response_data, 'lxml')
    soup = soup.find_all('a', class_='parent')

    for s in soup[2:]:
        data = {
            'name': s.text,
            'url': f'https://globus-online.kg{s.get("href")}',
        }
        print(data)
    
