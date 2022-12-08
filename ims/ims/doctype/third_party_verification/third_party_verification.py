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

		# if name_doc
		# third_party_child_data=frappe.get_all("")
		# a.s
		# if name_doc == "PO Consumable":
		# 	third_party_child_data=frappe.get_all("Reference of  Note sheet Verification",{"parent":""})
		# elif name_doc== "PO Consignment":
		# 	attachments = [frappe.attach_print(self.doctype, self.name, file_name=self.name, print_format='PO Consignment PF')]
		# elif name_doc == "PO Material Management":
		# 	attachments = [frappe.attach_print(self.doctype, self.name, file_name=self.name, print_format='PO Material Management PF')]
		# elif name_doc == "Pharmacy":
		# 	attachments = [frappe.attach_print(self.doctype, self.name, file_name=self.name, print_format='Pharmacy PF')]
		# elif name_doc== "Non PO Contract":
		# 	attachments = [frappe.attach_print(self.doctype, self.name, file_name=self.name, print_format='Non Po Contract PF')]
		# elif name_doc == "Non PO Non Contract":
		# 	attachments = [frappe.attach_print(self.doctype, self.name, file_name=self.name, print_format='Non PO Non Contract PF')]
		# elif name_doc == "Patient Refund":
		# 	attachments = [frappe.attach_print(self.doctype, self.name, file_name=self.name, print_format='Patient Refund PF')]