from random import shuffle

from airtables import Airtable
from constants import MAX_PROFILES_PER_PERSON
from datetimes import calculateEmailTimestamp, getCurrentDatetime, getWeekToCommitToRange
from emails import *

currentDate = getCurrentDatetime().date()
# if today is Saturday, nothing to do, just exit program
if currentDate.weekday() == 5:
	exit()

airtablePairs = Airtable('Emails')
airtableParticipants = Airtable("Participants")
participants = {
	row['fields']['ID'] : row['fields'] for row in airtableParticipants.get_all(
		fields=[
			 'ID','Name','Email','LinkedIn Profile','Day Preference','Time Zone','Group'
		]
	)
}


#################################### SUNDAY ####################################


# Runs Sun, at 0000
if currentDate.weekday() == 6:
	# clear everyone's day choice from last Mon-Fri
	airtableParticipants.update_all({"Day Preference": []})

	# clear every row from 'Emails' table
	airtablePairs.delete_all()

	sendCommitEmails(
		participants,
		calculateEmailTimestamp(currentDate, 'UTC'),
		getWeekToCommitToRange()
	)


############################### MONDAY to FRIDAY ###############################


# Runs Mon-Thu, at 0000
if currentDate.weekday() < 5:
	groups = {}
	for participant in participants.values():
		# if participant picked no days, skip em
		if "Day Preference" not in participant:
			continue
		# if today was NOT one of this participant's choices, skip em
		if currentDate.strftime("%A") not in participant['Day Preference']:
			continue

		if participant['Group'] in groups:
			groups[participant['Group']].append(participant)
		else:
			groups[participant['Group']] = [participant]


	allPairs = []
	for group in groups:
		numParticipants = len(groups[group])
		shuffle(groups[group])

		# range of numbers from 1 to max profiles per person
		# 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
		profilePairIndices = range(1, min(MAX_PROFILES_PER_PERSON, numParticipants - 1) + 1)

		groupPairs = []
		# for each participant
		for participantIndex in range(numParticipants):
			groupPairs.append(
				{
					"ID": groups[group][participantIndex]["ID"],
					"Profiles": [
						groups[group][(participantIndex + i) % numParticipants]["ID"] for i in profilePairIndices
					],
					"Profiles Assigned": [
						groups[group][(participantIndex - i) % numParticipants]["ID"] for i in profilePairIndices
					],
					"Timestamp": calculateEmailTimestamp(
						currentDate,
						groups[group][participantIndex]["Time Zone"]
					)
				}
			)
		allPairs.extend(groupPairs)

	sendProfilesEmail(
		participants,
		allPairs,
		currentDate.strftime("%-d %b")
	)

	# add pairs to Emails table (formatted to strings)
	airtablePairs.batch_insert([
		{
			"ID" : row["ID"],
			"Profiles" : ','.join(str(i) for i in row["Profiles"]),
			"Profiles Assigned" : ','.join(str(i) for i in row["Profiles Assigned"]),
			"Timestamp" : row["Timestamp"]
		} for row in allPairs
	])

# First email is sent Sunday, 18:30 UTC (New Zealand)
# Last email is sent Friday, 17:30 UTC (Hawaii)
