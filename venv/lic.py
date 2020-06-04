# -*- coding: utf-8 -*-
from lxml import etree
import csv


def csv_writer(path, fieldnames, data):
    """
    Функция для записи в файл csv
    path - путь до файла
    fieldnames - название столбцов
    data - список из списков
    """
    with open(path, "a", newline='') as out_file:
        '''
        out_file - выходные данные в виде объекта
        delimiter - разделитель :|;
        fieldnames - название полей (столбцов)
        '''
        writer = csv.DictWriter(out_file, delimiter=';', fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


if __name__ == "__main__":
    data = []
    elem_list = []
    tags_list = []

    inner_dict = {}

    path = "license_output.csv"
    deep = 0
    iter = 0

    # формирование списка tag-ов для заголовков
    for event, element in etree.iterparse("data.xml"):
        tags_list.append(element.tag)
        deep = deep + 1
        if deep > 26:
            break

    for event, element in etree.iterparse("data.xml"):
        #tags_list.append(element.tag)
        elem_list.append(element.text)
        deep = deep + 1
        element.clear()
        if deep > 26:
            inner_dict = dict(zip(tags_list, elem_list))
            data.append(inner_dict)
            deep = 0
            elem_list.clear()
            if len(data) == 1000:
                csv_writer(path, tags_list, data)
                data.clear()
                iter += 1
                print(f'Пройдено {iter} итераций')
                #break

    print(len(data))
    csv_writer(path, tags_list, data)
    #data.clear()
    print(f'Загружены оставшиеся {len(data)} строк')

    print('WOW!')