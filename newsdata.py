#!/usr/bin/env python

import psycopg2


def connect(db_name="news"):
    """Connect to the PostgreSQL database. Returns a database connection """
    try:
        db = psycopg2.connect("dbname={}".format(db_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Unable to connect to the database")


def popular_article():
    """Prints most popular three articles of all time"""
    db, cursor = connect()
    query = "select articles.title, count(*) as views \
    from articles join log on log.path \
    like concat('%', articles.slug) \
    where log.status like '%200%' group by \
    articles.title, log.path order by views desc limit 3"
    cursor.execute(query)
    result = cursor.fetchall()
    db.close()
    print "\nWhat are the most popular three articles of all time?\n"
    for i in range(0, len(result), 1):
        print str(i + 1) + ". \"" + result[i][0] + "\" has "\
            + str(result[i][1]) + " views"


def popular_authors():
    """Prints most popular article authors of all time"""
    db, cursor = connect()
    query = "select authors.name, count(*) as views from articles \
    join authors on articles.author = authors.id join log \
    on log.path like concat('/article/',articles.slug) where \
    log.status like '%200%' and articles.author = authors.id group \
    by authors.name order by views desc"
    cursor.execute(query)
    result = cursor.fetchall()
    db.close()
    print "\nWho are the most popular article authors of all time?\n"
    for i in range(0, len(result), 1):
        print str(i + 1) + ". \"" + result[i][0] + "\" has "\
            + str(result[i][1]) + " views"


def log_status():
    """Print days on which more than 1% of requests lead to errors"""
    db, cursor = connect()
    query = "select * from (select date(time),\
    round(100.0*sum(case when status like '%404%' then 1 else 0 end)/\
    count(status),3) as failure from log group\
    by date(time) order by failure desc) as result where failure > 1"
    cursor.execute(query)
    result = cursor.fetchall()
    db.close()
    print "\nOn which days did more than 1% of requests lead to errors?\n"
    for i in range(0, len(result), 1):
        print "On " + str(result[i][0]) + " it is found that the error is "\
            + str(result[i][1]) + "%\n"


if __name__ == '__main__':

    popular_article()
    popular_authors()
    log_status()
