# Copyright (c) 2022, SOUL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime
from ims.employee_permission_schedular import employee_user

class AbsentEmployeeReplacement(Document):  
    # def on_submit(self):
    #     employee = frappe.get_doc("User",self.email1)
    #     employee.add_roles("Accounts Clerk")
    def validate(self):
        now = datetime.now()
        today = now.strftime("%Y-%m-%d %H:%M:%S")		
        if self.email == self.email1:
            frappe.throw("Employee Name is same in both <b>From Employee</b> and <b>To Employee</b>")
        if self.role == self.role1:
            frappe.throw("Role is same in both Employee")
        if today >= self.to_date:
            frappe.throw("<b>To Date</b> must be greater than today date or current time")
        # if self.from_date <= today:
        #     frappe.throw("<b>From Date</b> must be greater than today date or current time")
        if self.from_date >= self.to_date:
            frappe.throw("<b>To Date</b> must be greater than <b>From date</b>")

    # def on_cancel(self):
    #     employee = frappe.get_doc("User",self.email1)
    #     employee.remove_roles(self.role)
    #     employee.flags.ignore_permissions = True
    #     employee.save()
