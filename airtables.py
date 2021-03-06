from os import environ
from time import sleep as time_sleep

from airtable import Airtable as AirtablePythonWrapper

from constants import DEBUG_MODE


class Airtable(AirtablePythonWrapper):
  def __init__(self, tableName):
    if tableName == "Participants":
      self._table = "Seyhan's testing group" if DEBUG_MODE else "Members"
    else:
      self._table = tableName

    super().__init__(
      environ.get('AIRTABLE_LINKEDIN_TABLE'),
      self._table,
      environ.get('AIRTABLE_KEY')
    )

  def time_sleep(self):
    time_sleep(self.API_LIMIT)

  def delete_all(self):
    self.batch_delete([record['id'] for record in self.get_all()])

  def update_all(self, fields):
    for row in self.get_all():
      self.update(row['id'], fields)
      self.time_sleep()

  def batch_update_by_field(self, column, recordsToUpdate):
    for ID in recordsToUpdate:
      self.update_by_field(column, ID, recordsToUpdate[ID])
      self.time_sleep()
