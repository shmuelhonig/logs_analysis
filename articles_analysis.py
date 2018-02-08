#!/usr/bin/env python2.7

import psycopg2
import datetime


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

top_three_articles = "SELECT * from popularity_by_title limit 3;"

author_popularity = '''SELECT name, sum(views) as total_views
                     from articles_and_authors as A
                     join popularity_by_title as P
                     on A.title = P.title
                     group by name
                     order by total_views desc;'''

high_error_days = '''SELECT "date",
                   cast(error_rate*100 as decimal(4,2)) as rounded_error_rate
                   from raw_error_rates
                   where error_rate*100 > 1;'''

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
    top_articles()
    top_authors()
    high_error_rates()
