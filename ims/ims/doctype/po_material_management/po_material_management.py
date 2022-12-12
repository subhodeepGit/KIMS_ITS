# Copyright (c) 2022, SOUL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import utils
from frappe.utils import cint, date_diff, datetime, get_datetime, today
from ims.ims.notification.custom_notification import supplier_payment_initiazation, designation_wise_email, supplier_passforpayment

class POMaterialManagement(Document):
	def validate(self):

		mandatory_check(self)

		designation_wise_email(self)
		
		if self.workflow_state == "Verified & Submitted by Note Creator":
			count = 0
			for t in self.get("authorized_signature"):
				if t.approval_status == "Verified & Submitted by Note Creator":
					count=count+1
			if count == 0:
				supplier_payment_initiazation(self)
		
		if self.workflow_state == "Passed for Payment":
			supplier_passforpayment(self)

		third_party_verification(self)
		if self.workflow_state=="Bill Received by Audit" and (self.today_date==None or self.today_date==""):
			date=datetime.date.today()
			self.db_set("today_date",date)
		session_user = frappe.session.user
		if self.workflow_state!="Rejected and Transfer":
			if 	self.workflow_state=="Passed for Payment":
				self.payment_status="Passed for Payment"	
			if session_user:
				emp_data = frappe.get_all("Employee",{"email":session_user,"enabled":1},["name","full_name","salutation","designation","department"])
				if emp_data:
					##################### Rejected and Transfer Check
					for t in self.get("authorized_signature"):
						doc_before_save = self.get_doc_before_save()
						if doc_before_save.document_status!=self.document_status:
							if t.transfer_to==1 and t.disapproval_check==1:
								pass
							if t.transfer_to==1 and t.disapproval_check==0:
								frappe.throw("Rejected and Transfer to state <b>%s</b> is checked in line no :-<b> %s </b> for the table Authorized Signature."%(t.approval_status,t.idx))
					##############################
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
					previous_status=frappe.get_all("PO Material Management",{"name":self.name},["workflow_state"])
					if not previous_status:
						previous_status=""
					else:
						previous_status=previous_status[0]['workflow_state']	
					

					document_type="PO Material Management"
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

						frappe.db.sql(""" update `tabPO Material Management` set workflow_state="%s" where name="%s" """%(check,self.name))
						frappe.db.commit()
						frappe.db.sql(""" update `tabPO Material Management` set document_status="%s" where name="%s" """%("Rejected and Transfer",self.name))
						frappe.db.commit()
						frappe.throw("Your Rejection and Transfer is Completed, So Please Referesh your page")	
					else:
						frappe.throw("Employee Not Found")			
				else:
					frappe.throw("Transfer To Employee Not Selected")



def mandatory_check(self):
	if self.workflow_state=="Verify and Save":
		count=0
		for t in self.get("details_of_invoices_and_po"):
			count=count+1
			if t.po_attachment_attachment!=1: 
				frappe.throw("PO Attachment	is mandatory in row on %s"%(count))
	
	if self.workflow_state=="Bill Received by Audit" and (self.audit_ref_no==None or self.audit_ref_no==""): 
		frappe.throw("Audit Ref No.	is mandatory")

	if self.workflow_state=="Passed for Payment":
		if self.profit_center==None or self.profit_center=="":
			frappe.throw("Profit Center	is mandatory")
		if self.document_number==None or self.document_number=="":
			frappe.throw("Document Number is mandatory")
		if self.ref_no==None or self.ref_no=="":
			frappe.throw("Ref No is mandatory")
		if self.document_date==None or self.document_date=="":
			frappe.throw("Document Date	is mandatory")
		if self.attach_journal_voucher==None or self.attach_journal_voucher=="":
			frappe.throw("Journal Voucher Attachment is mandatory")



@frappe.whitelist()
def get_table_attachments():
	attachments = []

	for t in frappe.get_all("DocField",{"parent": "Invoices and PO","fieldtype":"Attach"},["fieldname","mandatory_depends_on"]):
		if t['mandatory_depends_on']!=None or t['mandatory_depends_on']!="":
			a=t['mandatory_depends_on'].split(":")
			a=a[1].split(".")
			a=a[1].split("=")
			flag={}
			flag['att_fieldname']=t['fieldname']
			flag['chk_fieldname']=a[0]
			attachments.append(flag)	
	return attachments


def third_party_verification(self):
	third_party_verification=self.get("third_party_verification")
	if third_party_verification:
		for t in self.get("third_party_verification"):
			if t.final_status=="Open" and t.status_of_verification==None:
				########################### proving role for creation
				session_user = frappe.session.user
				emp_data = frappe.get_all("Employee",{"email":session_user,"enabled":1},["designation","email"])
				if emp_data:
					###################### Data enrty in Third-Party Verification
					ref_party_doc=frappe.get_doc({
						'doctype':'Third-Party Verification',
						"company":self.company,
						"type_of_note_sheet":"PO Material Management",
						"documnet_no":self.name,
						"note_sheet_no":self.note_sheet_no,
						"date_of_note_sheet":self.date_of_note_sheet,
						"name_of_schooldepartment":self.name_of_schooldepartment,
						"for_which_department":self.for_which_department,
						"document_status":self.document_status,
						"priority":self.priority,
						"approver_comment_to_third_party":t.remarks_by_creater
					})
					for j in self.get("details_of_invoices_and_po"):
						ref_party_doc.append("third_party_verification_child",{
							"details_of_invoices_po":j.po_no,
							"invoice_no":j.invoice_no,
							"invoice_date":j.invoice_date,
							"invoices_amountin_rs":j.invoices_amountin_rs,
							"invoice_attachment":j.invoice,
							"credit_memo_attachment":j.credit_memo,
							"document_attachment":j.document,
							"po_attachment_attachment":j.po_attachment,
							"bill_summary_attadelivery_challanchment":j.bill_summary,
							"delivery_challan_attachment":j.delivery_challan,
							"grn_attachment":j.grn,
						})
					ref_party_doc.save()
					doc_name=ref_party_doc.name
					t.status_of_verification="Forward For Verification"
					t.document_name=doc_name
					##################################### 3rd party Auto share with
					user=t.employee_id
					emp_data = frappe.get_all("Employee",{"name":user},["email"])
					user=emp_data[0]["email"]
					frappe.share.add_docshare('Third-Party Verification', 
										doc_name, 
										user, 
										submit=1,
										read=1,
										write=1,    
										flags={"ignore_share_permission": True}) 
				else:
					frappe.throw("Employee Not Found")	

@frappe.whitelist()
def get_action_acess(self):
	import json
	self = json.loads(self)
	count=0
	if self:
		for t in self["third_party_verification"]:
			if t['final_status']=="Open":
				count=count+1
	return count