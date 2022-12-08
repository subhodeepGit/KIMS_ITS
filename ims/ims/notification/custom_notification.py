from re import L
import frappe
from frappe.utils.data import format_date
from frappe.utils import get_url_to_form
from frappe.utils import cint, cstr, parse_addr
# from stripe import Recipient

def supplier_payment_initiazation(self):
    sub="""<p><b>Your payment is Initiated</b></p><br>"""
    msg="""<b>Thank You</b><br>"""
    # send_mail(frappe.db.get_value("Student Applicant",doc.get('name'),"student_email_id"),'Application status',msg) [{},{},{}] "email_id"
    send_mail(frappe.get_all("Supplier",{"name":self.supplier_code},["email_id"])[0]["email_id"],sub,msg)

def designation_wise_email(self):
    sub="""<p><b>Workflow received for Approval</b></p><br>"""
    msg="""<b>Thank You</b><br>"""
    doctype_name = self.doctype
    active_workflow = frappe.get_all("Workflow",{"document_type":self.doctype,"is_active":1},["name"])[0]["name"]
    print("\n\n\n\n")
    # print(active_workflow)
    print(self.workflow_state)
    role_to_state = frappe.get_all("Workflow Document State",{"parent":active_workflow,"state":self.workflow_state}, ["allow_edit"])
    role_email = frappe.get_all("Employee",{"designation":role_to_state[0]["allow_edit"]},["email"])
    print(role_email)
    if role_email:
        list_email=[]
        for t in role_email:
            recipients=t['email']
            subject=sub
            message=msg
            if self.doctype == "PO T Kitchen":
                attachments = [frappe.attach_print(self.doctype, self.name, file_name=self.name, print_format='PO Consumable PF')]
            elif self.doctype == "PO Consignment":
                attachments = [frappe.attach_print(self.doctype, self.name, file_name=self.name, print_format='PO Consignment PF')]
            elif self.doctype == "PO Material Management":
                attachments = [frappe.attach_print(self.doctype, self.name, file_name=self.name, print_format='PO Material Management PF')]
            elif self.doctype == "Pharmacy":
                attachments = [frappe.attach_print(self.doctype, self.name, file_name=self.name, print_format='Pharmacy PF')]
            elif self.doctype == "Non PO Contract":
                attachments = [frappe.attach_print(self.doctype, self.name, file_name=self.name, print_format='Non Po Contract PF')]
            elif self.doctype == "Non PO Non Contract":
                attachments = [frappe.attach_print(self.doctype, self.name, file_name=self.name, print_format='Non PO Non Contract PF')]
            elif self.doctype == "Patient Refund":
                attachments = [frappe.attach_print(self.doctype, self.name, file_name=self.name, print_format='Patient Refund PF')]
            send_mail(recipients,subject,message,attachments)

def send_mail(recipients,subject,message,attachments):
    if has_default_email_acc():
        frappe.sendmail(recipients=recipients,subject=subject,message = message,attachments=attachments,with_container=True)

def has_default_email_acc():
    for d in frappe.get_all("Email Account", {"default_outgoing":1}):
       return "true"
    return ""