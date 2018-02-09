#!/usr/bin/env python2.7

import psycopg2
import datetime

views = [
    '''CREATE or REPLACE VIEW article_views as
      SELECT "path", count(*) as views
      FROM log
      GROUP BY "path";''',

    '''CREATE or REPLACE VIEW popularity_by_title as
      SELECT title, views
      FROM articles JOIN article_views
      on article_views.path LIKE ('%' || articles.slug)
      ORDER BY views DESC;''',

    '''CREATE or REPLACE VIEW articles_and_authors as
      SELECT name, title
      FROM articles JOIN authors
      on articles.author = authors.id;''',

    '''CREATE or REPLACE VIEW status_date_stamp as
      SELECT status, cast("time" as date) as "date"
      FROM log;''',

    '''CREATE or REPLACE VIEW errors_by_date as
      SELECT "date", count(status) as errors
      FROM status_date_stamp
      WHERE status NOT LIKE '%OK%'
      GROUP BY "date"
      ORDER BY "date";''',

    '''CREATE or REPLACE VIEW requests_by_date as
      SELECT "date", count(status) as num
      FROM status_date_stamp
      GROUP BY "date"
      ORDER BY "date";''',

    '''CREATE or REPLACE VIEW raw_error_rates as
      SELECT E.date,
      (cast(E.errors as decimal)/cast(R.num as decimal)) as error_rate
      FROM errors_by_date as E JOIN requests_by_date as R
      on E.date = R.date;'''
]


def create_views(new_views):
    try:
        conn = psycopg2.connect(dbname="news")
        cursor = conn.cursor()
        for view in new_views:
            cursor.execute(view)
            conn.commit()
        conn.close()
    except psycopg2.Error as error:
        print error
        sys.exit(1)


def fetch_data(query):
    '''
    Connect to 'news' database and print results of SQL queries
    '''
    try:
        conn = psycopg2.connect(dbname="news")
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
    except psycopg2.Error as error:
        print error
        sys.exit(1)

top_three_articles = "SELECT * FROM popularity_by_title LIMIT 3;"

author_popularity = '''SELECT name, sum(views) as total_views
                     FROM articles_and_authors as A
                     JOIN popularity_by_title as P
                     on A.title = P.title
                     GROUP BY name
                     ORDER BY total_views DESC;'''

high_error_days = '''SELECT "date",
                   cast(error_rate*100 as decimal(4,2)) as rounded_error_rate
                   FROM raw_error_rates
                   WHERE error_rate*100 > 1;'''


def top_articles():
    results = fetch_data(top_three_articles)
    print "\nThe top 3 most popular articles are:\n"
    for title, views in results:
        print '\"{}\" - {} views'.format(title, views)
    print


def top_authors():
    results = fetch_data(author_popularity)
    print "\nTotal views by author:\n"
    for name, total_views in results:
        print '{} - {} views'.format(name, total_views)
    print


def high_error_rates():
    results = fetch_data(high_error_days)
    print "\nDates with an error rate greater than 1%:\n"
    for date, rounded_error_rate in results:
        print datetime.datetime.strptime(str(date), '%Y-%m-%d') \
         .strftime('%B %d, %Y') + " - " + str(rounded_error_rate) + " %"
    print

if __name__ == '__main__':
    create_views(views)
    top_articles()
    top_authors()
    high_error_rates()
