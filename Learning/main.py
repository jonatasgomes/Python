import nasdaqdatalink
mydata = nasdaqdatalink.get_table('ZACKS/FC', ticker='AAPL')
print(mydata)
