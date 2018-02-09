# Articles Analysis

This project uses Python to connect to the database of a newspaper and, using SQL, answer questions about the reader habits. It was created as part of Udacity's Intro to Programming Nanodegree program. Specifically, the program aims to answer the following questions:

1. What are the three most popular articles of all time?
2. Who are the most popular authors of all time?
3. On which days did more than 1% of web requests lead to errors?

## Installations and Configurations

The following steps are necessary to successfully run the program:

1. Access to a PostgresQL database system (psql 9.5.8 was used for testing)
2. Using the command line, launch psql and create a database 'news'
3. Download this [file](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip), which contains the schema and data for the 'news' database (created by Udacity instructors)
4. After unzipping the file, import 'newsdata.sql' into the 'news' database
5. Exit psql and run the python file 'articles_analysis.py' (python 2.7 is required to run the program)

## The Database

The database consists of the following tables and their corresponding columns (created by Udacity instructors):

articles (table):
- author (int)
- title (text)
- slug (text)
- lead (text)
- body (text)
- time (timestamp with time zone)
- id (int)

authors (table):
- name (text)
- bio (text)
- id (int)

log (table):
- path (text)
- ip (inet)
- method (text)
- status (text)
- time (timestamp with time zone)
- id (int)
