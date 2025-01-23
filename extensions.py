import requests
import json


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        if base == quote:
            raise APIException(f'Неверные данные: валюта {base} не может быть равна {quote}.')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Неудалось обработать количество: {amount}. Это должно быть числом.')

        url = f'https://api.exchangerate-api.com/v4/latest/{base}'

        response = requests.get(url)
        if response.status_code != 200:
            raise APIException(f'Ошибка API. {response.status_code}: {response.text}')

        data = json.loads(response.text)
        if quote not in data['rates']:
            raise APIException(f'Валюта {quote} не найдена.')

        return data['rates'][quote] * amount
