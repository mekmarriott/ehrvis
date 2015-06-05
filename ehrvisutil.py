# Author: Baris Ungun
# Description: timestamp conversion from Python datetime.date or datetime.datetime types to UTC integer

from time import mktime
import datetime 

def date2utc(timestamp):
	# return UTC time integer formatted to be in milliseconds
	if type(timestamp) is datetime.date:
		return 1000*mktime(timestamp.timetuple())
	else:
		return 1000*mktime(timestamp.date().timetuple())

