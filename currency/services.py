import decimal
import xml.etree.ElementTree as etree

from django.utils import formats

from currency.models import Currency
from utils.client import ConnectorRequests
from utils.helpers import decimal_format

url_source = 'http://www.cbr.ru/scripts/XML_daily.asp'


def load_currencies_data():
    """Загрузка данных о валютах из внешнего источника."""
    with ConnectorRequests() as connector:
        response = connector.perform_request(url_source, method='GET')

    root = etree.fromstring(response.text)
    for valute in root.findall('Valute'):
        code = valute.find('CharCode').text
        name = valute.find('Name').text
        nominal = valute.find('Nominal').text
        value = valute.find('Value').text

        try:
            nominal_num = int(nominal)
        except (TypeError, ValueError):
            raise ServiceError('Ошибка преобразования данных.')

        try:
            value = formats.sanitize_separators(value)
            rate_base = decimal.Decimal(value)
        except (ValueError, TypeError, decimal.InvalidOperation):
            raise ServiceError('Ошибка преобразования данных.')

        rate = rate_base / nominal_num
        data = {
            'code': code,
            'name': name,
            'rate': rate,
            }
        save_currency(data)


def save_currency(data):
    """Сохраннение данных о валюте."""
    try:
        currency = Currency.objects.get(code=data['code'])
        # округляем, чтобы было корректное сравнение,
        # т.к. при сохранении в БД django принудительно округляет в соответствии с decimal_places
        rate = decimal_format(data['rate'], Currency._meta.get_field('rate').decimal_places)

        if currency.name != data['name'] or currency.rate != rate:
            currency.name = data['name']
            currency.rate = rate
            currency.save(update_fields=['name', 'rate'])
    except Currency.DoesNotExist:
        currency = Currency.objects.create(**data)
    return currency


def get_currency_by_id(currency_id):
    """Получение данных о валюте по идентификатору."""
    try:
        currency = Currency.objects.get(pk=currency_id)
    except Currency.DoesNotExist:
        raise EntityDoesNotExist
    return currency


def get_all_currencies():
    """Получение данных обо всех валютах."""
    return Currency.objects.all().order_by('id')


class EntityDoesNotExist(Exception):
    pass


class ServiceError(Exception):
    pass
