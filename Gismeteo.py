import requests
import collections
from bs4 import BeautifulSoup as BS

URL = 'https://www.gismeteo.ua'
HEADERS = {
    'Host': 'www.gismeteo.ua',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'text/html; charset=UTF-8',
    'Connection': 'keep-alive'
}


class Request:
    """
    get requests from url and check all errors
    """
    def __init__(self):
        self._url = URL
        self.headers = HEADERS

    def get_request(self, url):
        """
        gets and returns requests
        :param url: lint which has to be concatenated with base url
        :return: request.content
        """
        try:
            response = requests.get(self._url + url, headers=self.headers, stream=True)
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError,
                requests.exceptions.Timeout, requests.exceptions.SSLError, requests.exceptions.ProxyError):
            raise ValueError('Извините, произошла ошибка подключения')
        if response.status_code != 200:
            raise ZeroDivisionError('Нет доступа к запрашиваемой информации')
        return response.content


class User:
    """
    gets user's answers and represents data for user
    """
    def get_city(self):
        city = input('Какой город Вас интересует? Введите первые 3-4 буквы: ')
        return city
    def select_number(self, lst):
        """
        asks user for number in list of variants which represents index of link
         on chosen variant in links-list
        :param lst: list of variants for user's choice
        :return: index of link, int
        """
        try:
            number = int(input('Введите номер из списка напротив интересующего Вас пункта или -1, чтобы выйти '))
        except:
            raise ValueError('Неверный формат ввода')
        if number == -1:
            return number
        number -= 1
        if number not in range(0, len(lst) + 1):
            raise ValueError('Неверный номер')
        return number

    def represent(self, date, data, counter):
        """
        takes chosen dates, index and data from Gismeteo and prints data for user
        :param date: list of strings with chosen by user dates
        :param data: list of namedtuples (city (str) and data (dict of dicts)
        :param counter: index on current data to display
        """
        print()
        city = data[counter].City
        print('Прогноз погоды г.{}'.format(city))
        print('-' * 41)
        for i, row in enumerate(data[counter].Data):
            for key in row:
                print(date[i])
                print('-' * 41)
                print(key)
                print('-' * 41)
                for k in row[key]:
                    print('{:<22}\t{}'.format(k, row[key][k]))
                print()
            print()
