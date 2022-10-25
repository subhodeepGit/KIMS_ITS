# Copyright (c) 2022, SOUL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Employee(Document):
	# pass
	def after_insert(self):
		self.create_emp_user()

	def create_emp_user(self):
		print("\n\n\n\n\n\n\n")
		print("emp_user")
		if not frappe.db.exists("User", self.email):
			emp_user = frappe.get_doc({
				'doctype':'User',
				'first_name': self.first_name,
				'last_name': self.last_name,
				'email': self.email,
				'gender': self.gender,
				'send_welcome_email': 1,
				'user_type': 'Website User'
				})
			print("\n\n\n\n\n\n\n")
			print(emp_user)
			emp_user.flags.ignore_permissions = True
			emp_user.add_roles("Accounts Manager")
			emp_user.save()
