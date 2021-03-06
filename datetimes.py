from datetime import datetime, timedelta, time
from pytz import common_timezones, timezone


""" common_timezones """
def getAllTimezones():
	return common_timezones


""" timezone, datetime """
def getCurrentDatetime():
	return timezone("UTC").localize(datetime.now())


""" datetime, time, timezone """
def getCommitDeadline(date):
	return timezone("UTC").localize(datetime.combine(date, time(0)))


""" getCurrentDatetime, timedelta """
def getCurrentCommitWeekMonday():
	# get the date right NOW
	# if before Friday's commit deadline:
	#		 its last monday
	# if after Friday's commit deadline:
	#		 its next monday
	now = getCurrentDatetime()

	friday = now.date() + timedelta(days=-now.weekday() + 4)

	if now < getCommitDeadline(friday):
		return now.date() + timedelta(days=-now.weekday())
	else:
		return now.date() + timedelta(days=-now.weekday() + 7)


""" timezone, datetime """
def calculateEmailTimestamp(date, userTimezone):
	datetimeToSend = timezone(userTimezone).localize(
		datetime.combine(date, time(7, 30))
	)
	return int(datetimeToSend.timestamp())


""" getCurrentCommitWeekMonday, timedelta """
# 29 Dec - 2 Jan
def getWeekToCommitToRange():
	monday = getCurrentCommitWeekMonday()
	friday = monday + timedelta(days=4)
	# Add monday's month if different to friday's
	extraMonth = " %b" if monday.month != friday.month else ""
	return monday.strftime("%-d" + extraMonth) + " - " + friday.strftime("%-d %b")


""" getCurrentCommitWeekMonday, getCurrentDatetime, Airtable, timedelta, getCommitDeadline """
# list of every weekday & its full date
def getCommitDayOptions():
	monday = getCurrentCommitWeekMonday()
	now = getCurrentDatetime()

	options = []
	for i in range(5):
		weekday = monday + timedelta(days=i)
		if now < getCommitDeadline(weekday):
			options.append({
				'date'	:	weekday.strftime("%A, %-d %b"),
				'value'	:	weekday.strftime("%A")
			})
	return options
