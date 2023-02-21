import requests
from bs4 import BeautifulSoup


def send(url):
    response = requests.get(url)

    if response.status_code != 200:
        return None
    
    return response.text


def get_product_categories_from_site(categories, url):
    response_data = send(url=url)
    soup = BeautifulSoup(response_data, 'lxml')
    soup = soup.find_all('li', class_='first')

    for i, s in enumerate(soup, start=1):
        sub_categories = []
        if s.findChildren('a', class_='sub'):
            for j, sub_c in enumerate(s.findChildren('a', class_='sub'), start=1):
                sub_categories.append(
                    {'id': f'{i}.{j}', 'name': sub_c.text, 'url': sub_c.get('href')}
                )

        categories.append(
            {
                'id': f'{i}',
                'name': s.findChildren('a', 'first')[0].text,
                'url': s.findChildren('a', 'first')[0].get('href'),
                'sub_categories': sub_categories,
            }
        )


def get_products_from_site(products: list, url):
    products.clear()
    response_data = send(url=url)
    soup = BeautifulSoup(response_data, 'lxml')
    soup = soup.find_all('div', class_='list-showcase__name')

    for s in soup:
        products.append({'name': s.text})
