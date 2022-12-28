# Copyright (c) 2022, SOUL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class InvoiceReceival(Document):
	# def after_insert(self):
	# 	self.add_user_permission()

	def validate(self):
		self.db_set("invoice_status","Draft")

	def on_submit(self):
		self.db_set("invoice_status","Passed for Notesheet")

	def on_cancel(self):
		# self.delete_user_permission()
		self.db_set("invoice_status","Cancelled")
		if self.batch_payment_no!="" and self.batch_payment_no!=None:
			frappe.throw("Data link with <b>{0}</b> Batch Payment Process, Unlink data before <b>Cancel</b>".format(self.get('batch_payment_no')))
		if self.note_no!="" and self.note_no!=None:
			frappe.throw("Data link with <b>{0}</b> NoteSheet, Unlink data before <b>Cancel</b>".format(self.get('note_no')))
		
	# def add_user_permission(self):
	# 	session_user = frappe.session.user
	# 	if session_user:
	# 		data = frappe.get_all("User Permission",{"user":session_user},["allow","for_value"])
	# 		if data:
	# 			if data[0]["allow"]==self.doctype and data[0]["for_value"]==self.name:
	# 				pass
	# 			else:
	# 				frappe.get_doc(dict(
	# 					doctype="User Permission",
	# 					user=session_user,
	# 					allow="Invoice Receival",
	# 					for_value=self.name,
	# 					apply_to_all_doctypes=1,
	# 					is_default=1,
	# 				)
	# 			).insert(ignore_permissions=False)
	# 		else:
	# 			frappe.get_doc(dict(
	# 					doctype="User Permission",
	# 					user=session_user,
	# 					allow="Invoice Receival",
	# 					for_value=self.name,
	# 					apply_to_all_doctypes=1,
	# 					is_default=1,
	# 				)
	# 			).insert(ignore_permissions=False)
	
	# def delete_user_permission(self):
	# 	for t in frappe.get_all("User Permission",{"allow":self.doctype,"for_value":self.name}):
	# 		frappe.delete_doc("User Permission",t.name)