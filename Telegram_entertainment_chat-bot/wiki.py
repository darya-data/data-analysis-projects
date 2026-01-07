import re
import wikipedia
from datetime import datetime
wikipedia.set_lang("ru")


def get_wiki(txt, user_id=None):
    """
    Получает информацию из Wikipedia по заданному запросу.

    Функция выполняет поиск статьи в Wikipedia, обрабатывает её содержимое, извлекает основной текст,
    очищает его от разметки, ограничивает 2000 символов и возвращает результат.
    Все запросы логируются в файл для указанного пользователя.

    Args:
        txt (str):  Поисковый запрос для Wikipedia. Может быть названием статьи, термином или фразой для поиска.
        user_id (str): Уникальный идентификатор пользователя для логирования. Если None, логирование не выполняется.
                       По умолчанию None.

    Returns:
        str: Обработанный текст статьи из Wikipedia или сообщение об ошибке.
    """
    try:
        ny = wikipedia.page(txt)
        wikitext = ny.content[:2000]
        wikimas = wikitext.split('.')
        wikimas = wikimas[:-1]
        wikitext2 = ''
        for x in wikimas:
            if not('==' in x):
                if(len(x.strip()))>3:
                    wikitext2 = wikitext2 + x + '.'
            else:
                break
        wikitext2 = re.sub(r'\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub(r'\{[^\{\}]*\}', '', wikitext2)
        result = wikitext2

    except wikipedia.exceptions.PageError:
        result = 'В энциклопедии нет информации об этом'

    except wikipedia.exceptions.DisambiguationError as e:
        options = ', '.join(e.options[:3])
        result = f'Запрос неоднозначный. Возможно: {options}'

    except wikipedia.exceptions.HTTPTimeoutError:
        result = 'Запрос к занимает больше времени, чем ожидалось.'

    finally:
        with open(f'logs/wikis/user_{user_id}.txt', 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"Время: {timestamp}\n")
            f.write(f"Запрос: {txt}\n")
            f.write(f"Результат:\n{result}\n")
            f.write(f"{'-'*60}\n")

    return result


if __name__ == '__main__':
    info = input('Введите термин, информацию о котором хотите получить. '
                 'Пожалуйста, используйте начальную форму слова\n')
    info = get_wiki(info)
    print(info)
