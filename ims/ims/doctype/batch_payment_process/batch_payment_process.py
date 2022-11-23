# Copyright (c) 2022, SOUL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import utils
from six import iteritems, string_types
import json

class BatchPaymentProcess(Document):
	def validate(self):
		calculate_total(self)
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
					previous_status=frappe.get_all("Batch Payment Process",{"name":self.name},["workflow_state"])
					if not previous_status:
						previous_status=""
					else:
						previous_status=previous_status[0]['workflow_state']	
					
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

						frappe.db.sql(""" update `tabBatch Payment Process` set workflow_state="%s" where name="%s" """%(check,self.name))
						frappe.db.commit()
						frappe.throw("Your Rejection and Transfer is Completed, So Please Referesh your page")	
					else:
						frappe.throw("Employee Not Found")			
				else:
					frappe.throw("Transfer To Employee Not Selected")

@frappe.whitelist()
def get_outstanding_amount(args):
	if isinstance(args, string_types):
		args = json.loads(args)
	filter=[]

	filter.append(['posting_date', 'between',[args.get('from_posting_date'),args.get('to_posting_date')]])
	filter.append(["net_final_amount_to_be_paid_in_rs",">",0])	
	filter.append(["workflow_state","=","Passed for Payment"])
	filter.append(['company',"=",args.get('company')])

	if args.get('outstanding_amt_greater_than') > 0:
		filter.append(["net_final_amount_to_be_paid_in_rs",">",args.get('outstanding_amt_greater_than')])
	if args.get('outstanding_amt_less_than') >0:
		filter.append(["net_final_amount_to_be_paid_in_rs","<",args.get('outstanding_amt_less_than')])

	c_doctype=[{"doctype":"PO Consumable","child_doc":"Details of Invoices and PO"},{"doctype":"PO Consignment","child_doc":"Credit Note and PO"},
						{"doctype":"PO Material Management","child_doc":"Invoices and PO"},{"doctype":"Pharmacy","child_doc":"Enclosed Bills"},
						{"doctype":"Non PO Contract","child_doc":"Details of Enclosed Bills"},{"doctype":"Non PO Non Contract","child_doc":"Details Enclosed Bills"}]
	data=[]
	for doctype in c_doctype:
		invoice_data=frappe.db.get_all(doctype['doctype'],filters=filter,
		fields=['name','posting_date','company','supplier_code','document_number',
				'document_date','supplier_code','name_of_supplier',
				'net_final_amount_to_be_paid_in_rs'],order_by="posting_date asc")
		
		for t in invoice_data:
			sup_info=frappe.db.get_all("Supplier",{"name":t['supplier_code']},["ifsc_code","bank_ac_no","account_holder_name","bank_name","bank_address"])
			t["ifsc_code"]=sup_info[0]['ifsc_code']
			t["bank_ac_no"]=sup_info[0]['bank_ac_no']
			t['account_holder_name']=sup_info[0]['account_holder_name']
			t["bank_name"]=sup_info[0]['bank_name']
			t['bank_address']=sup_info[0]['bank_address']

		for t in invoice_data:
			data.append(t)
	if not data:
		frappe.msgprint("No Data")

	return data

	########################################################
	# po_con=frappe.db.sql(""" Select supplier_code,name_of_supplier from `tabPO Consumable`
	# where company="%s" """%(company),as_dict = True)

	# if len(po_con)!=0:
	# 	return po_con
	# else:
	# 	frappe.throw("No Payment is due")
	########################################################

def calculate_total(self):
		"""Calculates total amount."""
		self.total_amount = 0
		for d in self.table_26:
			self.total_amount += d.amount1