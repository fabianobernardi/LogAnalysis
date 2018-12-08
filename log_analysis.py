#! /usr/bin/python3

# -*- coding: utf-8 -*-

import newsdb
from datetime import datetime

questions = {1: '\n1. Quais são os três artigos mais populares de todos os '
                'tempos?',
             2: '\n2. Quem são os autores de artigos mais populares de todos '
                'os tempos?',
             3: '\n3. Em quais dias mais de 1% das requisições resultaram em '
                'erros?'}


def pretty_print_console(question, data, descr):
    print(questions[question])
    for item in data:
        data, value = item
        if descr == 'views':
            print('-> {} -- {} {}'.format(data, value, descr))
        if descr == 'errors':
            value = round(value, ndigits=2)
            print('-> {} -- {}% {}'.format(datetime.strftime(data, '%d/%m/%Y'),
                                           value, descr))


def pretty_print_file(question, data, descr):

    fileout = open('result.txt', 'a')

    fileout.writelines(questions[question] + '\n')
    for item in data:
        data, value = item
        if descr == 'views':
            fileout.writelines('-> {} -- {} {}\n'.format(data, value, descr))
        if descr == 'errors':
            value = round(value, ndigits=2)
            fileout.writelines('-> {} -- {}% {}\n'.format(
                datetime.strftime(data, '%d/%m/%Y'),
                value,
                descr))
    fileout.close()


if __name__ == '__main__':

    top_3_articles = newsdb.get_top_articles()
    pretty_print_console(1, top_3_articles, 'views')
    pretty_print_file(1, top_3_articles, 'views')

    popular_authors = newsdb.get_most_popular_authors()
    pretty_print_console(2, popular_authors, 'views')
    pretty_print_file(2, popular_authors, 'views')

    errors_percent = newsdb.get_errors_percent()
    pretty_print_console(3, errors_percent, 'errors')
    pretty_print_file(3, errors_percent, 'errors')
