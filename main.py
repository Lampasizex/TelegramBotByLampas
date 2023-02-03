import telebot
from extensions import APIException, Convertor
from config import TOKEN, exchanges
import traceback


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Привет, доступные команды:/start , /help , /values , формат ввода: валюта валюта количество"

    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values', ])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    currencies = message.text.split()
    try:
        if len(currencies) != 3:
            raise APIException('Неверное количество параметров!')

        answer = Convertor.get_price(*currencies)

    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.send_message(message.chat.id, f"Неизвестная ошибка:\n{e}")
    else:
        bot.send_message(message.chat.id, answer)


bot.polling()



