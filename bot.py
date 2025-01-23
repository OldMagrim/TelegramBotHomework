import telebot
from extensions import CurrencyConverter, APIException
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для получения цен на валюту. Для использования введите:\n"
                          "<имя валюты> <валюта, в которой надо узнать цену> <количество>\n"
                          "Для получения списка доступных валют используйте команду /values.")

@bot.message_handler(commands=['values'])
def values(message):
    available_currencies = "Доступные валюты: евро (EUR), доллар (USD), рубль (RUB)"
    bot.reply_to(message, available_currencies)

@bot.message_handler(func=lambda message: True)
def get_currency_price(message):
    try:
        base, quote, amount = message.text.split()
        price = CurrencyConverter.get_price(base.upper(), quote.upper(), amount)
        bot.reply_to(message, f'{amount} {base.upper()} = {price} {quote.upper()}')
    except APIException as e:
        bot.reply_to(message, f'Ошибка: {e}')
    except Exception:
        bot.reply_to(message, 'Не удалось обработать данные. Пожалуйста, проверьте формат.')

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
