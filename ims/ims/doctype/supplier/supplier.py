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
	res = "https://ifsc.razorpay.com/" + ifsc_code
	response = requests.get(res)
	bank_data=response.json()
	return bank_data

def mand(self):
	if self.ifsc_code!="":
		if self.bank_address==None:
			frappe.throw("IFSC Code is not Correct")
	if self.bank_ac_no!="":
		if self.ifsc_code=="":
			frappe.throw("IFSC Code is Required")
