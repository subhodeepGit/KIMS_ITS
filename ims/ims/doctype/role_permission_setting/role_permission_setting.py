# Copyright (c) 2022, SOUL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RolePermissionSetting(Document):
	def on_submit(self):
		for t_object in self.get("table_2"):
			role_permissions_manager_cration(t_object,self.role)
	
	def on_cancel(self):
		frappe.throw("Document can not be cancel, Only New Document can be created.")
			

def role_permissions_manager_cration(t_object,role):
	role_permissions_manager_info=frappe.get_all("Custom DocPerm",{"parent":t_object.doctype_name,"role":role})
	if not role_permissions_manager_info:
		role_permissions_manager_doc = frappe.new_doc("Custom DocPerm")
		role_permissions_manager_doc.parent=t_object.doctype_name
		role_permissions_manager_doc.role=role
		role_permissions_manager_doc.permlevel=0
		role_permissions_manager_doc.select=t_object.select
		role_permissions_manager_doc.read=t_object.read
		role_permissions_manager_doc.write=t_object.write
		role_permissions_manager_doc.create=t_object.create
		role_permissions_manager_doc.delete=t_object.del_data
		role_permissions_manager_doc.submit=t_object.submittable
		role_permissions_manager_doc.cancel=0
		role_permissions_manager_doc.amend=0
		role_permissions_manager_doc.report=t_object.report
		role_permissions_manager_doc.export=t_object.export
		role_permissions_manager_doc.share=0
		role_permissions_manager_doc.print=t_object.print
		role_permissions_manager_doc.email=0
		role_permissions_manager_doc.save()
		frappe.db.sql(""" Update `tabCustom DocPerm` set import="%s" where name='%s' """%(t_object.import_data,role_permissions_manager_doc.name))
	else:
		role_permissions_manager_doc=frappe.get_doc("Custom DocPerm", role_permissions_manager_info[0]['name'])
		role_permissions_manager_doc.parent=t_object.doctype_name
		role_permissions_manager_doc.role=role
		role_permissions_manager_doc.permlevel=0
		role_permissions_manager_doc.select=t_object.select
		role_permissions_manager_doc.read=t_object.read
		role_permissions_manager_doc.write=t_object.write
		role_permissions_manager_doc.create=t_object.create
		role_permissions_manager_doc.delete=t_object.del_data
		role_permissions_manager_doc.submit=t_object.submittable
		role_permissions_manager_doc.cancel=0
		role_permissions_manager_doc.amend=0
		role_permissions_manager_doc.report=t_object.report
		role_permissions_manager_doc.export=t_object.export
		role_permissions_manager_doc.share=0
		role_permissions_manager_doc.print=t_object.print
		role_permissions_manager_doc.email=0
		role_permissions_manager_doc.save()
		frappe.db.sql(""" Update `tabCustom DocPerm` set import="%s" where name='%s' """%(t_object.import_data,role_permissions_manager_doc.name))



@frappe.whitelist()
def get_doctype_list(role):
	role_name=role
	# doctype_name = ["Company", "Department", "Employee", "Supplier", "Supplier Group", "Material or Service", "Material or Service Group", "Bank Details For Payment", "Designation"]
	ims_doc=frappe.get_all("DocType",filters={"module":"Ims","istable":0},fields=['name'],order_by="name asc")
	final_list=[]
	for doc in ims_doc:
		role_permission=frappe.get_all("Custom DocPerm",{"parent":doc['name'],"role":role_name},
							["name","select","read","write","create","delete","report","export","import","print"])
		if role_permission:
			list_dic={}
			list_dic['doctype_name']=doc['name']
			list_dic['select']=role_permission[0]["select"]
			list_dic['read']=role_permission[0]["read"]
			list_dic['write']=role_permission[0]["write"]
			list_dic['create']=role_permission[0]["create"]
			list_dic['del_data']=role_permission[0]["delete"]
			list_dic['report']=role_permission[0]["report"]
			list_dic['export']=role_permission[0]["export"]
			list_dic['import_data']=role_permission[0]["import"]
			list_dic['print']=role_permission[0]["print"]
			final_list.append(list_dic)
		else:
			field=["name","select","read","write","create","del_data","report","export","import_data","print"]
			list_dic={}
			list_dic['doctype_name']=doc['name']
			for t in field:
				list_dic[t]=0
			final_list.append(list_dic)
	return final_list