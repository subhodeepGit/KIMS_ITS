# Copyright (c) 2022, SOUL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import datetime

class RolePermissionTool(Document):

	def validate(self):
		role_cration(self)
		role_permissions_manager_cration(self)
		workflow_state_cration(self)
		workflow_action_master_cration(self)
		workflow_creation(self)
		grouping_of_designation_info_section(self)	



def role_cration(self):
	for t in self.get("role_permission_tool_child"):
		role_info=frappe.get_all("Role",{"name":t.designation})
		if not role_info:
			role_doc = frappe.new_doc("Role")
			role_doc.role_name = t.designation
			role_doc.search_bar=0
			role_doc.notifications=1
			role_doc.list_sidebar=0
			role_doc.bulk_actions=0
			role_doc.view_switcher=0
			role_doc.form_sidebar=1
			role_doc.timeline=1
			role_doc.dashboard=1  
			role_doc.save()
def role_permissions_manager_cration(self):
	pre_role_permissions_manager_info=frappe.get_all("Custom DocPerm",{"parent":self.doctype_name},["name",'role'])
	for t in pre_role_permissions_manager_info: 		
		frappe.delete_doc("Custom DocPerm",t["name"])
	if self.doctype_name!="Patient Refund":	
		pre_role_3d_permissions_manager_info=frappe.get_all("Custom DocPerm",{"parent":"Third-Party Verification"},["name",'role'])
		for t in pre_role_3d_permissions_manager_info: 		
			frappe.delete_doc("Custom DocPerm",t["name"])	

	for t in self.get("role_permission_tool_child"):
		role_permissions_manager_info=frappe.get_all("Custom DocPerm",{"parent":self.doctype_name,"role":t.designation})
		if not role_permissions_manager_info:
			role_permissions_manager_doc = frappe.new_doc("Custom DocPerm")
			role_permissions_manager_doc.parent=self.doctype_name
			role_permissions_manager_doc.role=t.designation
			role_permissions_manager_doc.permlevel=0
			role_permissions_manager_doc.select=1
			role_permissions_manager_doc.read=1
			role_permissions_manager_doc.write=1
			if t.idx==1:
				role_permissions_manager_doc.create=1
			else:
				role_permissions_manager_doc.create=0	
			role_permissions_manager_doc.delete=0
			role_permissions_manager_doc.submit=0
			role_permissions_manager_doc.cancel=0
			role_permissions_manager_doc.amend=0
			role_permissions_manager_doc.report=1
			role_permissions_manager_doc.export=1
			role_permissions_manager_doc.share=0
			role_permissions_manager_doc.print=1
			role_permissions_manager_doc.email=0
			role_permissions_manager_doc.save()
			frappe.db.sql(""" Update `tabCustom DocPerm` set import=1 where name='%s' """%(role_permissions_manager_doc.name))

		if self.doctype_name!="Patient Refund":
			role_3rd_party_permissions_manager_info=frappe.get_all("Custom DocPerm",{"parent":"Third-Party Verification","role":t.designation})
			if not role_3rd_party_permissions_manager_info:
				role_3rd_permissions_manager_doc = frappe.new_doc("Custom DocPerm")
				role_3rd_permissions_manager_doc.parent="Third-Party Verification"
				role_3rd_permissions_manager_doc.role=t.designation
				role_3rd_permissions_manager_doc.permlevel=0
				role_3rd_permissions_manager_doc.select=1
				role_3rd_permissions_manager_doc.read=1
				role_3rd_permissions_manager_doc.write=0
				role_3rd_permissions_manager_doc.create=0
				role_3rd_permissions_manager_doc.delete=0
				role_3rd_permissions_manager_doc.submit=0
				role_3rd_permissions_manager_doc.cancel=0
				role_3rd_permissions_manager_doc.amend=0
				role_3rd_permissions_manager_doc.report=1
				role_3rd_permissions_manager_doc.export=0
				role_3rd_permissions_manager_doc.share=0
				role_3rd_permissions_manager_doc.print=1
				role_3rd_permissions_manager_doc.email=0
				role_3rd_permissions_manager_doc.save()
				frappe.db.sql(""" Update `tabCustom DocPerm` set import=0 where name='%s' """%(role_permissions_manager_doc.name))	



def workflow_state_cration(self):
	for t in self.get("role_permission_tool_child"):
		if t.idx==1:
			list_info=["Draft","Verify and Save","Verified & Submitted by Note Creator","Rejected and Transfer","Cancelled"]
			for z in list_info:
				workflow_state_info=frappe.get_all("Workflow State",{"name":z},['name','style'])
				name=z
				if not workflow_state_info:
					workflow_state=frappe.new_doc("Workflow State")
					workflow_state.name=name
					workflow_state.workflow_state_name=name
					workflow_state.style=t.style
					workflow_state.save()
				if workflow_state_info:
					if workflow_state_info[0]['style']!=t.style:
						workflow_state=frappe.get_doc("Workflow State", name)
						workflow_state.style=t.style
						workflow_state.save()
		else:
			if t.description_of_state==None or t.description_of_state=="":	
				name="Approved by "+t.designation
			else:
				name=t.description_of_state	
			workflow_state_info=frappe.get_all("Workflow State",{"name":name},['name','style'])
			if not workflow_state_info:
				workflow_state=frappe.new_doc("Workflow State")
				workflow_state.name=name
				workflow_state.workflow_state_name=name
				workflow_state.style=t.style
				workflow_state.save()
			if workflow_state_info:
				if workflow_state_info[0]['style']!=t.style:
					workflow_state=frappe.get_doc("Workflow State", name)
					workflow_state.style=t.style
					workflow_state.save()

	list_info=["Passed for Payment"]
	workflow_state_info=frappe.get_all("Workflow State",{"name":list_info[0]},['name','style'])
	if not workflow_state_info:
		workflow_state=frappe.new_doc("Workflow State")
		workflow_state.name=list_info[0]
		workflow_state.workflow_state_name=list_info[0]
		workflow_state.style="Success"
		workflow_state.save()
	else:
		workflow_state=frappe.get_doc("Workflow State",list_info[0])
		workflow_state.style="Success"
		workflow_state.save()
		


def workflow_action_master_cration(self):
	list_action=["Verify and Save","Cancel","Submit","Approve","Reject and Transfer"]
	for t in list_action:
		workflow_action_master_info=frappe.get_all("Workflow Action Master",{"name":t})
		if not workflow_action_master_info:
			workflow_action_master=frappe.new_doc("Workflow State")
			workflow_action_master.name=t
			workflow_action_master.workflow_action_name=t
			workflow_action_master.save()

def workflow_creation(self):
	workflow_doc_info=frappe.get_all("Workflow",{"document_type":self.doctype_name})
	workflow_name=self.doctype_name+"_"+str(len(workflow_doc_info)+1)
	self.workflow_name=workflow_name

	workflow_doc = frappe.new_doc("Workflow")
	workflow_doc.workflow_name=workflow_name
	workflow_doc.document_type=self.doctype_name
	workflow_doc.is_active=1
	workflow_doc.override_status=0
	workflow_doc.send_email_alert=1
	workflow_doc.workflow_state_field="workflow_state"
	################################### Workflow Document State child doctype
	for t in self.get("role_permission_tool_child"):
		if t.idx==1:
			role_name=t.designation
			grouping_of_designation=t.grouping_of_designation
			single_user=t.single_user
			list_state=[{"state":"Draft","update_value":"Invoice in Draft State"},{"state":"Verify and Save","update_value":"Document save"},
						{"state":"Cancelled","update_value":"Document cancelled Note Keeper"}]
			for state in list_state:
				workflow_doc.append("states",{
					"state":state["state"],
					"doc_status":0,
					"update_field":"document_status",
					"update_value":state['update_value'],
					"allow_edit":role_name,
					"grouping_of_designation":grouping_of_designation,
					"single_user":single_user
				})

			name="Rejected and Transfer"
			update_value="Rejected and Transfer"
			workflow_doc.append("states",{
				"state":name,
				"doc_status":0,
				"update_field":"document_status",
				"update_value":update_value,
				"allow_edit":role_name,					
				"grouping_of_designation":grouping_of_designation,
				"single_user":single_user
			})
			for j in self.get("role_permission_tool_child"):
				new_j=t.idx+1
				if j.idx==new_j:
					list_state=[{"state":"Verified & Submitted by Note Creator","update_value":"Submitted by Note Keeper"}]
					name=list_state[0]["state"]
					update_value=list_state[0]['update_value']
					role_name=j.designation
					single_user=j.single_user
					grouping_of_designation=j.grouping_of_designation
					workflow_doc.append("states",{
								"state":name,
								"doc_status":0,
								"update_field":"document_status",
								"update_value":update_value,
								"allow_edit":role_name,
								"single_user":single_user,
								"grouping_of_designation":grouping_of_designation
							})
		
		else:
			flag="No"
			for j in self.get("role_permission_tool_child"):
				new_j=t.idx+1
				if j.idx==new_j:
					flag="Yes"
					if t.description_of_state==None or t.description_of_state=="":	
						name="Approved by "+t.designation
					else:
						name=t.description_of_state

					if t.description_of_state==None or t.description_of_state=="":
						update_value="Submitted by "+t.designation
					else:
						update_value=t.description_of_state

					role_name=j.designation
					single_user=t.single_user
					grouping_of_designation=t.grouping_of_designation
					workflow_doc.append("states",{
							"state":name,
							"doc_status":0,
							"update_field":"document_status",
							"update_value":update_value,
							"allow_edit":role_name,
							"single_user":single_user,
							"grouping_of_designation":grouping_of_designation
						})		

			if flag=="No":
				update_value="Submitted by "+t.designation
				if t.description_of_state==None or t.description_of_state=="":	
					name="Approved by "+t.designation
				else:
					name=t.description_of_state
				
				if t.description_of_state==None or t.description_of_state=="":
					update_value="Submitted by "+t.designation
				else:
					update_value=t.description_of_state	
				role_name=t.designation
				single_user=t.single_user
				grouping_of_designation=t.grouping_of_designation	
				workflow_doc.append("states",{
						"state":name,
						"doc_status":0,
						"update_field":"document_status",
						"update_value":update_value,
						"allow_edit":role_name,
						"single_user":single_user,
						"grouping_of_designation":grouping_of_designation
					})
				############################# pass for payment
				name="Passed for Payment"
				update_value="Passed for Payment"
				workflow_doc.append("states",{
						"state":name,
						"doc_status":0,
						"update_field":"document_status",
						"update_value":update_value,
						"allow_edit":role_name,
						"single_user":single_user,
						"grouping_of_designation":grouping_of_designation
					})

	############################################## Workflow Transition child doc
	for t in self.get("role_permission_tool_child"):
		if t.idx==1:
			list_state=[{"state":"Draft","action":"Verify and Save","next_state":"Verify and Save"},
					{"state":"Draft","action":"Cancel","next_state":"Cancelled"},
					{"state":"Verify and Save","action":"Submit","next_state":"Verified & Submitted by Note Creator"},
					]
			for states in list_state:		
				state=states['state']
				action=states['action']
				next_state=states['next_state']
				allowed=t.designation	
				workflow_doc.append("transitions",{
					"state":state,
					"action":action,
					"next_state":next_state,
					"allowed":allowed,
					"allow_self_approval":1,
				})

			new_j=t.idx+1
			for j in self.get("role_permission_tool_child"):
				if j.idx==new_j:
					list_state=[{"state":"Verified & Submitted by Note Creator"}]
					name=list_state[0]["state"]
					if j.description_of_state==None or j.description_of_state=="":
						next_state="Approved by "+j.designation
					else:
						next_state=j.description_of_state

					allowed=j.designation
					# condition=""

					if j.approve==1:	
						state=name
						action="Approve"
						next_state=next_state

						workflow_doc.append("transitions",{
							"state":state,
							"action":action,
							"next_state":next_state,
							"allowed":allowed,
							"allow_self_approval":1,
							# "condition":condition,
						})

					if j.reject==1:	
						state=name
						action="Reject"
						next_state="Cancelled"			
						workflow_doc.append("transitions",{
							"state":state,
							"action":action,
							"next_state":next_state,
							"allowed":allowed,
							"allow_self_approval":1,
							# "condition":condition,
						})
					if j.reject_and_transfer==1:	
						state=name
						action="Reject and Transfer"
						next_state=next_state		
						workflow_doc.append("transitions",{
							"state":state,
							"action":action,
							"next_state":next_state,
							"allowed":allowed,
							"allow_self_approval":1,
							# "condition":condition,
						})

		else:
			flag="No"
			new_j=t.idx+1
			for j in self.get("role_permission_tool_child"):
				if j.idx==new_j:
					flag="Yes"
					if t.description_of_state==None or t.description_of_state=="":	
						name="Approved by "+t.designation
					else:
						name=t.description_of_state
					allowed=j.designation
					if j.description_of_state==None or j.description_of_state=="":
						next_state="Approved by "+j.designation
					else:
						next_state=j.description_of_state
					
					condition=""
					if j.select_14=="Non Inclusive":
						if j.amount_grater!=0 and j.amount_smaller==0:
							condition="doc.net_final_amount_to_be_paid_in_rs>=%s "%(j.amount_grater)
						elif j.amount_grater==0 and j.amount_smaller!=0:	
							condition="doc.net_final_amount_to_be_paid_in_rs<=%s "%(j.amount_smaller)
						elif j.amount_grater!=0 and j.amount_smaller!=0:	
							condition="doc.net_final_amount_to_be_paid_in_rs>=%s and doc.net_final_amount_to_be_paid_in_rs<=%s "%(j.amount_grater,j.amount_smaller)	


					if t.approve==1:	
						state=name
						action="Approve"
						next_state=next_state				
						workflow_doc.append("transitions",{
							"state":state,
							"action":action,
							"next_state":next_state,
							"allowed":allowed,
							"allow_self_approval":1,
							"condition":condition,
						})

					if t.reject==1:	
						state=name
						action="Reject"
						next_state="Cancelled"			
						workflow_doc.append("transitions",{
							"state":state,
							"action":action,
							"next_state":next_state,
							"allowed":allowed,
							"allow_self_approval":1,
							"condition":condition,
						})

					if t.reject_and_transfer==1:	
						state=name
						action="Reject and Transfer"
						next_state=next_state			
						workflow_doc.append("transitions",{
							"state":state,
							"action":action,
							"next_state":next_state,
							"allowed":allowed,
							"allow_self_approval":1,
							"condition":condition,
						})
			if flag=="No":
				if t.description_of_state==None or t.description_of_state=="":	
					name="Approved by "+t.designation
				else:
					name=t.description_of_state
				allowed=t.designation
				next_state="Passed for Payment"
				
				if t.approve==1:	
					state=name
					action="Approve"
					next_state=next_state				
					workflow_doc.append("transitions",{
						"state":state,
						"action":action,
						"next_state":next_state,
						"allowed":allowed,
						"allow_self_approval":1,
					})

				if t.reject==1:	
					state=name
					action="Reject"
					next_state=next_state		
					workflow_doc.append("transitions",{
						"state":state,
						"action":action,
						"next_state":next_state,
						"allowed":allowed,
						"allow_self_approval":1,
					})

				if t.reject_and_transfer==1:	
					state=name
					action="Reject and Transfer"
					next_state=next_state		
					workflow_doc.append("transitions",{
						"state":state,
						"action":action,
						"next_state":next_state,
						"allowed":allowed,
						"allow_self_approval":1,
					})
	for t in self.get("role_permission_tool_child"):
		if t.idx!=1:
			if t.amount_grater!=0 and t.amount_smaller!=0:
				new_idx=t.idx-1
				for j in self.get("role_permission_tool_child"):
					if j.idx==new_idx:
						if j.description_of_state==None or j.description_of_state=="":	
							name="Approved by "+j.designation
						else:
							name=j.description_of_state

				if t.amount_grater!=0 and t.amount_smaller==0:
					condition="doc.net_final_amount_to_be_paid_in_rs>=%s "%(t.amount_grater)
				elif t.amount_grater==0 and t.amount_smaller!=0:	
					condition="doc.net_final_amount_to_be_paid_in_rs<=%s "%(t.amount_smaller)
				elif t.amount_grater!=0 and t.amount_smaller!=0:	
					condition="doc.net_final_amount_to_be_paid_in_rs>=%s and doc.net_final_amount_to_be_paid_in_rs<=%s "%(t.amount_grater,t.amount_smaller)	

				new_idx=t.idx+1
				flag="Yes"
				for j in self.get("role_permission_tool_child"):
					if j.idx==new_idx:
						flag="No"
						if j.description_of_state==None or j.description_of_state=="":
							next_state="Approved by "+j.designation
						else:
							next_state=j.description_of_state
						allowed=j.designation	


				if flag=="No":
					if t.approve==1:	
						state=name
						action="Approve"
						next_state=next_state				
						workflow_doc.append("transitions",{
							"state":state,
							"action":action,
							"next_state":next_state,
							"allowed":allowed,
							"allow_self_approval":1,
							"condition":condition,
						})
					
					if t.reject==1:	
						state=name
						action="Reject"
						next_state=next_state		
						workflow_doc.append("transitions",{
							"state":state,
							"action":action,
							"next_state":next_state,
							"allowed":allowed,
							"allow_self_approval":1,
						})

					if t.reject_and_transfer==1:	
						state=name
						action="Reject and Transfer"
						next_state=next_state		
						workflow_doc.append("transitions",{
							"state":state,
							"action":action,
							"next_state":next_state,
							"allowed":allowed,
							"allow_self_approval":1,
						})	

	workflow_doc.save()
	self.db_set("workflow_name",workflow_doc.name)
	date = datetime.date.today()
	self.db_set("posting_date",date)

def grouping_of_designation_info_section(self):
	grouping_of_designation_info=[]
	for t in self.get("role_permission_tool_child"):
		if t.grouping_of_designation!=None and t.grouping_of_designation!="":
			grouping_of_designation_info.append(t.grouping_of_designation)

	grouping_of_designation_info=list(set(grouping_of_designation_info))
	grouping_of_designation_info.sort()

	if not self.get("head_name"):
		for t in grouping_of_designation_info:
			self.append("head_name",{                                     
					"lable_name":t,                                       
					"name_of_the_group":t,                                                                   
				})
	else:
		for t in grouping_of_designation_info:
			flag="No"
			for j in self.get("head_name"):
				if j.lable_name==t:
					flag="Yes"
					break
			if flag=="No":
				self.append("head_name",{                                     
					"lable_name":t,                                       
					"name_of_the_group":t,                                                                   
				})	
