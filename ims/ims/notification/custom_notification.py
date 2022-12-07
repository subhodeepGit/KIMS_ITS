from re import L
import frappe
from frappe.utils.data import format_date
from frappe.utils import get_url_to_form
from frappe.utils import cint, cstr, parse_addr

def po(self):
    sub="""<p><b>Your payment is Initiated</b></p><br>"""
    msg="""Thank You</b><br>"""
    # send_mail(frappe.db.get_value("Student Applicant",doc.get('name'),"student_email_id"),'Application status',msg) [{},{},{}] "email_id"
    send_mail(frappe.get_all("Supplier",{"name":self.supplier_code},["email_id"])[0]["email_id"],sub,msg)

def send_mail(recipients,subject,message):
    if has_default_email_acc():
        frappe.sendmail(recipients=recipients,subject=subject,message = message)

def has_default_email_acc():
    for d in frappe.get_all("Email Account", {"default_outgoing":1}):
       return "true"
    return ""