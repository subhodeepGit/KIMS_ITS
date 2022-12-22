# Copyright (c) 2022, SOUL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests

class Supplier(Document):
	def validate(self):
			mand(self)

@frappe.whitelist()
def ifsc_code(ifsc_code):
	if ifsc_code!=None and ifsc_code!="":
		bank_data=[]
		res = "https://ifsc.razorpay.com/" + ifsc_code
		response = requests.get(res)
		if response.status_code!=404:
			bank_data=response.json()
			return bank_data
		else:
			# frappe.msgprint("IFSC Code not Found")	
			return bank_data

def mand(self):
	if self.ifsc_code!="" and self.ifsc_code!=None:
		if self.bank_address==None:
			frappe.throw("IFSC Code is not Correct")
	if self.bank_ac_no!="" and self.bank_ac_no!=None:
		if self.ifsc_code=="":
			frappe.throw("IFSC Code is Required")
