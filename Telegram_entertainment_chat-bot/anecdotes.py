import random
import requests
from bs4 import BeautifulSoup

url_a = 'https://www.anekdot.ru/last/good/'


def parser_a(url=url_a):
    """
    Парсит веб-страницу с анекдотами и возвращает их список.

    Args:
        url (str): URL страницы для парсинга.

    Returns:
        result (list): Список строк, где каждый элемент - отдельный анекдот.
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    jokes = soup.find_all('div', class_='text')
    result = [c.text for c in jokes]
    return result


if __name__ == '__main__':
    joke = random.choice(parser_a())
    print(joke)
