# Copyright (c) 2022, SOUL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Designation(Document):
	def validate(self):
		role_cration(self)
		
def role_cration(self):
	role_info=frappe.get_all("Role",{"name":self.designation})
	if not role_info:
		role_doc = frappe.new_doc("Role")
		role_doc.role_name = self.designation
		role_doc.search_bar=0
		role_doc.notifications=1
		role_doc.list_sidebar=0
		role_doc.bulk_actions=0
		role_doc.view_switcher=0
		role_doc.form_sidebar=1
		role_doc.timeline=1
		role_doc.dashboard=1  
		role_doc.save()