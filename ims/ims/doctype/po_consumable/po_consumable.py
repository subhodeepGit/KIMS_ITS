# Copyright (c) 2022, SOUL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import utils
from frappe.utils import cint, date_diff, datetime, get_datetime, today

class POConsumable(Document):
	def validate(self):
		if self.workflow_state=="Bill Received by Audit":
			date=datetime.date.today()
			self.db_set("today_date",date)
		session_user = frappe.session.user
		if self.workflow_state!="Cancelled" and self.workflow_state!="Rejected and Transfer":
			if session_user:
				emp_data = frappe.get_all("Employee",{"email":session_user,"enabled":1},["name","full_name","salutation","designation","department"])
				if emp_data:
					flag="Yes"
					object_var=""
					for t in self.get("authorized_signature"):
						object_var=t

					if object_var!="":
						if object_var.approval_status==self.workflow_state :
							flag="No"

					approval_status=self.workflow_state
					previous_status=frappe.get_all("PO Consumable",{"name":self.name},["workflow_state"])
					if not previous_status:
						previous_status=""
					else:
						previous_status=previous_status[0]['workflow_state']	
					

					document_type="PO Consumable"
					approval_status_print=""
					
					if previous_status=="":
						approval_status_print=approval_status
					else:
						approval_status_print=previous_status

					workflow_name=frappe.get_all("Workflow",{"document_type":document_type,"is_active":1},['name'])[0]['name']
					grp_info=frappe.get_all("Workflow Document State",{"parent":workflow_name,"state":approval_status_print},
												['name',"grouping_of_designation","single_user"])
						

					grouping_of_designation=grp_info[0]['grouping_of_designation']
					single_user=grp_info[0]['single_user']


					date_of_receivable=""
					for t in self.get("authorized_signature"):
						date_of_receivable=t.date_of_approval
					
					if date_of_receivable=="":
						date_of_receivable=utils.today()
					emp_name=emp_data[0]['salutation']+" "+emp_data[0]['full_name']


					if flag=="Yes":
						self.append("authorized_signature",{                                     
							"emp_id":emp_data[0]['name'],                                       
							"emp_name":emp_name,                                        
							"designation":emp_data[0]['designation'],                                        
							"date_of_approval":utils.today(),                                        
							"date_of_receivable":date_of_receivable,                                        
							"department":emp_data[0]['department'],                                        
							"approval_status":approval_status,                              
							"previous_status":previous_status,                                 
							"transfer_to":0,
							"workflow_data":workflow_name,
							"grouping_of_designation":grouping_of_designation,
							"single_user":single_user                                  
						})
					if flag=="No":
						for t in self.get("authorized_signature"):
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
								t.workflow_data= workflow_name
								t.grouping_of_designation=grouping_of_designation
								t.single_user=single_user 
								# t.transfer_to=0

			else:
				frappe.throw("Employee not found")		
		else:
			if self.workflow_state=="Rejected and Transfer":
				check=""
				count=0
				name=""
				for t in self.get("authorized_signature"):
					if t.transfer_to==1 and t.disapproval_check==0:
						check=t.previous_status
						name=t.name
				if name!="":
					emp_data = frappe.get_all("Employee",{"email":session_user,"enabled":1},["name","full_name","salutation","designation","department"])
					if emp_data:
						emp_name=emp_data[0]['salutation']+" "+emp_data[0]['full_name']
						for t in self.get("authorized_signature"):
							if t.name>=name:
								frappe.db.sql(""" update `tabAuthorized Signature` set disapproval_check=1,disapproval_emp_name="%s",disapproval_emp="%s" 
												where name="%s" """%(emp_name,emp_data[0]['name'],t.name))
								frappe.db.commit()

						frappe.db.sql(""" update `tabPO Consumable` set workflow_state="%s" where name="%s" """%(check,self.name))
						frappe.db.commit()
						frappe.throw("Your Rejection and Transfer is Completed, So Please Referesh your page")	
					else:
						frappe.throw("Employee Not Found")			
				else:
					frappe.throw("Transfer To Employee Not Selected")