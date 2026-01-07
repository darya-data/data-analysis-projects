import anecdotes
import films
import game
import horoscopes
import memes
import os
import random
import talking
import wiki
import telebot
from telebot import types
from key import API_KEY

if __name__ == '__main__':
    bot = telebot.TeleBot(API_KEY)

    os.makedirs('logs', exist_ok=True)
    os.makedirs('logs/conversations', exist_ok=True)
    os.makedirs('logs/wikis', exist_ok=True)
    os.makedirs('logs/films', exist_ok=True)

    @bot.message_handler(commands=['start'])
    def start(message):
        """
        Обрабатывает команду '/start' в Telegram боте, отправляя приветственное сообщение и меню.

        Функция создает интерактивное меню с четырьмя основными опциями бота и отправляет
        два сообщения: предупреждение о контенте и приветствие с меню выбора действий.

        Args:
            message (types.Message): Объект сообщения от Telegram API, содержащий:
            - chat.id: ID чата для отправки ответа.
            - from_user.first_name: Имя пользователя для персонализации приветствия.

        Returns:
            None: Функция не возвращает значение, только отправляет сообщения в чат.
        """
        main = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton('📝 Найти информацию', callback_data='option1')
        item2 = types.InlineKeyboardButton('🤪 Посмеяться', callback_data='option2')
        item3 = types.InlineKeyboardButton('🎬 Порекомендовать фильм', callback_data='option3')
        item4 = types.InlineKeyboardButton('🎯 Поиграть в игру', callback_data='option4')
        main.add(item1, item2, item3, item4)
        bot.send_message(message.chat.id,
                         f'Внимание! 🔞 Информация (в том числе игры, картинки и рекомендации), которую присылает '
                         f'этот бот, собрана на просторах Интернета. Она может показаться неуместной или '
                         f'оскорбительной определенным группам людей. Если Вы относите себя к таким группам, то, '
                         f'пожалуйста, не пользуйтесь этим ботом. Только если Вы внимательно прочитали это и согласны, '
                         f'что ответственность за просмотр этих материалов не несет никто, кроме Вас, продолжайте. '
                         f'Продолжая пользоваться этим ботом, вы подтверждаете, что Вам исполнилось 18 лет или больше. '
                         f'Если вам нет 18 лет, пожалуйста, покиньте бота.')
        bot.send_message(message.chat.id,
                         f"✌️ Добрый день, {message.from_user.first_name}! Можно выбрать что-то из меню или "
                         f"написать мне, чтобы поговорить",
                         reply_markup=main)


    func = 0


    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        """
        Основной обработчик инлайн-кнопок Telegram бота.

        Обрабатывает все callback запросы от интерактивных кнопок меню, обеспечивая
        навигацию по функциям бота и взаимодействие с пользователем. Функция использует
        глобальную переменную `func` для отслеживания текущего режима работы бота.

        Args:
            call (types.CallbackQuery): Объект callback запроса от Telegram API, содержащий:
                - data: Идентификатор callback_data нажатой кнопки.
                - message: Объект сообщения с кнопкой.
                - from_user: Информация о пользователе.
                - chat: Информация о чате.

        Returns:
            None: Функция не возвращает значения, только отправляет сообщения и редактирует меню.
        """
        global func

        if call.data == "mainmenu":
            func = 0
            main = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton('📝 Найти информацию', callback_data='option1')
            item2 = types.InlineKeyboardButton('🤪 Посмеяться', callback_data='option2')
            item3 = types.InlineKeyboardButton('🎬 Порекомендовать фильм', callback_data='option3')
            item4 = types.InlineKeyboardButton('🎯 Поиграть в игру', callback_data='option4')
            main.add(item1, item2, item3, item4)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=f"🗣 Выберите что-то из меню или напишите, чтобы поговорить.", reply_markup=main)

        if call.data == "option1":
            menu1 = types.InlineKeyboardMarkup(row_width=1)
            key1 = types.InlineKeyboardButton(text='Ⓨ Перейти в Яндекс', url='https://ya.ru/', parse_mode='html')
            key2 = types.InlineKeyboardButton(text='Ⓦ Найти информацию в Википедии', callback_data='wiki')
            main_menu = types.InlineKeyboardButton(text='☰ В главное меню', callback_data='mainmenu')
            menu1.add(key1, key2, main_menu)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=f"🧐 Выберите что-то из меню", reply_markup=menu1)

        if call.data == "wiki":
            func = 1
            menu_back = types.InlineKeyboardMarkup(row_width=1)
            back = types.InlineKeyboardButton(text='↩ Назад', callback_data='option1')
            main_menu = types.InlineKeyboardButton(text='☰ В главное меню', callback_data='mainmenu')
            menu_back.add(back, main_menu)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='🧐 О чем расказать?',
                                  reply_markup=menu_back)

        if call.data == "option2":
            menu2 = types.InlineKeyboardMarkup(row_width=1)
            key1 = types.InlineKeyboardButton(text='🤭 Получить анекдот', callback_data='joke')
            key2 = types.InlineKeyboardButton(text='🤡 Получить мем', callback_data='mem')
            main_menu = types.InlineKeyboardButton(text='☰ В главное меню', callback_data='mainmenu')
            menu2.add(key1, key2, main_menu)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=f"🧐 Выберите что-то из меню", reply_markup=menu2)

        if call.data == "joke":
            bot.send_message(call.message.chat.id, random.choice(anecdotes.parser_a()))
            menu_back = types.InlineKeyboardMarkup(row_width=1)
            key1 = types.InlineKeyboardButton(text='🤭 Еще анекдот', callback_data='joke')
            back = types.InlineKeyboardButton(text='↩ Назад', callback_data='option2')
            main_menu = types.InlineKeyboardButton(text='☰ В главное меню', callback_data='mainmenu')
            menu_back.add(key1, back, main_menu)
            bot.send_message(call.message.chat.id, '🧐 Введите запрос повторно или перейдите в другое меню',
                             reply_markup=menu_back)

        if call.data == "mem":
            bot.send_photo(call.message.chat.id, photo=memes.parser_m())
            menu_back = types.InlineKeyboardMarkup(row_width=1)
            key1 = types.InlineKeyboardButton(text='🤡 Еще мем', callback_data='mem')
            back = types.InlineKeyboardButton(text='↩ Назад', callback_data='option2')
            main_menu = types.InlineKeyboardButton(text='☰ В главное меню', callback_data='mainmenu')
            menu_back.add(key1, back, main_menu)
            bot.send_message(call.message.chat.id, '🧐 Введите запрос повторно или перейдите в другое меню',
                             reply_markup=menu_back)

        if call.data == "option3":
            func = 2
            menu3 = types.InlineKeyboardMarkup(row_width=1)
            main_menu = types.InlineKeyboardButton(text='☰ В главное меню', callback_data='mainmenu')
            menu3.add(main_menu)
            bot.send_message(call.message.chat.id,
                             '🧐 Введите информацию о фильме или жанр или вернитесь в главное меню', reply_markup=menu3)

        if call.data == "option4":  #
            menu4 = types.InlineKeyboardMarkup(row_width=1)
            key1 = types.InlineKeyboardButton(text='🎲 Играть в "Камень, ножницы, бумага"',
                                              callback_data='rock_paper_scissors')
            key2 = types.InlineKeyboardButton(text='💫 Получить предсказание на день', callback_data='fortune_telling')
            main_menu = types.InlineKeyboardButton(text='☰ В главное меню', callback_data='mainmenu')
            menu4.add(key1, key2, main_menu)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=f"🧐 Выберите желаемый вариант:", reply_markup=menu4)

        if call.data == "rock_paper_scissors":
            menu_game1 = types.InlineKeyboardMarkup(row_width=1)
            key1 = types.InlineKeyboardButton(text='🗿 камень', callback_data='rock')
            key2 = types.InlineKeyboardButton(text='✂ ножницы', callback_data='scissors')
            key3 = types.InlineKeyboardButton(text='📃 бумага', callback_data='paper')
            back = types.InlineKeyboardButton(text='↩ Назад', callback_data='option4')
            main_menu = types.InlineKeyboardButton(text='☰ В главное меню', callback_data='mainmenu')
            menu_game1.add(key1, key2, key3, back, main_menu)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text="🎉 Добро пожаловать в игру 'Камень, ножницы, бумага'! "
                                       "Выберите желаемый вариант: ",
                                  reply_markup=menu_game1)
        if call.data == "rock":
            bot.send_message(call.message.chat.id, game.play_game("🗿 камень"))
            menu_back = types.InlineKeyboardMarkup(row_width=1)
            key1 = types.InlineKeyboardButton(text='🎲 Играть еще', callback_data='rock_paper_scissors')
            back = types.InlineKeyboardButton(text='↩ Назад', callback_data='option4')
            main_menu = types.InlineKeyboardButton(text='☰ В главное меню', callback_data='mainmenu')
            menu_back.add(key1, back, main_menu)
            bot.send_message(call.message.chat.id, '🧐 Нажмите желаемую кнопку', reply_markup=menu_back)
        if call.data == "scissors":
            bot.send_message(call.message.chat.id, game.play_game("✂ ножницы"))
            menu_back = types.InlineKeyboardMarkup(row_width=1)
            key1 = types.InlineKeyboardButton(text='🎲 Играть еще', callback_data='rock_paper_scissors')
            back = types.InlineKeyboardButton(text='↩ Назад', callback_data='option4')
            main_menu = types.InlineKeyboardButton(text='☰ В главное меню', callback_data='mainmenu')
            menu_back.add(key1, back, main_menu)
            bot.send_message(call.message.chat.id, '🧐 Нажмите желаемую кнопку', reply_markup=menu_back)
        if call.data == "paper":
            bot.send_message(call.message.chat.id, game.play_game("📃 бумага"))
            menu_back = types.InlineKeyboardMarkup(row_width=1)
            key1 = types.InlineKeyboardButton(text='🎲 Играть еще', callback_data='rock_paper_scissors')
            back = types.InlineKeyboardButton(text='↩ Назад', callback_data='option4')
            main_menu = types.InlineKeyboardButton(text='☰ В главное меню', callback_data='mainmenu')
            menu_back.add(key1, back, main_menu)
            bot.send_message(call.message.chat.id, '🧐 Нажмите желаемую кнопку', reply_markup=menu_back)

        if call.data == "fortune_telling":
            bot.send_message(call.message.chat.id, horoscopes.fortune_teller())
            menu_game2 = types.InlineKeyboardMarkup(row_width=1)
            key1 = types.InlineKeyboardButton(text='💫 Предсказание для другого человека',
                                              callback_data='fortune_telling')
            back = types.InlineKeyboardButton(text='↩ Назад', callback_data='option4')
            main_menu = types.InlineKeyboardButton(text='☰ В главное меню', callback_data='mainmenu')
            menu_game2.add(key1, back, main_menu)
            bot.send_message(call.message.chat.id, '🧐 Для одного человека можно получить только одно предсказание',
                             reply_markup=menu_game2)


    @bot.message_handler(content_types=["text"])
    def handle_text(message):
        """
        Основной обработчик текстовых сообщений от пользователей в Telegram боте.

        Функция обрабатывает все текстовые сообщения, направляя их в соответствующие
        модули в зависимости от текущего режима работы бота (глобальная переменная `func`).
        Режимы определяют, какой функционал активирован: диалог, поиск или рекомендации.

        Args:
            message (types.Message): Объект сообщения от Telegram API, содержащий:
                - text: Текст сообщения пользователя.
                - chat.id: ID чата для отправки ответа.
                - from_user.first_name: Имя пользователя для персонализации.
                - message_id: ID сообщения для возможного редактирования.

        Returns:
            None: Функция не возвращает значения, только отправляет ответы в чат.
        """
        global func
        if message.text == True:
            func = 0
        elif func == 0:
            bot.send_message(message.chat.id, talking.conversation(message.text, message.from_user.first_name))
            menu_back = types.InlineKeyboardMarkup(row_width=1)
            main_menu = types.InlineKeyboardButton(text='☰ В главное меню', callback_data='mainmenu')
            menu_back.add(main_menu)
            bot.send_message(message.chat.id, '🗣 Продолжите разговор или вернитесь в главное меню',
                             reply_markup=menu_back)
        elif func == 1:
            bot.send_message(message.chat.id, wiki.get_wiki(message.text, message.from_user.first_name))
            menu_back = types.InlineKeyboardMarkup(row_width=1)
            back = types.InlineKeyboardButton(text='↩ Назад', callback_data='option1')
            main_menu = types.InlineKeyboardButton(text='☰ В главное меню', callback_data='mainmenu')
            menu_back.add(back, main_menu)
            bot.send_message(message.chat.id, '🧐 Введите запрос для повторного поиска или вернитесь назад',
                             reply_markup=menu_back)
        elif func == 2:
            bot.send_message(message.chat.id, films.get_response(message.text, message.from_user.first_name))
            menu_back = types.InlineKeyboardMarkup(row_width=1)
            main_menu = types.InlineKeyboardButton(text='☰ В главное меню', callback_data='mainmenu')
            menu_back.add(main_menu)
            bot.send_message(message.chat.id,
                             '🧐 Введите запрос для повторной рекомендации или вернитесь в главное меню',
                             reply_markup=menu_back)


    bot.infinity_polling(none_stop=True, timeout=123)



