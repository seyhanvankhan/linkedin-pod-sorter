from datetime import datetime
from pytz import timezone

from airtable import Airtable

PEOPLE_TABLE = "Members"
DAYS = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']


currentDate = datetime.now(timezone("UTC")).date()


airtableParticipants = Airtable(environ.get('AIRTABLE_LINKEDIN_TABLE'), PEOPLE_TABLE, environ.get('AIRTABLE_KEY'))
participants = {
	row['fields']['ID'] : row['fields'] for row in airtableParticipants.get_all(
		fields=[
			 'ID','Name','Email','LinkedIn Profile','Day Preference','Time Zone','Group'
		]
	)
}


#################################### SUNDAY ####################################

# Runs every Sunday, 07:30 UTC
if currentDate.weekday() == DAYS.index('Sunday'):
	monday = currentDate + timedelta(days=1)
	friday = currentDate + timedelta(days=5)
	# Add monday's month if different to friday's
	extraMonth = " %b" if monday.month != friday.month else ""
	nextWeekRange = monday.strftime("%-d" + extraMonth) + " - " + friday.strftime("%-d %b")

	emails = []
	for participant in participants.values():
    emails.append(Email(
      to=participant["Email"],
			subject="Are you participating next week? ("+nextWeekRange+") | LinkedIn Pod Sorter",
			html=render_template(
				"emails/commit.html",
				name=participant["Name"],
				userHash=hashID(participant["ID"], participant["Name"]),
				nextWeekRange=nextWeekRange,
			)
		))


############################### MONDAY to FRIDAY ###############################

# Runs Mon-Fri, at 07:30 UTC
if currentDatetime.weekday() < 5:
	groups = {}
	for participant in participants.values():
		if "Day Preference" not in person:
			continue

		for group in participant['Group']:
			if currentDatetime.strftime("%A") in participant['Day Preference']
			if group in groups:
				if day in groups[group]:
					groups[group][day].append(person)
				else:
					groups[group][day] = [person]
			else:
				groups[group] = {day: [person]}

	pairs = generateAllPairsAndTimestamps(groups, participants)

	addPairsToAirtable(pairs)

	emails = createParticipantEmails("Sunday", render_template, pairs, participants)
	emails.extend(createNonParticipantEmails(render_template, participants))

	# now send each email
	# if error occurs, output & stop sending emails
	for email in emails:
		sendEmail(email)
		break
		print(sendEmail(email))


	# make everyone now OPTED OUT
	# if they want to opt back in, they will need to click link in email
	optOutEveryone(airtableParticipants)





# ##################### EMAIL ROUTE TO BE OPENED EVERY WEEK ######################
#
#
# """
# TIMELINE:
# Sunday, 19:00 UTC
# 		All pairs are calculated
# 		Pairs IDs saved on Airtable 'Emails' table
# 		Timestamp is saved for any emails to be sent AFTER 1900 Wednesday - THE CUTOFF
# 		Send all scheduled emails due within range:
# 			First email sent Sunday, 19:30 UTC (New Zealand)
# 			Last email sent Wednesday, 18:59 UTC
#
# Wednesday, 18:00 UTC
# 		Get remaining pairs & timestamps from airtable (only get rows with timestamps)
# 		Send all remaining scheduled emails up to Saturday 17:59 UTC
# 		last email is sent at Friday 17:30 UTC (Hawaii)
# """
#
# # runs at Sunday 19:00 UTC
# # covers Sunday 19:00 UTC to Wednesday 18:59 UTC
# # first email is sent Sunday 19:30 UTC (New Zealand)
# @app.route('/sunday/')# + environ.get('EMAIL_CODE'), methods=['POST'])
# def weeklyEmailCalculation_Sunday():
# 	# get list of participants
# 	airtableParticipants = Airtable(environ.get('AIRTABLE_LINKEDIN_TABLE'), PEOPLE_TABLE, environ.get('AIRTABLE_KEY'))
# 	participants = {
# 		row['fields']['ID'] : row['fields'] for row in airtableParticipants.get_all(
# 			fields=[
# 				'ID','Name','Email','LinkedIn Profile','Day Preference','Time Zone','Group'
# 			]
# 		)
# 	}
#
# 	groups = {}
# 	for person in participants.values():
# 		if "Opted In" not in person:
# 			continue
# 		for group, day in product(person['Group'], person['Day Preference']):
# 			if group in groups:
# 				if day in groups[group]:
# 					groups[group][day].append(person)
# 				else:
# 					groups[group][day] = [person]
# 			else:
# 				groups[group] = {day: [person]}
#
# 	pairs = generateAllPairsAndTimestamps(groups, participants)
#
# 	addPairsToAirtable(pairs)
#
# 	emails = createParticipantEmails("Sunday", render_template, pairs, participants)
# 	emails.extend(createNonParticipantEmails(render_template, participants))
#
# 	# now send each email
# 	# if error occurs, output & stop sending emails
# 	for email in emails:
# 		sendEmail(email)
# 		break
# 		print(sendEmail(email))
#
#
# 	# make everyone now OPTED OUT
# 	# if they want to opt back in, they will need to click link in email
# 	optOutEveryone(airtableParticipants)
#
# 	return redirect("/")
#
#
# ################################### WEDNESDAY ##################################
#
#
# # runs at Wednesday 18:00 UTC
# # covers Wednesday 19:00 UTC to Saturday 17:59 UTC
# # last email is sent at Friday 17:30 UTC (Hawaii)
# @app.route('/wednesday/' + environ.get('EMAIL_CODE'), methods=['POST'])
# def weeklyEmailCalculation_Wednesday():
# 	# get list of participants
# 	airtableParticipants = Airtable(environ.get('AIRTABLE_LINKEDIN_TABLE'), PEOPLE_TABLE, environ.get('AIRTABLE_KEY'))
# 	participants = {
# 		row['fields']['ID'] : row['fields'] for row in airtableParticipants.get_all(
# 			fields=[
# 				'ID','Name','Email','LinkedIn Profile'
# 			]
# 		)
# 	}
# 	airtablePairs = Airtable(environ.get('AIRTABLE_LINKEDIN_TABLE'), 'Emails', environ.get('AIRTABLE_KEY'))
# 	pairs = [
# 		{
# 			'ID' : 								row['fields']['ID'],
# 			'Profiles' : 				 	[int(id) for id in row['fields']['Profiles'].split(",")],
# 			'Profiles Assigned' : [int(id) for id in row['fields']['Profiles Assigned'].split(",")],
# 			"Timestamp" : 				row['fields']['Timestamp']
# 		} for row in airtablePairs.get_all()
# 	]
#
# 	emails = createParticipantEmails("Wednesday", render_template, pairs, participants)
# 	# now send each email
# 	# if error occurs, output & end the function
# 	for email in emails:
# 		print(sendEmail(email))
#
# 	return redirect('/')
