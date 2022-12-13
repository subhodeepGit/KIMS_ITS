# Copyright (c) 2022, SOUL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class InvoiceReceival(Document):
	def validate(self):
		self.db_set("invoice_status","Draft")

	def on_submit(self):
		self.db_set("invoice_status","Passed for Notesheet")

	def on_cancel(self):
		self.db_set("invoice_status","Cancelled")
		if self.note_no!="":
			frappe.throw("Data link with <b>{0}</b> NoteSheet, Unlink data before <b>Cancel</b>".format(self.get('note_no')))