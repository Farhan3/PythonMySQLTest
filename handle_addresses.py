import sys
import Util

from peewee import *


"""
Setup connection to database and create Models (i.e. Tables)
"""
db = MySQLDatabase(Util.DB_NAME, user=Util.USERNAME, passwd=Util.PASSWORD)

class Mailing(Model):
   addr = CharField(primary_key=True)

   class Meta:
      database = db


"""
Connect to database and create neccessary tables
"""
def setup():
   db.connect()
   db.create_tables([Mailing], safe=True)


"""
Disconnect from database
"""
def teardown():
   db.close()


"""
Read the addresses from the specified file.
Note: one address per line in the form name@domain
"""
def readAddresses(file):
   new_addresses = []
   with open(file) as addrFile:
      for line in addrFile:
         new_addresses.append(line.strip())
   return new_addresses


"""
Format the set of addresses. Required because peewee has a optimized method
for inserting many rows.
"""
def formatAddresses(setOfAddr):
   new_addresses = []
   for item in set(setOfAddr):
      new_addresses.append({'addr': item})

   return new_addresses


"""
Add the provided addresses to the Mailing table
"""
def addAddressesToTable(setOfAddr):
   addresses = formatAddresses(setOfAddr)

   with db.atomic():
      for data_dict in addresses:
         addr = data_dict['addr']
         if not Mailing.select().where(Mailing.addr == addr).exists():
            Mailing.create(**data_dict)

"""
Remove the specified addresses from the Mailing table
"""
def removeAddressesFromTable(setOfAddr):
   for addr in setOfAddr:
      query = Mailing.select().where(Mailing.addr == addr)
      if query.exists():
         query = Mailing.delete().where(Mailing.addr == addr)
         query.execute()

"""
Read addresses from file and add them to the Mailing table.
"""
def addFromFile(file):
   setup()
   addresses = readAddresses(file)
   addAddressesToTable(addresses)
   db.close()


"""
Read addresses from the provided set of strings and add them to the 
Mailing table.
"""
def addFromSet(addresses):
   setup()
   addAddressesToTable(addresses)
   db.close()

def removeFromSet(addresses):
   setup()
   removeAddressesFromTable(addresses)
   db.close()