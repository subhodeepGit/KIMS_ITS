# Copyright (c) 2022, SOUL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import utils

class BatchPaymentProcess(Document):
	def validate(self):
		session_user = frappe.session.user
		if session_user:
			emp_data = frappe.get_all("Employee",{"email":session_user,"enabled":1},["name","full_name","salutation","designation","department"])
			if emp_data:
				flag="Yes"
				object_var=""
				for t in self.get("approval_hierarchy"):
					object_var=t

				if object_var!="":
					if object_var.approval_status==self.workflow_state :
						flag="No"

				approval_status=self.workflow_state
				previous_status=frappe.get_all("Batch Payment Process",{"name":self.name},["workflow_state"])
				if not previous_status:
					previous_status=""
				else:
					previous_status=previous_status[0]['workflow_state']	
				
				date_of_receivable=""
				for t in self.get("approval_hierarchy"):
					date_of_receivable=t.date_of_approval
				
				if date_of_receivable=="":
					date_of_receivable=utils.today()
				emp_name=emp_data[0]['salutation']+" "+emp_data[0]['full_name']


				if flag=="Yes":
					self.append("approval_hierarchy",{                                     
						"emp_id":emp_data[0]['name'],                                       
						"emp_name":emp_name,                                        
						"designation":emp_data[0]['designation'],                                        
						"date_of_approval":utils.today(),                                        
						"date_of_receivable":date_of_receivable,                                        
						"department":emp_data[0]['department'],                                        
						"approval_status":approval_status,                              
						"previous_status":previous_status,                                 
						"transfer_to":0,                                    
					})
				if flag=="No":
					for t in self.get("approval_hierarchy"):
						if t.name==object_var.name:
							previous_status=t.previous_status
							t.emp_id=emp_data[0]['name']
							t.emp_name=emp_name
							t.designation=emp_data[0]['designation']
							t.date_of_approval=utils.today()
							t.date_of_receivable=date_of_receivable
							t.department=emp_data[0]['department']
							t.approval_status=approval_status
							t.previous_status=previous_status

		else:
			frappe.throw("Employee not found")

@frappe.whitelist()
def get_outstanding_amount(company=None):
	po_con=frappe.db.sql(""" Select supplier_code,name_of_supplier from `tabPO Consumable`
	where company="%s" """%(company),as_dict = True)

	if len(po_con)!=0:
		return po_con
	else:
		frappe.throw("No Payment is due")