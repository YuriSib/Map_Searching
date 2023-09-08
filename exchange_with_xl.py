import openpyxl
import pickle


def import_xl(stop, start=2):
    catalog = openpyxl.open('plases.xlsx', read_only=True)
    sheet = catalog.active
    list_qwery_ = []

    #sheet.max_row + 1 в range - для вывода всего ряда (start, finish) - для диапазона
    for row in range(start, stop + 1):
        search_query = ''

        city = sheet[start][0].value
        place = sheet[start][1].value

        search_query = city + ' ' + place
        list_qwery_.append(search_query)
        start += 1

    return list_qwery_


def export_xl(value1, value2, value3, value4, value5, value6, value7, row):
    workbook = openpyxl.load_workbook('plases.xlsx')
    sheet = workbook.active
    sheet[row][2].value = value1
    sheet[row][3].value = value2
    sheet[row][4].value = value3
    sheet[row][5].value = value4
    sheet[row][6].value = value5
    sheet[row][7].value = value6
    sheet[row][8].value = value7
    workbook.save('plases.xlsx')


# list_qwery = import_xl(2991)
# with open('data.pickle', 'wb') as file:
#     pickle.dump(list_qwery, file)


# with open('data.pickle', 'rb') as file:
#     loaded_data = pickle.load(file)
#
# print(loaded_data)


# export_xl('10:00', 2, 5)
# export_xl('10:00', 3, 5)
# export_xl('10:00', 4, 5)
# export_xl('10:00', 5, 5)
# export_xl('10:00', 6, 5)