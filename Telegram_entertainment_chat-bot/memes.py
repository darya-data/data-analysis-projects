import random
import requests
from bs4 import BeautifulSoup

url_m = 'https://www.memify.ru/'


def parser_m(url=url_m):
    """
    Парсит веб-страницу и возвращает ссылку на случайное изображение.

    Args:
        url (str): URL страницы для парсинга.

    Returns:
        result (str): URL изображения.
    """
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    image_tags = soup.find_all('img')
    image_links = [tag['src'] for tag in image_tags]
    res_links = []
    for link in image_links:
        if link.startswith('https://www.nvcdn.memify'):
            res_links.append(link)
    result = random.choice(res_links)
    return result


if __name__ == '__main__':
    mem = random.choice(parser_m())
    print(mem)
