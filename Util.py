import sys

DB_NAME = 'index_exchange'
USERNAME = 'index_exchange'
PASSWORD = 'password'

"""
Get the first and last item of the datastructure
"""
def getFirstAndLastItem(data):
   firstItem = None
   lastItem = None

   for lastItem in data:
      if firstItem is None:
         firstItem = lastItem

   return (firstItem, lastItem)


"""
Print the results
"""
def prettyPrint(top50):
   print '   +--------------------+-------+------------+'
   print '   |        name        | count | %  growth  |'
   print '   +--------------------+-------+------------+'
   spaces = '                                       '

   i = 1;
   for item in top50:
      name = item[0]
      count = item[1]
      growth = item[2]
      print i, ' ', name, spaces[:(18 - len(str(name)))], \
         ' ', count, spaces[:(5 - len(str(count)))], \
         ' ', growth, spaces[:(10 - len(str(growth)))]
      i += 1