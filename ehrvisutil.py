from time import mktime
import datetime 

def date2utc(timestamp):
	if type(timestamp) is datetime.date:
		return 1000*mktime(timestamp.timetuple())
	else:
		return 1000*mktime(timestamp.date().timetuple())

