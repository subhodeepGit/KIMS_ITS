# Copyright (c) 2022, SOUL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class POConsumable(Document):
	def validate(self):
		print("\n\n\n\n\n\n")
		session_user = frappe.session.user
		print(session_user)
		data = frappe.get_all("Employee",{"email":session_user},{"name"})
		print(data)
		for i in data:
			self.append("authorized_signature",{                                     
				"emp_id":i['name'],                                       
				"emp_name":"Ram",                                        
				"designation":"Dr.",                                        
				"date_of_approval":"2022-11-02",                                        
				"date_of_receivable":"2022-11-02",                                        
				"department":"D",                                        
				"approval_status":"Save",                                        
				"previous_status":"Draft",                                        
				"transfer_to":0,                                    
			})
			a.s
