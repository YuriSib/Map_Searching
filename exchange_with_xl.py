import openpyxl
import pickle


def import_xl(stop, start=2):
    catalog = openpyxl.open('plases.xlsx', read_only=True)
    sheet = catalog.active
    list_qwery_ = []

    count = 0
    #sheet.max_row + 1 в range - для вывода всего ряда (start, finish) - для диапазона
    for row in range(start, stop + 1):
        search_query = ''

        city = sheet[start][0].value
        place = sheet[start][1].value

        search_query = city + ' ' + place
        list_qwery_.append(search_query)
        count += 1

    return list_qwery_


# запись в pickle
list_qwery = import_xl(2991)
with open('data.pickle', 'wb') as file:
    pickle.dump(list_qwery, file)
