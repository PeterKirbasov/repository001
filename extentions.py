import json
import requests


class APIException(Exception):
    pass


class StatikClass:
    @staticmethod
    def get_price( quote: str, base: str, amount: str, keys):
        # в задании указана передача 3х аргументов, однако в \
        # в отзыве заказчика на предыдущие 2 работы есть требование
        # не использовать глобальные переменные ( даже контстанты _),
        # поэтому считаем это неявным требованием к коду и
        # передаем четвертый аргумент, таблицу тикетов
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

#        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
#        print(f'https://v6.exchangerate-api.com/v6/674726c975e9a219fa5294bb/pair/{quote_ticker}/{base_ticker}')
        r = requests.get(f'https://v6.exchangerate-api.com/v6/674726c975e9a219fa5294bb/pair/{quote_ticker}/{base_ticker}')
        total_base = json.loads(r.content)['conversion_rate']*amount

        #total_base = json.loads(r.content)

        return total_base