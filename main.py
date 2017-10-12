from Gismeteo import *
from BSoup import *


def printVariants(catalog):
    """
    takes list of variants (Regions, Districts, Subdistricts, Cities or Dates) for user and prints them
    :param catalog: list of variants
    """
    for i, name in enumerate(catalog, start=1):
        print('{:<3}\t{}'.format(i, name))


user = User()
request = Request()
beautiful = Beautiful()
counter = 0
_dates = []
print('Вас приветствует программа прогноза погоды в Украине')
while True:
    try:
        response = request.get_request('/catalog/ukraine/')
    except ValueError as e:
        print(e)
        break
    except ZeroDivisionError as e:
        print(e)
        break
    try:
        regions, links = beautiful.get_catalog(response)
    except ValueError as e:
        print(e)
        continue
    printVariants(regions)
    while True:
        try:
            number = user.select_number(regions)
            break
        except ValueError as e:
            print(e)
            continue
    if number == -1:
        while True:
            ask = input('Вы хотите продолжить (д.н)? ')
            if ask not in 'дн':
                print('Не верный формат ввода')
                continue
            break
        if ask == 'д':
            continue
        else:
            break
    try:
        response = request.get_request(links[number])
    except ValueError as e:
        print(e)
        continue
    except ZeroDivisionError as e:
        print(e)
        break
    try:
        districts, links = beautiful.get_catalog(response)
    except ValueError as e:
        print(e)
        continue
    printVariants(districts)
    while True:
        try:
            number = user.select_number(regions)
            break
        except ValueError as e:
            print(e)
            continue
    if number == -1:
        continue
    try:
        response = request.get_request(links[number])
    except ValueError as e:
        print(e)
        continue
    except ZeroDivisionError as e:
        print(e)
        break
    cities, links = beautiful.get_city(response)
    printVariants(cities)
    while True:
        try:
            number = user.select_number(cities)
            break
        except ValueError as e:
            print(e)
            continue
    if number == -1:
        continue
    try:
        response = request.get_request(links[number] + '14-days/#')
    except ValueError as e:
        print(e)
        continue
    except ZeroDivisionError as e:
        print(e)
        break
    try:
        dates = beautiful.get_dates(response)
    except ValueError as e:
        print(e)
        continue
    printVariants(dates)
    numbers = []
    while True:
        try:
            num = user.select_number(dates)
        except ValueError as e:
            print(e)
            continue
        if num == -1:
            break
        if num in numbers:
            print('Дата уже отмечена')
            continue
        numbers.append(num)
    all_dates = []
    for num in numbers:
        all_dates.append(dates[num])
        try:
            beautiful.fill_data(response, num, cities[number])
        except ValueError as e:
            print(e)
            continue
    _dates.append(all_dates)
    user.represent(all_dates, beautiful.data, counter)
    counter += 1
while True:
    ask = input('Хотите увидеть всю информацию еще раз (д/н)? ').lower()
    if ask not in 'дн':
        print('Не верный формат ввода')
        continue
    if ask == 'н':
        break
    else:
        for i in range(counter):
            user.represent(_dates[i], beautiful.data, i)
        break
print('До свидания!')
