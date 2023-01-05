import frappe
from datetime import datetime

def employee_user():
    now = datetime.now()
    today = now.strftime("%Y-%m-%d %H:%M:%S")
    absent = frappe.get_all("Absent Employee Replacement",{"docstatus":1},["from_employee","email","role","from_date","to_employee","email1","to_date"])
    cancel = frappe.get_all("Absent Employee Replacement",{"docstatus":2},["from_employee","email","role","from_date","to_employee","email1","to_date"])
    for Nr in cancel:
        employee = frappe.get_doc("User",Nr["email1"])
        if Nr:
            employee.remove_roles(Nr["role"])
            print("3cancel")
            print(Nr["role"])
            employee.flags.ignore_permissions = True
            employee.save()
        employee.save()
    for Nr in absent:
        employee = frappe.get_doc("User",Nr["email1"])
        if Nr:
            from_dt = datetime.strftime(Nr["from_date"], "%Y-%m-%d %H:%M:%S")
            to_dt = datetime.strftime(Nr["to_date"], "%Y-%m-%d %H:%M:%S")
            if Nr["email"] != Nr["email1"]:
                if from_dt <= today <= to_dt:
                    employee.add_roles(Nr["role"])
                    print("1rolegiven")
                    print(Nr["role"])
                    employee.flags.ignore_permissions = True
                    employee.save()
                if to_dt <= today:
                    employee.remove_roles(Nr["role"])
                    print("2roletaken")
                    print(Nr["role"])
                    employee.flags.ignore_permissions = True
                    employee.save()
        employee.save()