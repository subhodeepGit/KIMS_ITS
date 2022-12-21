from re import L
import frappe
from frappe.utils.data import format_date
from frappe.utils import get_url_to_form
from frappe.utils import cint, cstr, parse_addr
from frappe import utils
# from stripe import Recipient

def supplier_payment_initiazation(self):
    sub="""<p><b>Your payment is Initiated</b></p><br>"""
    msg="""<b>Thank You</b><br>"""
    # send_mail(frappe.db.get_value("Student Applicant",doc.get('name'),"student_email_id"),'Application status',msg) [{},{},{}] "email_id"
    attachments = None
    send_mail(frappe.get_all("Supplier",{"name":self.supplier_code},["email_id"])[0]["email_id"],sub,msg,attachments)

def supplier_passforpayment(self):
    sub="""<p><b>Your Invoice is verified and passed for payment</b></p><br>"""
    msg="""<b>Thank You</b><br>"""
    attachments = None
    send_mail(frappe.get_all("Supplier",{"name":self.supplier_code},["email_id"])[0]["email_id"],sub,msg,attachments)

def supplier_finalpayment(self):
    sub="""Your payment is Done"""
    msg="""<b>Thank You</b><br>"""
    attachments = None
    vendor_code = frappe.get_all("Vendor Wise Payment Details",{"parent":self.name},["vendor_code"])
    vendor=vendor_code[0]["vendor_code"]
    vendor_email=frappe.get_all("Supplier",{"name":vendor},["email_id"])
    send_mail(vendor_email[0]["email_id"],sub,msg,attachments)

def thirdparty_email(user):
    receipient = user
    sub = "<b>NoteSheet received for Verification</b>"
    msg = "<b>Thank You</b>"
    attachments = None
    send_mail(receipient,sub,msg,attachments)


def designation_wise_email(self):
    sub="""<p><b>Workflow received for Approval</b></p><br>"""
    msg="""<b>Thank You</b><br>"""
    doctype_name = self.doctype
    active_workflow = frappe.get_all("Workflow",{"document_type":self.doctype,"is_active":1},["name"])[0]["name"]
    role_to_state = frappe.get_all("Workflow Document State",{"parent":active_workflow,"state":self.workflow_state}, ["allow_edit"])
    role_email = frappe.get_all("Employee",{"designation":role_to_state[0]["allow_edit"]},["email"])
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


def report_scheduler(emp_wf,inward_letter,final_passed_for_payment,payment_section,cancelation_section,final_passed_paymen,field):
        # table="""
    #         <table border=1>
    #             <tr>
    #                 <th>Company</th>
    #                 <th>Contact</th>
    #                 <th>Country</th>
    #             </tr>
    #             <tr>
    #                 <td>Alfreds Futterkiste</td>
    #                 <td>Maria Anders</td>
    #                 <td>Germany</td>
    #             </tr>
    #         </table>
    #         """Pharmacy         
    date_time=str(utils.now())[:19]
    msg=""""""
    ################################################################# Payment Status  ##################################################
    ####### Section Head
    msg =msg+ "<p><b>Details Of Batch Payment Document where status changed to Payment Done as on %s</b></p> <br><br>"%(date_time)
    ########## end of Section Head

    ################## Doctype present in set and filtering doctype name
    name_doc_type=[]
    for type_doc in payment_section:
        name_doc_type.append(type_doc['doc_type'])     
    name_doc_type=list(set(name_doc_type))
    ######################## end Doctype present in set and filtering doctype name
    
    c=""
    for t in name_doc_type:
        ################### Filtering coloum name and coloum name 
        coloum=[]
        for j in field:
            if j['parent']==t:
                coloum.append(j)
        # [{'label': 'Cheque Date', 'fieldname': 'cheque_date', 'parent': 'Batch Payment Process'}]
        ################### end Filtering coloum name and coloum name
        
        ################### Table name in HTML  
        table_head="""<p>Notesheet Name %s</p><br>"""%(t)
        ################### end Table name in HTML

        ############ Coloum Name   
        c1=""" <table border=1>
                    <tr>
                    <th>Document No</th>"""
        c2=""            
        for j in coloum:
            c2=c2+"""<th>%s</th>"""%(j['label'])
        c1=c1+c2
        c1=c1+"""</tr>"""
        ################# end Coloum Name
        ############## Data of the coloum 
        c3=""
        for j in payment_section:
            c4=""
            if j["doc_type"]==t:
                c4="""<td>%s</td>"""%(j['name'])
                for k in coloum:
                    c4=c4+"""<td>%s</td>"""%(j[k['fieldname']])
            if c4!="":        
                c3=c3+"<tr>"+c4+"</tr>"

        c=c+table_head+c1+c3+"</table><br>"
        ####################### end Data of the coloum
    ################### merging table to main Messager     
    if c!="":
        msg=msg+c
    else:
        msg=msg+"""<br><p>No Batch Payment Found</p><br>"""
    ################### end merging table to main Messager          
    #############################################################end Payment Status #############################################################

    ####################################################### Inward letter
    ####### Section Head
    msg =msg+ "<p><b>Notesheet Received For Approval as on %s</b></p> <br><br>"%(date_time)
    ########## end of Section Head
    name_doc_type=[]
    for type_doc in inward_letter:
        name_doc_type.append(type_doc['document_type'])     
    name_doc_type=list(set(name_doc_type))


    c=""
    for t in name_doc_type:
        ################### Filtering coloum name and coloum name 
        coloum=[]
        for j in field:
            if j['parent']==t:
                coloum.append(j)
        # [{'label': 'Cheque Date', 'fieldname': 'cheque_date', 'parent': 'Batch Payment Process'}]
        ################### end Filtering coloum name and coloum name
        
        ################### Table name in HTML  
        table_head="""<p>Notesheet Name %s</p><br>"""%(t)
        ################### end Table name in HTML
        ############ Coloum Name   
        c1=""" <table border=1>
                    <tr>
                    <th>Document No</th>"""
        c2=""            
        for j in coloum:
            c2=c2+"""<th>%s</th>"""%(j['label'])
        c1=c1+c2
        c1=c1+"""</tr>"""
        ################# end Coloum Name
        ############## Data of the coloum 
        c3=""
        for j in inward_letter:
            c4=""
            if j["document_type"]==t:
                c4="""<td>%s</td>"""%(j['name'])
                for k in coloum:
                    c4=c4+"""<td>%s</td>"""%(j[k['fieldname']])
            if c4!="":        
                c3=c3+"<tr>"+c4+"</tr>"

        c=c+table_head+c1+c3+"</table><br>"
        ####################### end Data of the coloum
    ################### merging table to main Messager     
    if c!="":
        msg=msg+c
    else:
        msg=msg+"""<br><p>No New Task Found For Approval</p><br>"""
    ####################################################### end Inward letter ##############################################################
    ######################### Pass for payment Section
    ####### Section Head
    msg =msg+ "<p><b>Notesheet Passed For Payment as on %s</b></p> <br><br>"%(date_time)
    ########## end of Section Head
    name_doc_type=[]
    for type_doc in final_passed_for_payment:
        name_doc_type.append(type_doc['doc_type'])     
    name_doc_type=list(set(name_doc_type))
    
    c=""
    for t in name_doc_type:
        ################### Filtering coloum name and coloum name 
        coloum=[]
        for j in field:
            if j['parent']==t:
                coloum.append(j)      
        ################### Table name in HTML  
        table_head="""<p>Notesheet Name %s</p><br>"""%(t)
        ################### end Table name in HTML

        ############ Coloum Name   
        c1=""" <table border=1>
                    <tr>
                    <th>Document No</th>"""
        c2=""            
        for j in coloum:
            c2=c2+"""<th>%s</th>"""%(j['label'])
        
        c1=c1+c2
        c1=c1+"""</tr>"""
        ################# end Coloum Name
        ############## Data of the coloum
        c3=""
        for j in final_passed_for_payment:
            c4=""
            if j["doc_type"]==t:
                c4="""<td>%s</td>"""%(j['name'])
                for k in coloum:
                    c4=c4+"""<td>%s</td>"""%(j[k['fieldname']])
            if c4!="":        
                c3=c3+"<tr>"+c4+"</tr>"

        c=c+table_head+c1+c3+"</table><br>"
        ####################### end Data of the coloum
    ################### merging table to main Messager     
    if c!="":
        msg=msg+c
    else:
        msg=msg+"""<br><p>No Doument found for Passed For Payment</p><br>""" 
    ################################################################### Pass for payment Section #########################################################
    ############################ Final payment Section

    ####### Section Head
    msg =msg+ "<p><b>Final Payment Section as on %s</b></p> <br><br>"%(date_time)
    ########## end of Section Head
    name_doc_type=[]
    for type_doc in final_passed_paymen:
        name_doc_type.append(type_doc['doc_type'])     
    name_doc_type=list(set(name_doc_type))
    
    c=""
    for t in name_doc_type:
        ################### Filtering coloum name and coloum name 
        coloum=[]
        for j in field:
            if j['parent']==t:
                coloum.append(j)
        ################### Table name in HTML  
        table_head="""<p>Notesheet Name %s</p><br>"""%(t)
        ################### end Table name in HTML        
        
        ############ Coloum Name   
        c1=""" <table border=1>
                    <tr>
                    <th>Document No</th>"""
        c2=""            
        for j in coloum:
            c2=c2+"""<th>%s</th>"""%(j['label'])
        c1=c1+c2
        c1=c1+"""</tr>"""
        ################# end Coloum Name
        ############## Data of the coloum
        c3=""
        for j in final_passed_for_payment:
            c4=""
            if j["doc_type"]==t:
                c4="""<td>%s</td>"""%(j['name'])
                for k in coloum:
                    c4=c4+"""<td>%s</td>"""%(j[k['fieldname']])
            if c4!="":        
                c3=c3+"<tr>"+c4+"</tr>"

        c=c+table_head+c1+c3+"</table><br>"
        ####################### end Data of the coloum
    ################### merging table to main Messager     
    if c!="":
        msg=msg+c
    else:
        msg=msg+"""<br><p>No Doument found for Passed For Payment</p><br>""" 
    ########################################################### END Final payment Section   ############################################## 
    # emp_wf=['name','role','full_name','employee_number','email','department']
    receipient = emp_wf['email']
    sub = """<b> MIS Report for Employee %s as on %s </b>"""%(emp_wf['email'],date_time)
    msg = msg
    attachments = None
    send_mail(receipient,sub,msg,attachments)    
             

        
    


                 




            







def send_mail(recipients,subject,message,attachments):
    if has_default_email_acc():
        frappe.sendmail(recipients=recipients,subject=subject,message = message,attachments=attachments,with_container=True)

def has_default_email_acc():
    for d in frappe.get_all("Email Account", {"default_outgoing":1}):
       return "true"
    return ""

