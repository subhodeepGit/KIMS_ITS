# Copyright (c) 2022, SOUL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import money_in_words
from frappe import utils

class PatientRefund(Document):
	def validate(self):
		# mand(self)
		mandatory_check(self)
		# self.net_refundable_in_figures=(self.amount_deposited_by_patient - self.approval_of_tpa__insurance__corporate__ostf - self.cash_refund - self.total_bill - self.approval_of_tpa__insurance__corporate__ostf - self.less__non_admissible_item__discount_amount)
		self.net_refundable_in_words = money_in_words(self.net_refundable_in_figures)
		session_user = frappe.session.user
		if self.workflow_state!="Rejected and Transfer":
			if 	approval_status=="Approved by Accounts Clerk":
				self.payment_status="Passed for Payment"	
			if session_user:
				emp_data = frappe.get_all("Employee",{"email":session_user,"enabled":1},["name","full_name","salutation","designation","department"])
				if emp_data:
					flag="Yes"
					object_var=""
					for t in self.get("authorized_signature"):
						object_var=t

					if object_var!="":
						if self.workflow_state=="Draft" or self.workflow_state=="Verify and Save" or self.workflow_state=="Cancelled":
							if (object_var.approval_status==self.workflow_state) and object_var.emp_id==emp_data[0]["name"]:
								flag="No"
						else:
							doc_before_save = self.get_doc_before_save()
							if doc_before_save.document_status==self.document_status:
								flag=""

					approval_status=self.workflow_state
					previous_status=frappe.get_all("Patient Refund",{"name":self.name},["workflow_state"])
					if not previous_status:
						previous_status=""
					else:
						previous_status=previous_status[0]['workflow_state']
					

					document_type="Patient Refund"
					approval_status_print=""
					workflow_name=frappe.get_all("Workflow",{"document_type":document_type,"is_active":1},['name'])[0]['name']
					if previous_status=="":
						approval_status_print=approval_status
					else:
						state_info=frappe.get_all("Workflow Document State",{"parent":workflow_name},["state"],order_by="idx asc")
						count=0
						for s in state_info:
							count=count+1
							if s["state"]==approval_status:
								break

						pre_flow_list=state_info[count-1]["state"]
						approval_status_print=pre_flow_list	
					
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
								t.grouping_of_designation=grouping_of_designation
								t.single_user=single_user			

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

						frappe.db.sql(""" update `tabPatient Refund` set workflow_state="%s" where name="%s" """%(check,self.name))
						frappe.db.commit()
						frappe.throw("Your Rejection and Transfer is Completed, So Please Referesh your page")
					else:
						frappe.throw("Employee Not Found")
				else:
					frappe.throw("Transfer To Employee Not Selected")


def mandatory_check(self):
	if self.ifsc_code!="":
		if self.branch==None:
			frappe.throw("IFSC Code is not Correct")
	if self.net_refundable_in_figures<=0:
		frappe.throw("Net Refundable should more the Zerro.")	

# def mand(self):
# 	if self.ifsc_code!="":
# 		if self.branch==None:
# 			frappe.throw("IFSC Code is not Correct")