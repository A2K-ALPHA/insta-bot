import datetime


def days_since_date(n):
    n = datetime.datetime.strptime(n, '%Y-%m-%d')

    diff = datetime.datetime.now().date() - n.date()
    return diff.days