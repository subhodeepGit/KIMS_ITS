# Copyright (c) 2022, SOUL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Employee(Document):
	def validate(self):
		self.enabled_emp()
		self.set_employee_name()
		if self.new_password!=None:
			if self.user!=None:
				emp_user=frappe.get_doc('User', self.email)
				emp_user.new_password=self.new_password
				emp_user.save()	
				self.db_set("new_password",None)
			else:
				self.db_set("new_password",None)	

	def on_trash(self):
		data = frappe.db.get_all("User", {'email':self.email},{'name'})
		if data:
			for usr in frappe.db.get_all("User", {'email':self.email},{'name'}):
				frappe.delete_doc("User",usr.name)

	def after_insert(self):
		self.create_emp_user()
	
	def on_change(self):
		new_email(self)
		
	def before_save(self):
		emply = frappe.get_all("Employee",{"name":self.name},{"role","third_party_employee"})
		if emply:
			if self.role!=emply[0]["role"] or self.third_party_employee!=emply[0]["third_party_employee"]:
				self.role_user()

	def set_employee_name(self):
		self.full_name = ' '.join(filter(lambda x: x, [self.first_name, self.middle_name, self.last_name]))

	def create_emp_user(self):
		if not frappe.db.exists("User", self.email):
			emp_user = frappe.get_doc({
				'doctype':'User',
				'first_name': self.first_name,
				'last_name': self.last_name,
				'email': self.email,
				'gender': self.gender,
				'enabled': self.enabled,
				'username': self.employee_number,
				# 'role_profile_name': self.role_profile,
				'send_welcome_email': 1,
				'user_type': 'Website User'
				})
			emp_user.flags.ignore_permissions = True
			if self.role==None and self.third_party_employee==1:
				emp_user.add_roles("Third Party")
			if self.role!=None and self.third_party_employee==0:
				emp_user.add_roles(self.role)
			if self.role!=None and self.third_party_employee==1:
				emp_user.add_roles("Third Party")
				emp_user.add_roles(self.role)
			emp_user.save()
			self.db_set("user",emp_user.name)

	def enabled_emp(self):
		user_list=frappe.get_all("Employee",{"name":self.name},["enabled"])
		if user_list:
			if self.enabled==0 and user_list[0]["enabled"]==1:
				emp=frappe.db.get_all("User", {'email':self.email},['name','enabled'])
				update_doc = frappe.get_doc("User",emp)
				update_doc.enabled=0
				update_doc.save()
			if self.enabled==1 and user_list[0]["enabled"]==0:
				emp=frappe.db.get_all("User", {'email':self.email},['name','enabled'])
				update_doc = frappe.get_doc("User",emp)
				update_doc.enabled=1
				update_doc.save()

	def role_user(self):
		rol_user = frappe.db.get_all("User",filters=[["email","=",self.email]],fields=["name"])
		if rol_user:
			emp_user = frappe.get_doc('User', self.email)
			user_roles = frappe.get_roles()
			if self.role!=None and self.third_party_employee==0:	
				emp_user.remove_roles(*user_roles)
				emp_user.flags.ignore_permissions = True
				emp_user.add_roles(self.role)
			if self.role==None and self.third_party_employee==1:
				emp_user.remove_roles(*user_roles)
				emp_user.flags.ignore_permissions = True
				emp_user.add_roles("Third Party")
			if self.role!=None and self.third_party_employee==1:
				emp_user.remove_roles(*user_roles)
				emp_user.flags.ignore_permissions = True
				emp_user.add_roles("Third Party")
				emp_user.add_roles(self.role)
			if self.role==None and self.third_party_employee==0:
				emp_user.remove_roles(*user_roles)
				emp_user.flags.ignore_permissions = True
			emp_user.save()
	
def new_email(self):
	emp_data= frappe.get_all("Employee",{"name":self.name},['email','user'])
	if emp_data:
		if emp_data[0]["user"]!=self.email:
			old_user=emp_data[0]["user"]
			frappe.rename_doc("User", old_user, self.email)
			frappe.db.commit()
			user=frappe.get_doc("User",self.email)
			user.email=self.email
			user.save()
			self.db_set("user",user.name)

