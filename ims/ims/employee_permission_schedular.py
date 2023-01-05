import frappe
from datetime import datetime

def employee_user():
    now = datetime.now()
    today = now.strftime("%Y-%m-%d %H:%M:%S")
    absent = frappe.get_all("Absent Employee Replacement",{"docstatus":1},["from_employee","email","role","from_date","to_employee","email1","to_date"])
    cancel = frappe.get_all("Absent Employee Replacement",{"docstatus":2},["from_employee","email","role","from_date","to_employee","email1","to_date"])
    for Nr in cancel:
        if Nr:
            employee = frappe.get_doc("User",Nr.email1)
            employee.remove_roles("Translator")
            employee.flags.ignore_permissions = True
            employee.save()
        employee.save()
    for Nr in absent:
        if Nr:
            from_dt = datetime.strftime(Nr.from_date, "%Y-%m-%d %H:%M:%S")
            to_dt = datetime.strftime(Nr.to_date, "%Y-%m-%d %H:%M:%S")
            if Nr.email != Nr.email1:
                if from_dt <= today <= to_dt:
                    employee = frappe.get_doc("User",Nr.email1).add_roles(Nr.role)
                    employee.add_roles("Translator")
                    employee.flags.ignore_permissions = True
                    employee.save()
                if to_dt <= today:
                    employee = frappe.get_doc("User",Nr.email1)
                    employee.remove_roles("Translator")
                    employee.flags.ignore_permissions = True
                    employee.save()

# def can():
#     can= frappe.get_all("Absent Employee Replacement",{"docstatus":1},["name"])
#     for Nr in can:
#         if Nr:
#             employee = frappe.get_doc("Absent Employee Replacement",Nr.name)
#             employee.cancel()
            