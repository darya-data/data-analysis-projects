import emoji
import nltk
import re
import string
from datetime import datetime
from pymorphy3 import MorphAnalyzer
from stop_words import get_stop_words
from transformers import AutoModelForCausalLM, AutoTokenizer
nltk.download('stopwords')
# nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')

model_name = 'sberbank-ai/rugpt3small_based_on_gpt2'
tokenizer = AutoTokenizer.from_pretrained(model_name)
txtgen_model = AutoModelForCausalLM.from_pretrained(model_name)

MorphAnalyzer = MorphAnalyzer()
sw = set(get_stop_words('ru') + nltk.corpus.stopwords.words('russian'))
exclude = set(string.punctuation)

history_dialog = []
histories = {}


def preprocess_txt(txt):
    """
    Выполняет комплексную предобработку текста на русском языке для задачи NLP.

    Функция выполняет последовательную очистку и нормализацию текста:
    1. Удаляет пунктуацию, HTML-теги, URL-адреса и некириллические символы.
    2. Приводит текст к нижнему регистру.
    3. Удаляет эмодзи и короткие слова.
    4. Токенизирует текст.
    5. Удаляет стоп-слова русского языка.
    6. Выполняет лемматизацию слов.

    Args:
        txt (str): Исходный текст для предобработки.

    Returns:
        txt (list): Список предобработанных токенов (лемматизированных слов) в нижнем регистре,
        очищенных от стоп-слов и нерелевантных символов.
    """
    txt = re.sub(r'[^\w\s]', ' ', txt)
    txt = re.sub(r'http\S+', '', txt)
    txt = re.sub('<[^<]+?>', '', txt)
    txt = re.sub(r'[^а-яА-Я]', ' ', txt)
    txt = txt.lower()
    txt = emoji.replace_emoji(txt, replace='')
    txt = ' '.join([w for w in txt.split() if len(w) > 1])
    txt = nltk.tokenize.word_tokenize(txt)
    txt = [item for item in txt if item not in nltk.corpus.stopwords.words('russian')]
    txt = [nltk.stem.wordnet.WordNetLemmatizer().lemmatize(word) for word in txt]
    return txt


def respond_to_dialog(texts):
    """
    Генерирует ответ на основе истории диалога с использованием языковой модели.

    Функция принимает историю диалога, форматирует её,
    передаёт в языковую модель 'sberbank-ai/rugpt3small_based_on_gpt2' и извлекает
    сгенерированный ответ.

    Args:
        texts (str): История диалога в виде списка строк, где элементы чередуются:
            - Чётные индексы - сообщения пользователя.
            - Нечётные индексы - ответы бота.

    Returns:
        result (str): Сгенерированный ответ бота.
    """
    prefix = '\nx:'
    for i, t in enumerate(texts):
        prefix += t
        prefix += '\nx:' if i % 2 == 1 else '\ny:'
    tokens = tokenizer(prefix, return_tensors='pt')
    tokens = {k: v.to(txtgen_model.device) for k, v in tokens.items()}
    end_token_id = tokenizer.encode('\n')[0]
    size = tokens['input_ids'].shape[1]
    output = txtgen_model.generate(
        **tokens,
        eos_token_id=end_token_id,
        do_sample=True,
        max_length=size + 128,
        repetition_penalty=3.2,
        temperature=1,
        num_beams=3,
        length_penalty=0.01,
        pad_token_id=tokenizer.eos_token_id
    )
    decoded = tokenizer.decode(output[0])
    result = re.findall(r'\ny:(.+)', decoded)[-1]

    return result.strip()


def conversation(txt, user_id=None):
    """
    Обрабатывает пользовательское сообщение в контексте диалога и возвращает ответ.

    Основная функция для управления диалогами с поддержкой множества пользователей.
    Сохраняет историю диалога, генерирует контекстно-зависимые ответы с помощью
    языковой модели и логирует диалог.

    Args:
        txt (str): Текст сообщения от пользователя. Содержит строку на естественном языке.
        user_id (str): Уникальный идентификатор пользователя. Используется для персонализированного
        логирования в отдельные файлы. По умолчанию None.

    Returns:
        response (str): Ответ бота, сгенерированный на основе контекста диалога.
        Ответ формируется с учётом последних 100 сообщений пользователя.
    """
    global history_dialog

    if user_id not in histories:
        histories[user_id] = []

    history_dialog = histories[user_id]
    history_dialog.append(txt)
    context = history_dialog[-100:]

    response = respond_to_dialog(context)
    history_dialog.append(response)

    log_file = f'logs/conversations/user_{user_id}.txt'
    timestamp = datetime.now().strftime('%d.%m.%Y %H:%M:%S')

    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n[{timestamp}] 👤: {txt}\n")
        f.write(f"[{timestamp}] 🤖: {response}\n")
        f.write(f"{'-' * 60}\n")

    return response


if __name__ == '__main__':
    dialog = input("Введите текст\n")
    dialog = conversation(dialog)
    print(dialog)
