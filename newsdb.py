#! /usr/bin/python3

# -*- coding: utf-8 -*-


import psycopg2


TOP_3_ARTICLES = """
SELECT articles.title,
       total_views
FROM articles,
    (SELECT split_part(log.PATH, '/article/', 2) AS article,
            count(*) AS total_views
    FROM log
    WHERE log.PATH != '/'
      AND log.status = '200 OK'
    GROUP BY split_part(log.PATH, '/article/', 2)
    ORDER BY total_views DESC
    LIMIT 3) AS subquery
WHERE articles.slug = article
ORDER BY total_views DESC"""

MOST_POPULAR_AUTHORS = """
SELECT authors.name,
       count(*) AS total
FROM authors
LEFT JOIN articles ON authors.id = articles.author
LEFT JOIN log ON articles.slug = split_part(log.path, '/article/', 2)
AND log.path != '/'
AND log.status = '200 OK'
GROUP BY authors.name
ORDER BY 2 DESC"""

ERRORS_PERCENT = """
SELECT dia,
       (total_erros/total_dia::float)*100 AS "porcento"
FROM
    (SELECT log1.time::timestamptz::date AS dia,
            log1.total_dia,
            log2.total_erros
    FROM
        (SELECT TIME::timestamptz::date,
                count(*) AS "total_dia"
        FROM log
        GROUP BY TIME::timestamptz::date) log1
    LEFT JOIN
        (SELECT TIME::timestamptz::date,
                count(*) AS "total_erros"
        FROM log
        WHERE status = '404 NOT FOUND'
        GROUP BY TIME::timestamptz::date) log2
    ON (log1.time::timestamptz::date = log2.time::timestamptz::date)) subq
WHERE (total_erros/total_dia::float)*100 > 1
ORDER BY dia"""


def get_top_articles():
    try:
        db_conn = psycopg2.connect('dbname=news')
        db_cursor = db_conn.cursor()
        db_cursor.execute(TOP_3_ARTICLES)
        top_articles = db_cursor.fetchall()
        db_conn.close()
        return top_articles
    except psycopg2.Error as error:
        print('Oops, não consegui coletar a informação')
        pass


def get_most_popular_authors():
    try:
        db_conn = psycopg2.connect('dbname=news')
        db_cursor = db_conn.cursor()
        db_cursor.execute(MOST_POPULAR_AUTHORS)
        popular_authors = db_cursor.fetchall()
        db_conn.close()
        return popular_authors
    except psycopg2.Error as error:
        print('Oops, não consegui coletar a informação')
        pass


def get_errors_percent():
    try:
        db_conn = psycopg2.connect('dbname=news')
        db_cursor = db_conn.cursor()
        db_cursor.execute(ERRORS_PERCENT)
        errors_percent = db_cursor.fetchall()
        db_conn.close()
        return errors_percent
    except psycopg2.Error as error:
        print('Oops, não consegui coletar a informação')
        pass
