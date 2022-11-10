# Copyright (c) 2022, SOUL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import money_in_words

class PatientRefund(Document):
	def validate(self):
		self.net_refundable_in_words = money_in_words(self.net_refundable_in_figures)
