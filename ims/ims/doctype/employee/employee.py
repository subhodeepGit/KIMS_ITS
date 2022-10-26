# Copyright (c) 2022, SOUL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Employee(Document):
	# pass
	def after_insert(self):
		self.create_emp_user()
	
	def validate(self):
		self.enabled_emp()
		self.disable_emp()

	def on_trash(self):
		for usr in frappe.db.get_all("User", {'email':self.email},{'name'}):
			frappe.delete_doc("User",usr.name)

	def create_emp_user(self):
		if not frappe.db.exists("User", self.email):
			emp_user = frappe.get_doc({
				'doctype':'User',
				'first_name': self.first_name,
				'last_name': self.last_name,
				'email': self.email,
				'gender': self.gender,
				'enabled': self.enabled,
				'send_welcome_email': 1,
				'user_type': 'Website User'
				})
			emp_user.flags.ignore_permissions = True
			emp_user.add_roles("Accounts Manager")
			emp_user.save()

	def enabled_emp(self):
		if self.enabled==0:
			emp=frappe.db.get_all("User", {'email':self.email},['name','enabled'])
			status=emp[0]['enabled']
			emp_name = emp[0]['name']
			if status == 1:
				update_doc = frappe.get_doc("User",emp_name)
				update_doc.enabled=0
				update_doc.save()

	def disable_emp(self):
		if self.enabled==1:
			emp=frappe.db.get_all("User", {'email':self.email},['name','enabled'])
			status=emp[0]['enabled']
			emp_name = emp[0]['name']
			if status == 0:
				update_doc = frappe.get_doc("User",emp_name)
				update_doc.enabled=1
				update_doc.save()
