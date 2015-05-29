## Problem
Given a table 'mailing':

CREATE TABLE mailing (
	addr VARCHAR(255) NOT NULL
);

The mailing table will initially be empty.  New addresses will be added on a daily basis.  It is expected that the table will store at least 10,000,000 email addresses and 100,000 domains.

Write a Python script that updates another table which holds a daily count of email addresses by their domain name.

Use this table to report the top 50 domains by count sorted by percentage growth of the last 30 days compared to the total.

** NOTE **

- The original mailing table should not be modified.

- All processing must be done in Python (eg. no complex queries or sub-queries)

- Submit a compressed file(tar/zip) with the files required to run your script.


## Solution
The following assumptions were made for the solution:
- "percentage growth of the last 30 days compared to the total" meant that
the percentage growth for a domain would be the increase/decrease in the last 30 days over the total initial count. (see Example 2 below)
- the second table can contain an additional date column

This solution utilizes the peewee ORM (a small and simple Object-relational 
mapping library for MySQL). peewee can be obtained from: 
http://peewee.readthedocs.org/en/latest/index.html# or by running "pip install peewee".

# Util.py
This file contains:
- the credentials for the database
- a simple function to get the first and last element in a data set
- a function to format and print the final solution

# handle_addresses.py
This file handles adding and removing addrs from the Mailing table.

# run_update.py
This file contains the main solution to the problem.
It begins be creating the Mailing and Domain Model classes, which represent the
corresponding tables. A connection to the database is then created and the 
tables are creates if necessary. 

The Domain table is where the domain counts are stored with their respective dates. A domain name and count entry is only created if there is no previous 
count or the count has changed. This means that the upper bound to the table 
size would be 100,000 * 30 rows while the lower bound would be 100,000. 
Because the probability of new addrs from all domains being added is low, we
will likely never use 100,000 * 30 rows.

> Example 1:
+----+-------------+-------+------------+
| id | name        | count | date       |
+----+-------------+-------+------------+
|  3 | gmail.com   |     1 | 2015-05-28 |
|  4 | yahoo.com   |     3 | 2015-05-29 |
|  5 | yahoo.com   |     6 | 2015-05-30 |
+----+-------------+-------+------------+

During each update, entries older than 30 days are deleted since they no longer
effect the final output.

To get the top 50 domains by count, a MySQL query is used. This query sorts 
the rows in descending order by count, while grouping rows with the same 
domain name. Then using the LIMIT feature, the top 50 rows are obtained.

To get the percentage growth for each top 50 domain, the difference between
the newest and oldest count is obtained and then divided by the oldest count.

> Example 2:
Using the table from Example 1 above, we can see that the oldest entry for
yahoo.com has a count of 3 and the newest entry has a count of 6.

6-3
___ x 100 = 100%
3

Therefore, yahoo.com had a percentage growth of 100% in the last 30 days. Note 
that if the oldest entry was older than 30 days, it would have been removed. 
In that case, the growth would be 0%, as would be the case for gmail.com.

# tests.py
This file contains several tests, each with a description. The file tests
things such as sanity test, negative growth, sorting by growth, load test, etc.

To run the tests, execute the following line:
python test.py

Alternatively, you can view the sample output in tests_output.txt

Note: the addresses for the load test were obtained from http://www.sistersofspam.co.uk/Scam_Email_Addresses_1.php
