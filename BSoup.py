import collections
from bs4 import BeautifulSoup as BS


class Beautiful:
    """
    stores response objects from Gismeteo in soup and parses data
    """

    def __init__(self):
        """
        creates list for store all collected data for user
        """
        self.data = []

    def update_data(self, d):
        """
        updates data after collecting
        :param d: named tuple (city, data) with city(str) and weather data (dict of dicts)
        :return: updated 'big' data
        """
        self.data.append(d)

    def get_city(self, response):
        """
        parses Cities, which were chosen by user
        :param response: response object
        :return: list of Cities and links on them in Gismeteo
        """
        soup = BS(response, 'lxml')
        links = []
        cities = []
        try:
            all_catalog = soup.findAll('div', {'class': 'districts wrap'})[:-1]
            for section in all_catalog:
                group = section.findAll('div', {'class': 'group'})
                for part_group in group:
                    part_group.find('ul')
                    li = part_group.findAll('li')
                    for d in li:
                        l = d.find('a')
                        link = l.get('href')
                        city = d.text.strip()
                        remove = '\t\n'
                        table = str.maketrans("", "", remove)
                        city = city.translate(table)
                        cities.append(city)
                        links.append(link)
        except (IndexError, Exception):
            raise ValueError('Попробуйте еще раз')
        return cities, links


    def fill_data(self, response, number, city):
        """
        parses page, collect data for user
        :param response: response object
        :param number: index (int)
        :param city: list of cities (lst)
        """
        _title = collections.namedtuple('Title', 'City Data')
        _title.City = city
        _title.Data = []
        dict_date = collections.OrderedDict()
        soup = BS(response, 'lxml')
        content = soup.findAll('div', {'class': 'wbfull'})[number]
        weather = content.findAll('tr')
        for el in weather:
            day = el.find('th').text
            dict_date[day] = collections.OrderedDict()
            params = el.findAll('td')[1:]
            dict_date[day]['Облачность'] = params[0].text
            dict_date[day]['Температура'] = params[1].find('span', {'class': 'value m_temp c'}).text
            dict_date[day]['Атм.давление'] = params[2].find('span', {'class': 'value m_press torr'}).text
            title = params[3].find('dt').get('title')
            wind = params[3].find('dd').find('span', {'class': 'value m_wind ms'}).text
            dict_date[day]['Ветер'] = title + ', ' + wind
            dict_date[day]['Влажность'] = params[4].text
            dict_date[day]['Комфортная температура'] = params[5].find('span', {'class': 'value m_temp c'}).text
        if self.data:
            if city == self.data[-1].City:
                self.data[-1].Data.append(dict_date)
                return
            else:
                _title.Data.append(dict_date)
        else:
            _title.Data.append(dict_date)
        self.update_data(_title)
