import sys
import run_update
import handle_addresses

from datetime import date, timedelta

EMPTY_TEST_FILE = 'address_files/empty.txt'
LOAD1_TEST_FILE = 'address_files/load1.txt'
LOAD2_TEST_FILE = 'address_files/load2.txt'

"""
In this test we add no addresses to the Mailing table.

Purpose: to test whether run_update.py can handle the boundary case
when no entries exist in Mailing table.

Expected output: No exceptions should occur and the top domain list should be
empty.
"""
def emptyTest():
   print '########## tests.emptyTest() ##########'

   d = date.today()
   print d
   handle_addresses.addFromFile(EMPTY_TEST_FILE)
   run_update.main(d)

   print '\n\n'
   teardown()

"""
In this test we add a new addr for the same domain. 
The first addr is added on 2015-1-1 and the second addr is added on 2015-1-2. 
This is test the lower boundary for when an address is added the next day.

Another addr for the same domain will be added 30 days later, which should 
still be okay because we should include up to thirty days.

The last addr will be added after 31 days. This means the very first entry 
should no longer be considered.

Purpose: to test the upper and lower boundaries for the dates when 
addrs are added. 

Expected output: No exceptions should occur.
The output for the first entry should have a growth = 0
The output for the second entry should have a growth = 100
The output for the third entry should have a growth = 200
The output for the fourth entry should have a growth = 100
"""
def sanityCheck():
   print '########## tests.sanityCheck() ##########'

   d = date(2015, 1, 1)
   print d
   addrs = {'20150101@example.com'}
   handle_addresses.addFromSet(addrs)
   run_update.main(d)

   print '\n'
   d = date(2015, 1, 2)
   print d
   addrs = {'20150102@example.com'}
   handle_addresses.addFromSet(addrs)
   run_update.main(d)

   print '\n'
   d = date(2015, 1, 31)
   print d
   addrs = {'20150130@example.com'}
   handle_addresses.addFromSet(addrs)
   run_update.main(d)

   print '\n'
   d = date(2015, 2, 1)
   print d
   addrs = {'20150201@example.com'}
   handle_addresses.addFromSet(addrs)
   run_update.main(d)

   print '\n\n'
   teardown()

"""
In this test we add a large number of new addrs on two dates less than 30
days apart.

Purpose: to test whether large addrs behave as expected.

Expected output: No exceptions should occur.
For the first update, the growth for all the domain names should be 0 and the 
top domain should be gmail.com

For the second update, the growth should be non-zero for most domain names, 
the domain names should be sorted by growth and the top domain should be 
mit.tc with a growth of 250 and a count of 7.
"""
def loadTest():
   print '########## tests.sanityCheck() ##########'

   d = date.today() - timedelta(days=30)
   print d
   handle_addresses.addFromFile(LOAD2_TEST_FILE)
   run_update.main(d)

   print '\n'
   d = date.today()
   print d
   handle_addresses.addFromFile(LOAD1_TEST_FILE)
   run_update.main(d)

   print '\n\n'
   teardown()


"""
In this test we test whether only entries older than 30 days are removed.
This is done by adding a large set of addrs 31 days before today. 
Then adding another small set of addrs a few days before today.
Lastly, another small of addrs are added with todays date.

Purpose: to verify that only extries older than 30 days are removed.

Expected output: No exceptions should occur.
For the first update, the growth for all the domain names should be 0 and the 
top domain should be gmail.com.

After athe second update, the growth for all the domain names should still be 
0 but we should now see example1.com and example.com in the list.

After the third update, all entries from 31 days ago should be deleted. And 
only entries for example1.com and example.com should remain.

Because three new example1.com domain name addrs were added, the growth should
be 100%. Whereas, only one new example.com domain name was added, so the growth
should be 33%
"""
def thirtyDayTest():
   print '########## tests.thirtyDayTest() ##########'

   d = date.today() - timedelta(days=31)
   print d
   handle_addresses.addFromFile(LOAD1_TEST_FILE)
   run_update.main(d)

   print '\n'
   d = date.today() - timedelta(days=5)
   print d
   addrs = {'1@example.com', '2@example.com', '3@example.com',\
            '1@example1.com', '2@example1.com', '3@example1.com'}
   handle_addresses.addFromSet(addrs)
   run_update.main(d)

   print '\n'
   d = date.today() 
   print d
   addrs = {'4@example.com',\
         '4@example1.com', '5@example1.com', '6@example1.com'}
   handle_addresses.addFromSet(addrs)
   run_update.main(d)

   print '\n\n'
   teardown()


"""
In this test we check whether negative growth percentage is handled correctly.

Purpose: Check that the growth percentage can be negative.

Expected Output: No exceptions should occur.
After the first update, the growth should be 0 for both domains.

After the second update, the growth for example.com should be -33 percent
and -66 for example1.com. -33 should be sorted higher than -66.
"""
def negativeGrowthTest():
   print '########## tests.negativeGrowthTest() ##########'

   d = date.today() - timedelta(days=5)
   print d
   addrs = {'1@example.com', '2@example.com', '3@example.com',\
            '1@example1.com', '2@example1.com', '3@example1.com'}
   handle_addresses.addFromSet(addrs)
   run_update.main(d)

   print '\n'
   addrs = {'1@example.com',\
            '1@example1.com', '2@example1.com'}
   handle_addresses.removeFromSet(addrs)
   d = date.today() 
   print d
   handle_addresses.addFromSet({})
   run_update.main(d)

   print '\n\n'
   teardown()


def teardown():
   run_update.dropAllTables()


if __name__ == '__main__':
   emptyTest()
   sanityCheck()
   loadTest()
   thirtyDayTest()
   negativeGrowthTest()