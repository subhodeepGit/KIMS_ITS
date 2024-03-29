# Copyright (c) 2022, SOUL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import utils
from six import iteritems, string_types
import json
from ims.ims.notification.custom_notification import supplier_finalpayment

class BatchPaymentProcess(Document):
	def before_validate(self):
		for z in frappe.get_all("Batch Payment Child",{"parent":self.name},["invoice_tracking_number"]):
			invoice = frappe.get_all("Invoice Receival",{"note_no":z.invoice_tracking_number},["name"])
			if invoice:
				frappe.db.set_value("Invoice Receival",invoice,"batch_payment_no","")
				frappe.db.set_value("Invoice Receival",invoice,"payment_status","")
		for t in frappe.get_all("Batch Payment Child",{"parent":self.name},["invoice_tracking_number","name_of_notesheet"]):
			doctype_data = frappe.get_all(t["name_of_notesheet"],{"name":t.invoice_tracking_number},["name"])
			if doctype_data :
				frappe.db.set_value(t["name_of_notesheet"],doctype_data,"payment_status","Passed for Payment")
				frappe.db.set_value(t["name_of_notesheet"],doctype_data,"batch_payment_no","")

	def validate(self):
		mand(self)
		status_update(self)
		child_mand(self)
		
		if self.workflow_state == "Payment Done":
			supplier_finalpayment(self)

		field_update_notesheer(self)
		if self.workflow_state=="Verified & Submitted by Note Creator":
			doc_before_save = self.get_doc_before_save()
			if doc_before_save.get("vendor_wise_payment_details") == self.get("vendor_wise_payment_details"):
				merge_same_vendor(self)
		calculate_total(self)
		session_user = frappe.session.user
		if self.workflow_state!="Rejected and Transfer":
			if session_user:
				emp_data = frappe.get_all("Employee",{"email":session_user,"enabled":1},["name","full_name","salutation","designation","department"])
				if emp_data:
					##################### Rejected and Transfer Check
					for t in self.get("approval_hierarchy"):
						if self.workflow_state=="Draft":
							pass
						else:
							doc_before_save = self.get_doc_before_save()
							if doc_before_save.document_status!=self.document_status:
								if t.transfer_to==1 and t.disapproval_check==1:
									pass
								if t.transfer_to==1 and t.disapproval_check==0:
									frappe.throw("Rejected and Transfer to state <b>%s</b> is checked in line no :-<b> %s </b> for the table Authorized Signature."%(t.approval_status,t.idx))
					##############################
					flag="Yes"
					object_var=""
					for t in self.get("approval_hierarchy"):
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
					previous_status=frappe.get_all("Batch Payment Process",{"name":self.name},["workflow_state"])
					if not previous_status:
						previous_status=""
					else:
						previous_status=previous_status[0]['workflow_state']	
					
					date_of_receivable=""
					for t in self.get("approval_hierarchy"):
						date_of_receivable=t.date_of_approval
					

					document_type="Batch Payment Process"
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



					if date_of_receivable=="":
						date_of_receivable=utils.now()
					emp_name=emp_data[0]['salutation']+" "+emp_data[0]['full_name']


					if flag=="Yes":
						approval_email_status="Mail Not Send"
						notesheet_cancellation_email_status=""
						if self.workflow_state=="Draft" or self.workflow_state=="Verify and Save":
							approval_email_status=""
							notesheet_cancellation_email_status=""
						if self.workflow_state=="Cancelled":
							approval_email_status=""
							notesheet_cancellation_email_status="Mail Not Send"	
						self.append("approval_hierarchy",{                                     
							"emp_id":emp_data[0]['name'],                                       
							"emp_name":emp_name,                                        
							"designation":emp_data[0]['designation'],                                        
							"date_of_approval":utils.now(),                                        
							"date_of_receivable":date_of_receivable,                                        
							"department":emp_data[0]['department'],                                        
							"approval_status":approval_status,                              
							"previous_status":previous_status,                                 
							"transfer_to":0, 
							"workflow_data":workflow_name,
							"grouping_of_designation":grouping_of_designation,
							"single_user":single_user,
							"approval_email_status":approval_email_status,
							"notesheet_cancellation_email_status":notesheet_cancellation_email_status                                       
						})
						frappe.msgprint("Your Document has been %s"%(self.workflow_state))
					if flag=="No":
						for t in self.get("approval_hierarchy"):
							if t.name==object_var.name:
								previous_status=t.previous_status
								t.emp_id=emp_data[0]['name']
								t.emp_name=emp_name
								t.designation=emp_data[0]['designation']
								t.date_of_approval=utils.now()
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
				for t in self.get("approval_hierarchy"):
					if t.transfer_to==1 and t.disapproval_check==0:
						check=t.previous_status
						name=t.name
				if name!="":
					emp_data = frappe.get_all("Employee",{"email":session_user,"enabled":1},["name","full_name","salutation","designation","department"])
					if emp_data:
						emp_name=emp_data[0]['salutation']+" "+emp_data[0]['full_name']
						for t in self.get("approval_hierarchy"):
							if t.name>=name:
								frappe.db.sql(""" update `tabAuthorized Signature` set disapproval_check=1,disapproval_emp_name="%s",disapproval_emp="%s" ,
												rejection_email_status="Mail Not Send" where name="%s" """%(emp_name,emp_data[0]['name'],t.name))
								frappe.db.commit()

						frappe.db.sql(""" update `tabBatch Payment Process` set workflow_state="%s" where name="%s" """%(check,self.name))
						frappe.db.commit()
						frappe.db.sql(""" update `tabBatch Payment Process` set document_status="%s" where name="%s" """%("Rejected and Transfer",self.name))
						frappe.db.commit()
						frappe.throw("Your Rejection and Transfer is Completed, So Please Referesh your page")	
					else:
						frappe.throw("Employee Not Found")			
				else:
					frappe.throw("Transfer To Employee Not Selected")

@frappe.whitelist()
def get_outstanding_amount(args,name):
	if isinstance(args, string_types):
		args = json.loads(args)
	filter=[]

	filter.append(['posting_date', 'between',[args.get('from_posting_date'),args.get('to_posting_date')]])	
	filter.append(["workflow_state","=","Passed for Payment"])
	filter.append(["payment_status","in",("Passed for Payment","Cancelled")])
	filter.append(['company',"=",args.get('company')])
	# if args.get('priority'):
	# 	filter.append(['priority',"=",args.get('priority')])
	


	if args.get("invoice")==None:
		c_doctype=[{"doctype":"PO Consumable","child_doc":"Details of Invoices and PO"},{"doctype":"PO Consignment","child_doc":"Credit Note and PO"},
					{"doctype":"PO Material Management","child_doc":"Invoices and PO"},{"doctype":"Pharmacy","child_doc":"Enclosed Bills"},
					{"doctype":"Non PO Contract","child_doc":"Details of Enclosed Bills"},{"doctype":"Non PO Non Contract","child_doc":"Details Enclosed Bills"},
					{"doctype":"Patient Refund","child_doc":""}]
	elif args.get("invoice")!=None:
		c_doctype=[{"doctype":args.get("invoice")}]

	if (args.get('vendor') and args.get('patient_refund')) or (args.get('employee') and args.get('patient_refund')) or (args.get('vendor') and args.get('employee')):
		frappe.msgprint("Please Select one filed in Type Of Supplier on Pop-Up Screen")

	# if args.get('vendor'):
	# 	filter.append(['supplier_code',"=",args.get('vendor')])
	# if args.get('employee'):
	# 	filter.append(['employee',"=",args.get('employee')])	
	# if args.get('patient_refund'):
	# 	filter.append(['name',"=",args.get('patient_refund')])	

	data=[]

	for doctype in c_doctype:
		filter_for=[]
		filter_for=filter.copy()

		if doctype['doctype']!="Patient Refund":
			if args.get('priority'):
				filter_for.append(['priority',"=",args.get('priority')])
			if args.get('vendor'):
				filter_for.append(['supplier_code',"=",args.get('vendor')])	
			filter_for.append(["net_final_amount_to_be_paid_in_rs",">",0])
			if args.get('outstanding_amt_greater_than') > 0:
				filter_for.append(["net_final_amount_to_be_paid_in_rs",">=",args.get('outstanding_amt_greater_than')])
			if args.get('outstanding_amt_less_than') >0:
				filter_for.append(["net_final_amount_to_be_paid_in_rs","<=",args.get('outstanding_amt_less_than')])
			if doctype['doctype']=="Non PO Non Contract":
				if args.get('employee'):
					filter_for.append(['employee',"=",args.get('employee')])	
				invoice_data=frappe.db.get_all(doctype['doctype'],filters=filter_for,
				fields=['name','posting_date','company','supplier_code','document_number',
						'document_date','supplier_code','name_of_supplier',
						'net_final_amount_to_be_paid_in_rs','workflow_state','type_of_supplier','employee','employee_name'],order_by="posting_date asc")

				for t in invoice_data:
					if t['type_of_supplier']=="Supplier":
						sup_info=frappe.db.get_all("Supplier",{"name":t['supplier_code']},["ifsc_code","bank_ac_no","account_holder_name","bank_name","bank_address"])
						t["ifsc_code"]=sup_info[0]['ifsc_code']
						t["bank_ac_no"]=sup_info[0]['bank_ac_no']
						t['account_holder_name']=sup_info[0]['account_holder_name']
						t["bank_name"]=sup_info[0]['bank_name']
						t['bank_address']=sup_info[0]['bank_address']
						t['name_of_notesheet']=doctype['doctype']
						t['type_of_clients']="Supplier"
					if t['type_of_supplier']=="Employee":
						emp_info=frappe.db.get_all("Employee",{"name":t['employee']},["ifsc_code","bank_ac_no","account_holder_name","bank_address","branch_name","bank_name"])
						t["ifsc_code"]=emp_info[0]['ifsc_code']
						t["bank_ac_no"]=emp_info[0]['bank_ac_no']
						t['account_holder_name']=emp_info[0]['account_holder_name']
						t["bank_name"]=emp_info[0]['bank_name']
						t['bank_address']=emp_info[0]['branch_name']
						t['name_of_notesheet']=doctype['doctype']
						t['type_of_clients']="Employee"

				for t in invoice_data:
					emp={}
					if t['type_of_supplier']=="Supplier":
						emp['workflow_state']=t['workflow_state']	
						emp['name_of_notesheet']=doctype['doctype']
						emp['name']=t['name']
						emp['document_number']=t['document_number']
						emp['document_date']=t['document_date']
						emp['supplier_code']=t['supplier_code']
						emp['name_of_supplier']=t['name_of_supplier']
						emp['account_holder_name']=t['account_holder_name']
						emp['bank_name']=t['bank_name']
						emp['bank_address']=t['bank_address']
						emp['bank_ac_no']=t['bank_ac_no']
						emp['ifsc_code']=t['ifsc_code']
						emp['net_final_amount_to_be_paid_in_rs']=t['net_final_amount_to_be_paid_in_rs']
						emp['net_final_amount_to_be_paid_in_rs']=t['net_final_amount_to_be_paid_in_rs']
						emp['type_of_clients']=t['type_of_clients']
						if not args.get('patient_refund'):
							if not args.get('employee'):
								data.append(emp)
					if t['type_of_supplier']=="Employee":
						emp['workflow_state']=t['workflow_state']	
						emp['name_of_notesheet']=doctype['doctype']
						emp['name']=t['name']
						emp['document_number']=t['document_number']
						emp['document_date']=t['document_date']
						emp['supplier_code']=t['employee']
						emp['name_of_supplier']=t['employee_name']
						emp['account_holder_name']=t['account_holder_name']
						emp['bank_name']=t['bank_name']
						emp['bank_address']=t['bank_address']
						emp['bank_ac_no']=t['bank_ac_no']
						emp['ifsc_code']=t['ifsc_code']
						emp['net_final_amount_to_be_paid_in_rs']=t['net_final_amount_to_be_paid_in_rs']
						emp['net_final_amount_to_be_paid_in_rs']=t['net_final_amount_to_be_paid_in_rs']
						emp['type_of_clients']=t['type_of_clients']
						if not args.get('patient_refund'):
							if not args.get('vendor'):
								data.append(emp)
			else:	
				invoice_data=frappe.db.get_all(doctype['doctype'],filters=filter_for,
				fields=['name','posting_date','company','supplier_code','document_number',
						'document_date','supplier_code','name_of_supplier',
						'net_final_amount_to_be_paid_in_rs','workflow_state'],order_by="posting_date asc")
		
				for t in invoice_data:
					sup_info=frappe.db.get_all("Supplier",{"name":t['supplier_code']},["ifsc_code","bank_ac_no","account_holder_name","bank_name","bank_address"])
					t["ifsc_code"]=sup_info[0]['ifsc_code']
					t["bank_ac_no"]=sup_info[0]['bank_ac_no']
					t['account_holder_name']=sup_info[0]['account_holder_name']
					t["bank_name"]=sup_info[0]['bank_name']
					t['bank_address']=sup_info[0]['bank_address']
					t['name_of_notesheet']=doctype['doctype']
					t['type_of_clients']="Supplier"

				for t in invoice_data:
					if not args.get('employee'):
						if not args.get('patient_refund'):
							data.append(t)
		else:
			if args.get('patient_refund'):
				filter_for.append(['name',"=",args.get('patient_refund')])
			filter_for.append(["net_refundable_in_figures",">",0])	
			if args.get('outstanding_amt_less_than') > 0:
				filter_for.append(["net_refundable_in_figures",">=",args.get('outstanding_amt_greater_than')])
			if args.get('outstanding_amt_less_than') >0:
				filter_for.append(["net_refundable_in_figures","<=",args.get('outstanding_amt_less_than')])
			invoice_data=frappe.db.get_all(doctype['doctype'],filters=filter_for,
							fields=["name","name_of_the_patient","ip__uhid_no","posting_date","ifsc_code",
							"account_no","net_refundable_in_figures","account_holder_name","name_of_the_bank",
							"bank_address","workflow_state","branch"])
			
			for t in invoice_data:
				patient_refund={}
				patient_refund['name_of_supplier']=t['name_of_the_patient']
				patient_refund['supplier_code']=t['ip__uhid_no']
				patient_refund['document_number']=""
				patient_refund['document_date']=t['posting_date']
				patient_refund['ifsc_code']=t['ifsc_code']
				patient_refund['bank_ac_no']=t['account_no']
				patient_refund['net_final_amount_to_be_paid_in_rs']=t['net_refundable_in_figures']
				patient_refund['net_final_amount_to_be_paid_in_rs']=t['net_refundable_in_figures']
				patient_refund['account_holder_name']=t['account_holder_name']
				patient_refund['bank_name']=t['name_of_the_bank']
				patient_refund['bank_address']=t['branch']
				# patient_refund['bank_address']=t['bank_address']
				patient_refund['name']=t['name']
				patient_refund['workflow_state']=t['workflow_state']
				patient_refund['name_of_notesheet']=doctype['doctype']
				patient_refund['type_of_clients']="Patient"
				
				if not args.get('vendor'):
					if not args.get('employee'):
						if not args.get('priority'):
							data.append(patient_refund)

			for x in frappe.get_all("Batch Payment Child",{"parent":name},["approve","invoice_tracking_number","name_of_notesheet",
			               			"document_no","document_date","vendor_code","vendor_name","ac_holder_name","bank_name",
									"branch","ac_no","ifsc_code","amount","amount1"]):
				all_ready={}
				all_ready['workflow_state']=x['approve']	
				all_ready['name_of_notesheet']=x['name_of_notesheet']
				all_ready['name']=x['invoice_tracking_number']
				all_ready['document_number']=x['document_no']
				all_ready['document_date']=x['document_date']
				all_ready['supplier_code']=x['vendor_code']
				all_ready['name_of_supplier']=x['vendor_name']
				all_ready['account_holder_name']=x['ac_holder_name']
				all_ready['bank_name']=x['bank_name']
				all_ready['bank_address']=x['branch']
				all_ready['bank_ac_no']=x['ac_no']
				all_ready['ifsc_code']=x['ifsc_code']
				all_ready['net_final_amount_to_be_paid_in_rs']=x['amount']
				all_ready['net_final_amount_to_be_paid_in_rs']=x['amount1']		
				all_ready['type_of_clients']="Patient"	
				data.append(all_ready)

	if not data:
		frappe.msgprint("You have No Data in NoteSheet")
	print("\n\n")
	print(data)
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
			self.total_amount += d.amount

@frappe.whitelist()
def merge_same_vendor(self):
	data=[]
	for t in self.get("table_26"):
		a={}
		a['name']=t.name
		a['supplier_code']=t.vendor_code
		a['name_of_supplier']=t.vendor_name
		a['net_final_amount_to_be_paid_in_rs']=t.amount
		a['ifsc_code']=t.ifsc_code
		a['bank_ac_no']=t.ac_no
		a['account_holder_name']=t.ac_holder_name
		a['bank_name']=t.bank_name
		a['bank_address']=t.branch
		a['type_of_clients']=t.type_of_clients
		data.append(a)
	
	if not data:
		frappe.msgprint("No Data")
	else:
		supplier_code=[]
		for t in data:
			supplier_code.append(t['supplier_code'])
		supplier_code=list(set(supplier_code))
		final_data=[]
		for t in supplier_code:
			a={}
			for j in data:
				if t==j['supplier_code']:
					a['supplier_code']=j['supplier_code']
					a['name_of_supplier']=j['name_of_supplier']
					a["ac_holder_name"]=j['account_holder_name']
					a["bank_name"]=j['bank_name']
					a["ac_no"]=j['bank_ac_no']
					a["ifsc_code"]=j['ifsc_code']
					a["branch"]=j['bank_address']
					a['type_of_clients']=j['type_of_clients']
					a["amount"]=[]
					break
			final_data.append(a)

		for t in final_data:
			for j in data:
				if t['supplier_code']==j['supplier_code']:
					t["amount"].append(j['net_final_amount_to_be_paid_in_rs'])

		for t in final_data:
			t["amount"]=sum(t["amount"])
		data=final_data
		for t in data:
			self.append("vendor_wise_payment_details",{                                     
					"vendor_code":t['supplier_code'],                                       
					"vendor_name":t['name_of_supplier'],
					"ac_holder_name":t['ac_holder_name'],
					"bank_name":t['bank_name'],
					"ac_no":t['ac_no'],
					"ifsc_code":t['ifsc_code'],
					"branch":t['branch'],
					"amount":t['amount'],
					"type_of_client":t['type_of_clients']                                                                   
				})
def mand(self):
	if self.document_status=="Payment Sheet Submitted to Bank":
		if self.cheque_no==None or self.cheque_no=="":
			frappe.throw("Cheque No	is mandatory")
		if self.cheque_date==None or self.cheque_date=="":
			frappe.throw("Cheque Date is mandatory")
		if self.cheque_attachment==None or self.cheque_attachment=="":
			frappe.throw("Cheque Attachment is mandatory")
		if self.note_sheet_attachment==None or self.note_sheet_attachment=="":
			frappe.throw("Note Sheet Attachment	is mandatory")
		if self.contact_person==None or self.contact_person=="":
			frappe.throw("Contact Person is mandatory")
	if self.document_status=="Payment Sheet Received By Audit":
		if self.audit_reference_no==None or self.audit_reference_no=="":
			frappe.throw("Audit Reference No is mandatory")
		if self.audit_posting_date==None or self.audit_posting_date=="":
			frappe.throw("Audit Posting Date is mandatory")
	if self.document_status=="Payment Done":
		for t in self.get("vendor_wise_payment_details"):
			if t.payment_status!="" or t.payment_status!=None:
				if t.payment_status=="Payment successful":
					if t.sap_document_number=="" or t.sap_document_number==None:
						frappe.throw("SAP Document number is mandatory in Payment Details table")
					if t.mode_of_payment=="" or t.mode_of_payment==None:
						frappe.throw("Mode of Payment is mandatory in Payment Details table")
			else:
				frappe.throw("Payment Status is mandatory in Payment Details table")	

def child_mand(self):
	if self.document_status=="Payment Done":
		for t in self.get("vendor_wise_payment_details"):
			if t.payment_status=="" or t.payment_status==None:
				frappe.throw("Payment Status is Required in Vendor Wise Payment Details table")

def field_update_notesheer(self):
	doc_before_save = self.get_doc_before_save()
	if self.workflow_state=="Draft" or self.workflow_state=="Verify and Save" or self.workflow_state=="Cancelled":
		for t in self.get("table_26"):
			workflow_status=self.workflow_state
			frappe.db.set_value(t.name_of_notesheet,t.invoice_tracking_number,"payment_status",workflow_status)
			frappe.db.set_value(t.name_of_notesheet,t.invoice_tracking_number,"batch_payment_no",self.name)

	elif doc_before_save.document_status!=self.document_status:
		for t in self.get("table_26"):
			if self.document_status=="Payment Done":
				pass
			else:
				workflow_status=self.workflow_state
				frappe.db.set_value(t.name_of_notesheet,t.invoice_tracking_number,"payment_status",workflow_status)
				frappe.db.set_value(t.name_of_notesheet,t.invoice_tracking_number,"batch_payment_no",self.name)

		if self.document_status=="Payment Done":
			for j in self.get("vendor_wise_payment_details"):
				for t in self.get("table_26"):
					if t.vendor_code==j.vendor_code:
						if j.payment_status=="Payment Failed":
							workflow_status=j.payment_status
							frappe.db.set_value(t.name_of_notesheet,t.invoice_tracking_number,"payment_status",workflow_status)
							frappe.db.set_value(t.name_of_notesheet,t.invoice_tracking_number,"workflow_state","Verify and Save")
							frappe.db.set_value(t.name_of_notesheet,t.invoice_tracking_number,"document_status","Document save")
							frappe.db.set_value(t.name_of_notesheet,t.invoice_tracking_number,"batch_payment_no",self.name)
						else:
							workflow_status=j.payment_status
							frappe.db.set_value(t.name_of_notesheet,t.invoice_tracking_number,"payment_status",workflow_status)	
							frappe.db.set_value(t.name_of_notesheet,t.invoice_tracking_number,"batch_payment_no",self.name)		

def status_update(self):
	workflow_status=self.workflow_state
	name=self.name
	for t in self.get("table_26"):
		invoice = frappe.get_all("Invoice Receival",{"note_no":t.invoice_tracking_number},["name"])
		if invoice:
			for x in invoice:
				if workflow_status!="Cancelled":
					frappe.db.set_value("Invoice Receival",x["name"],"batch_payment_no",name)
					frappe.db.set_value("Invoice Receival",x["name"],"payment_status",workflow_status)
				else:
					frappe.db.set_value("Invoice Receival",x["name"],"batch_payment_no","")
					frappe.db.set_value("Invoice Receival",x["name"],"payment_status","")