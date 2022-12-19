import frappe
from datetime import datetime

def employee_user():
    now = datetime.now()
    today = now.strftime("%Y-%m-%d %H:%M:%S")
    absent = frappe.get_all("Absent Employee Replacement",{"docstatus":1},["from_employee","email","role","from_date","to_employee","email1","to_date"])
    cancel = frappe.get_all("Absent Employee Replacement",{"docstatus":2},["from_employee","email","role","from_date","to_employee","email1","to_date"])
    from_dt = datetime.strftime(absent[0]["from_date"], "%Y-%m-%d %H:%M:%S")
    to_dt = datetime.strftime(absent[0]["to_date"], "%Y-%m-%d %H:%M:%S")
    if absent:
        if absent[0]["email"] != absent[0]["email1"]:
            if from_dt <= today <= to_dt:
                employee = frappe.get_doc("User",absent[0]["email1"])
                employee.add_roles(absent[0]["role"])
                employee.flags.ignore_permissions = True
                employee.save()
            else:
                employee = frappe.get_doc("User",absent[0]["email1"])
                employee.remove_roles(absent[0]["role"])
                employee.flags.ignore_permissions = True
                employee.save()
    if cancel:
        employee = frappe.get_doc("User",absent[0]["email1"])
        employee.remove_roles(absent[0]["role"])
        employee.flags.ignore_permissions = True
        employee.save()