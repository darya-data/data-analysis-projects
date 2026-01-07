import random


def fortune_teller():
    """
    Генерирует случайное предсказание, комбинируя фразы из файлов.

    Функция читает четыре текстовых файла с частями предсказаний, случайным образом
    выбирает по одной фразе из каждого файла и объединяет их в полное предсказание.

    Returns:
        str: Случайное предсказание в виде строки.
    """
    with open("horoscope_1.txt", "r", encoding="utf-8") as f1:
        first = random.choice([line.strip() for line in f1])
    with open("horoscope_2.txt", "r", encoding="utf-8") as f2:
        second = random.choice([line.strip() for line in f2])
    with open("horoscope_3.txt", "r", encoding="utf-8") as f3:
        third = random.choice([line.strip() for line in f3])
    with open("horoscope_4.txt", "r", encoding="utf-8") as f4:
        fourth = random.choice([line.strip() for line in f4])
    return f"{first} {second} {third} {fourth}"


if __name__ == '__main__':
    horo = fortune_teller()
    print(horo)
