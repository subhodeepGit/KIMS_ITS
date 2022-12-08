# Copyright (c) 2022, SOUL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ThirdPartyVerification(Document):
	def on_submit(self):
		name_doc=self.type_of_note_sheet
		doc_no=self.documnet_no
		third_party_child_data=frappe.get_all("Reference of  Note sheet Verification",{"parent":doc_no,"parenttype":name_doc},['name','final_status'])
		name=""
		for t in third_party_child_data:
			if t['final_status']=="Open":
				name=t['name']
				break
		frappe.db.set_value("Reference of  Note sheet Verification",name,"final_status","Close")
		frappe.db.set_value("Reference of  Note sheet Verification",name,"status_of_verification","Verification Completed")		