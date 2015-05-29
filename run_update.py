import sys
import Util

from datetime import date, timedelta
from peewee import *

"""
Setup connection to database and create Models (i.e. Tables)
"""
db = MySQLDatabase(Util.DB_NAME, user=Util.USERNAME, passwd=Util.PASSWORD)

# Mailing table - contains the email addresses
class Mailing(Model):
   addr = CharField(primary_key=True)

   class Meta:
      database = db

# Domain table - contains the domain, count and the date the count was changed
class Domain(Model):
   name = CharField()
   count = IntegerField()
   date = DateField()

   class Meta:
      database = db


"""
Connect to database and create neccessary tables
"""
def setup():
   db.connect()
   db.create_tables([Mailing, Domain], safe=True)


"""
Disconnect from database
"""
def teardown():
   db.close()


"""
Process all addr in mailing table and 
store their domain counts in a dictionary 
"""
def getDomainCounts():
   domains = {}
   for mailing in Mailing.select():
      user, sep, domain = mailing.addr.lower().partition("@")

      if domain in domains:
         domains[domain] += 1
      else:
         domains[domain] = 1

   return domains


"""
Create a new entry if the count has changed compared to the previously 
latest entry
"""
def updateDomainTable(dateToday):
   domains = getDomainCounts()
   for domain in domains:
      count = domains[domain]

      if not Domain.select().where(Domain.name == domain).exists():
         Domain.create(name=domain, count=count, date=dateToday)
      else:
         mostRecentEntry = Domain.select().where(Domain.name == domain)\
            .order_by(-Domain.date).first()

         if mostRecentEntry.count != count:
            Domain.create(name=domain, count=count, date=dateToday)


"""
Remove entries older than 30 days
"""
def removeOldEntries(dateToday):
   d30DaysAgo = dateToday - timedelta(days=30)

   query = Domain.select().where(Domain.date < d30DaysAgo)
   if query.exists():
      print 'Removing entries older than', d30DaysAgo
   for domain in query:
      print 'Removed: ', domain.name, domain.count, domain.date

   query = Domain.delete().where(Domain.date < d30DaysAgo)
   query.execute()


"""
Top 50 domains by count sorted by percentage growth of the last 30 days
compared to the total
"""
def getTop50Domains():
   top50 = []
   query = Domain.select().order_by(-Domain.count)\
      .group_by(Domain.name).limit(50)
   for domain in query:
      subQuery = Domain.select().where(Domain.name == domain.name) \
         .order_by(-Domain.date)

      (newestEntry, oldestEntry) = Util.getFirstAndLastItem(subQuery)

      growth = None
      if newestEntry.date == oldestEntry.date:
         growth = 0
      else:
         growth = int(((newestEntry.count - oldestEntry.count) \
            / float(oldestEntry.count)) * 100)

      top50.append((domain.name, newestEntry.count, growth))

   top50.sort(key=lambda x: x[2], reverse=True)
   return top50


"""
Drop the tables. Used during testing.
"""
def dropAllTables():
   db.connect()
   Mailing.drop_table()
   Domain.drop_table()
   db.close()

"""
Does all the work. Is also called through tests.py.
"""
def main(dateToday=date.today()):
   setup()
   updateDomainTable(dateToday)
   removeOldEntries(dateToday)
   Util.prettyPrint(getTop50Domains())
   teardown()

if __name__ == '__main__':
   main()