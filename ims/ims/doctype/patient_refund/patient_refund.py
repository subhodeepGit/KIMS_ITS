# Copyright (c) 2022, SOUL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import money_in_words

class PatientRefund(Document):
	def validate(self):
		# self.net_refundable_in_figures=(self.amount_deposited_by_patient - self.approval_of_tpa__insurance__corporate__ostf - self.cash_refund - self.total_bill - self.approval_of_tpa__insurance__corporate__ostf - self.less__non_admissible_item__discount_amount)
		self.net_refundable_in_words = money_in_words(self.net_refundable_in_figures)
