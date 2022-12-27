import frappe
from frappe import utils
from datetime import timedelta,date
from ims.ims.notification.custom_notification import report_scheduler,report_scheduler_reject_trasfer,report_holder_notesheet,notesheet_reminder_mail



def cron_tab():
    # bench --site erp.soulunileaders.com execute ims.tasks.cron_tab
    doctype_name=['PO Consumable',"PO Consignment","PO Material Management","Pharmacy","Non PO Contract","Non PO Non Contract",
                "Patient Refund","Batch Payment Process"]

    genral_field_list= ['name','note_sheet_no','posting_date','item_of_purchaseexpense','supplier_code','name_of_supplier','total_amount_in_rs',
                        'tds_amount_to_be_deducted_in_rs','advance_amount_already_paid_in_rs','net_final_amount_to_be_paid_in_rs','document_status']
    po_consignment_field_list=['name','note_sheet_no','posting_date','item_of_purchaseexpense','total_hospital_margin_amount','supplier_code','name_of_supplier',
                                            'to_pay_total','total_amount_in_rs','less_credit_note_amount_in_rs','net_final_amount_to_be_paid_in_rs','document_status'] 
    pharmacy_field_list=['name','note_sheet_no','posting_date','item_of_purchaseexpense','supplier_code','name_of_supplier','total_amount'
                                    ,'advance_amount_already_paid_in_rs','net_final_amount_to_be_paid_in_rs','document_status']
    patient_refund_field_list=['name',"type_of_insurance","name_of_the_patient","ip__uhid_no","posting_date","total_bill","approval_of_tpa__insurance__corporate__ostf",
                                    "amount_deposited_by_patient","net_refundable_in_figures",'document_status']
    batch_payment_process=['name',"date","document_status","account_reference_no","bank_ac_no","bank_name","bank_address","account_reference_no",
                                            "account_post_date","audit_reference_no","audit_posting_date","cheque_no","cheque_date","total_amount"]

    emp_date_workflow=frappe.get_all("Employee",[["enabled","=",1],["role","!=","Null"]],
                                        ['name','role','full_name','employee_number','email','department'])
    active_workflow=frappe.get_all("Workflow",{"is_active":1},['name','document_type'])

    doctype_name_filed_map=[{"parent":'PO Consumable',"fieldname":genral_field_list},{"parent":"PO Consignment","fieldname":po_consignment_field_list},
                    {"parent":"PO Material Management","fieldname":genral_field_list},{"parent":"Pharmacy","fieldname":pharmacy_field_list}
                    ,{"parent":"Non PO Contract","fieldname":genral_field_list},{"parent":"Non PO Non Contract","fieldname":genral_field_list},
                {"parent":"Patient Refund","fieldname":patient_refund_field_list},{"parent":"Batch Payment Process","fieldname":batch_payment_process}]

    field=[]
    for t in doctype_name_filed_map:
        fieldname=t["fieldname"]
        for j in fieldname:
            dofield=frappe.get_all("DocField",filters=[["parent","=",t['parent']],["fieldname","=",j]],fields=["label","fieldname","parent"])
            if dofield:
                field.append(dofield[0])      

    for emp_wf in emp_date_workflow:
        emp_name=emp_wf['name']
        if emp_wf['role']!=None and emp_wf['role']!="":
            states_list=[]
            ################################################ Inward Letter
            inward_letter=[]
            for aw in active_workflow:
                workflow_document_state=frappe.get_all("Workflow Document State",[["parent","=",aw['name']],["allow_edit","=",emp_wf['role']]],
                                    ['name','parent','allow_edit','state'])                  
                for t in workflow_document_state:
                    if t['state']!="Draft" and t['state']!="Rejected and Transfer" and t['state']!="Passed for Payment" and t['state']!="Cancelled":
                        t['document_type']=aw['document_type']
                        states_list.append(t)
            for t in states_list:
                if t['document_type']=='PO Consumable' or t['document_type']=='PO Material Management' \
                    or t['document_type']=='Non PO Contract' or t['document_type']=="Non PO Non Contract" or t['document_type']=="Non PO Non Contract":
                    data=frappe.get_all(t['document_type'],{"workflow_state":t['state']},genral_field_list)
                    for j in data:
                        j['document_type']=t['document_type']
                        inward_letter.append(j)                         
                if t['document_type']=='PO Consignment':
                    data=frappe.get_all(t['document_type'],{"workflow_state":t['state']},po_consignment_field_list)
                    for j in data:
                        j['document_type']=t['document_type']
                        inward_letter.append(j)                         
                if t['document_type']=="Pharmacy":
                    data=frappe.get_all(t['document_type'],{"workflow_state":t['state']},pharmacy_field_list)
                    for j in data:
                        j['document_type']=t['document_type']
                        inward_letter.append(j)
                if t['document_type']=="Patient Refund":
                    data=frappe.get_all(t['document_type'],{"workflow_state":t['state']},patient_refund_field_list)
                    for j in data:
                        j['document_type']=t['document_type']
                        inward_letter.append(j)       
            # print(emp_wf['name'])
            # print(inward_letter)
            ######################################## end of Invoice
            ########################################## Master Record preparation                                            
            data=frappe.get_all("Authorized Signature",{"emp_id":emp_name},['name','parent','parenttype',"approval_status","date_of_approval"])
            doc_head=[]
            for t in data:
                doc_head.append(t['parenttype'])
            doc_head=list(set(doc_head))

            doc_dict={} 
            for t in doc_head:
                doc_dict[t]=[]

            ####################################### Pass for Payment section 
            # (Logic - Emp was a part of approval process of note-sheet and note sheet has reached for Passed for Payment but batch payment is not initiated)
            pass_for_payment_section=doc_dict.copy()
            
            for t in data:
                if t["approval_status"]=="Passed for Payment":
                    doc_date=frappe.get_all(t['parenttype'],{"name":t['parent']},['name','payment_status','document_status'])
                    if doc_date[0]['payment_status']==None or doc_date[0]['payment_status']!="Payment Failed":
                        pass_for_payment_section[t['parenttype']].append(t["parent"])
            
            for t in pass_for_payment_section:
                pass_for_payment_section[t]=list(set(pass_for_payment_section[t]))

            final_passed_for_payment=[]
            for t in pass_for_payment_section:
                if t=='PO Consumable' or t=='PO Material Management' \
                    or t=='Non PO Contract' or t=="Non PO Non Contract" or t=="Non PO Non Contract":
                    if pass_for_payment_section[t]:
                        for j in pass_for_payment_section[t]:
                            flag_data=frappe.get_all(t,{"name":j},genral_field_list)
                            flag_data[0]['doc_type']=t
                            final_passed_for_payment.append(flag_data[0])                            
                if t=='PO Consignment':
                    if pass_for_payment_section[t]:
                        for j in pass_for_payment_section[t]:
                            flag_data=frappe.get_all(t,{"name":j},po_consignment_field_list)
                            flag_data[0]['doc_type']=t
                            final_passed_for_payment.append(flag_data[0])                   
                if t=="Pharmacy":
                    if pass_for_payment_section[t]:
                        for j in pass_for_payment_section[t]:
                            flag_data=frappe.get_all(t,{"name":j},pharmacy_field_list)
                            flag_data[0]['doc_type']=t
                            final_passed_for_payment.append(flag_data[0])
                if t=="Patient Refund":
                    if pass_for_payment_section[t]:
                        for j in pass_for_payment_section[t]:
                            flag_data=frappe.get_all(t,{"name":j},patient_refund_field_list)
                            flag_data[0]['doc_type']=t
                            final_passed_for_payment.append(flag_data[0])
            # print(emp_wf['name'])
            # print(final_passed_for_payment)
            ####################################### End Pass for Payment section   
            ####################################### Payment status from batch payment 
            # (Logic:- which of the invoice emp has approved and batch payment is completed with spacification of payment status of the success or failure note sheet spacific as on sys date )
            today_date=utils.nowdate()
            start_time_date="%s 00:00:00"%today_date
            end_time_date="%s 23:59:59"%today_date
            payment_data_bep=frappe.get_all("Authorized Signature",{"date_of_approval":['between', [start_time_date,end_time_date]],"approval_status":"Payment Done"},
                                                           ['name',"parent"])
            final_passed_payment=[]
            if  payment_data_bep:                                             
                list_approved_doc=[]
                for t in payment_data_bep:
                    list_approved_doc.append(t['parent'])

                list_approved_doc=list(set(list_approved_doc))
                filter=[]
                if len(list_approved_doc)==1:
                    filter.append(["batch_payment_no","=",list_approved_doc[0]])
                else:
                    filter.append(["batch_payment_no","IN",list_approved_doc])
                list_of_data=[]    
                for t in doctype_name:
                    if t!="Batch Payment Process":
                        flag_data=frappe.get_all(t,filters=filter,fields=['name'])
                        for j in flag_data:
                            list_of_data.append(j['name'])
                list_of_data=list(set(list_of_data))

                filter=[]
                if len(list_of_data)==1:
                    filter.append(["parent","=",list_of_data[0]])
                else:
                    filter.append(["parent","IN",list_of_data])
                filter.append(["emp_id","=",emp_wf['name']])

                paid_data=frappe.get_all("Authorized Signature",filters=filter,fields=["parent",'parenttype'])
                if paid_data:
                    doc_head=[]
                    for t in paid_data:
                        doc_head.append(t['parenttype'])
                    doc_head=list(set(doc_head))
                    doc_dict={} 
                    for t in doc_head:
                        doc_dict[t]=[]

                    for t in paid_data:
                        doc_dict[t['parenttype']].append(t["parent"])

                    for t in doc_dict:
                        doc_dict[t]=list(set(doc_dict[t]))       
                    
                    for t in doc_dict:
                        if t=='PO Consumable' or t=='PO Material Management' \
                            or t=='Non PO Contract' or t=="Non PO Non Contract" or t=="Non PO Non Contract":
                            if doc_dict[t]:
                                for j in doc_dict[t]:
                                    flag_data=frappe.get_all(t,{"name":j},genral_field_list)
                                    flag_data[0]['doc_type']=t
                                    final_passed_payment.append(flag_data[0])                            
                        if t=='PO Consignment':
                            if doc_dict[t]:
                                for j in doc_dict[t]:
                                    flag_data=frappe.get_all(t,{"name":j},po_consignment_field_list)
                                    flag_data[0]['doc_type']=t
                                    final_passed_payment.append(flag_data[0])                   
                        if t=="Pharmacy":
                            if doc_dict[t]:
                                for j in doc_dict[t]:
                                    flag_data=frappe.get_all(t,{"name":j},pharmacy_field_list)
                                    flag_data[0]['doc_type']=t
                                    final_passed_payment.append(flag_data[0])
                        if t=="Patient Refund":
                            if doc_dict[t]:
                                for j in doc_dict[t]:
                                    flag_data=frappe.get_all(t,{"name":j},patient_refund_field_list)
                                    flag_data[0]['doc_type']=t
                                    final_passed_payment.append(flag_data[0])
            # print(emp_wf['name'])
            # print(final_passed_payment)
            ####################################### end Payment status from batch payment
            ########################## Batch payment Inward Letter
            states_list=[]
            payment_inward_letter=[]
            for aw in active_workflow:
                if aw['document_type']=='Batch Payment Process':
                    workflow_document_state=frappe.get_all("Workflow Document State",[["parent","=",aw['name']],["allow_edit","=",emp_wf['role']]],
                                        ['name','parent','allow_edit','state'])
                    for t in workflow_document_state:
                        if t['state']!="Draft" and t['state']!="Verify and Save" and t['state']!="Rejected and Transfer" \
                                and t['state']!="Payment Done" and t['state']!="Cancelled":
                            t['document_type']=aw['document_type']
                            states_list.append(t)
            for t in states_list:
                data=frappe.get_all("Batch Payment Process",{"workflow_state":t['state']},batch_payment_process)
                for j in data:
                    j['document_type']=t['document_type']
                    payment_inward_letter.append(j)                          
            # print(payment_inward_letter)
            ########################################## Master Record preparation   \
            today_date=utils.nowdate()
            start_time_date="%s 00:00:00"%today_date
            end_time_date="%s 23:59:59"%today_date                                         
            data=frappe.get_all("Authorized Signature",{"emp_id":emp_name,'parenttype':'Batch Payment Process',"date_of_approval":['between', [start_time_date,end_time_date]]},
                                ['name','parent','parenttype',"approval_status","date_of_approval"])
            payment_section=[]
            if data:
                doc_head=[]
                for t in data:
                    doc_head.append(t['parenttype'])
                doc_head=list(set(doc_head))

                doc_dict={} 
                for t in doc_head:
                    doc_dict[t]=[]
                #################################################### Payment section
                for t in data:
                    if t["approval_status"]=="Payment Done":
                        # print(t['parenttype'])
                        doc_date=frappe.get_all(t['parenttype'],{"name":t['parent']},batch_payment_process)
                        doc_date[0]["doc_type"]=t['parenttype']
                        payment_section.append(doc_date[0])
            # print(emp_wf['name'])
            # print(payment_section)
            #################################################### end of Payment section
            ############################################ Cancelation of all Doc record
            today_date=utils.nowdate()
            start_time_date="%s 00:00:00"%today_date
            end_time_date="%s 23:59:59"%today_date
            data=frappe.get_all("Authorized Signature",{"approval_status":"Cancelled","date_of_approval":['between', [start_time_date,end_time_date]]},
                                    ['name','parent','parenttype',"approval_status","date_of_approval"])
            cancelation_section=[]
            if data:                        
                doc_head=[]
                for t in data:
                    doc_head.append(t['parenttype'])
                doc_head=list(set(doc_head))

                doc_dict={} 
                for t in doc_head:
                    doc_dict[t]=[]

                
                for t in data:
                    flag_data=frappe.get_all("Authorized Signature",{"parent":t['parent'],"emp_id":emp_wf['name']},['name'])
                    if flag_data:
                        doc_dict[t['parenttype']].append(t['parent'])

                for t in doc_dict:
                    doc_dict[t]=list(set(doc_dict[t]))

                for t in doc_dict:
                    if t=='PO Consumable' or t=='PO Material Management' \
                        or t=='Non PO Contract' or t=="Non PO Non Contract" or t=="Non PO Non Contract":
                        if doc_dict[t]:
                            for j in doc_dict[t]:
                                flag_data=frappe.get_all(t,{"name":j},genral_field_list)
                                flag_data[0]['doc_type']=t
                                cancelation_section.append(flag_data[0])                            
                    if t=='PO Consignment':
                        if doc_dict[t]:
                            for j in doc_dict[t]:
                                flag_data=frappe.get_all(t,{"name":j},po_consignment_field_list)
                                flag_data[0]['doc_type']=t
                                cancelation_section.append(flag_data[0])                   
                    if t=="Pharmacy":
                        if doc_dict[t]:
                            for j in doc_dict[t]:
                                flag_data=frappe.get_all(t,{"name":j},pharmacy_field_list)
                                flag_data[0]['doc_type']=t
                                cancelation_section.append(flag_data[0])
                    if t=="Patient Refund":
                        if doc_dict[t]:
                            for j in doc_dict[t]:
                                flag_data=frappe.get_all(t,{"name":j},patient_refund_field_list)
                                flag_data[0]['doc_type']=t
                                cancelation_section.append(flag_data[0])
                    if t=="Batch Payment Process":
                        if doc_dict[t]:
                            for j in doc_dict[t]:
                                flag_data=frappe.get_all(t,{"name":j},batch_payment_process)
                                flag_data[0]['doc_type']=t
                                cancelation_section.append(flag_data[0])                  
            ############################################ end Cancelation of all Doc record
            report_scheduler(emp_wf,inward_letter,final_passed_for_payment,payment_section,
                            cancelation_section,final_passed_payment,field)                                      

                
def reject_transfer():
    # bench --site erp.soulunileaders.com execute ims.tasks.reject_transfer
    doctype_name=['PO Consumable',"PO Consignment","PO Material Management","Pharmacy","Non PO Contract","Non PO Non Contract",
                "Patient Refund","Batch Payment Process"]

    genral_field_list= ['name','note_sheet_no','posting_date','item_of_purchaseexpense','supplier_code','name_of_supplier','total_amount_in_rs',
                        'tds_amount_to_be_deducted_in_rs','advance_amount_already_paid_in_rs','net_final_amount_to_be_paid_in_rs','document_status']
    po_consignment_field_list=['name','note_sheet_no','posting_date','item_of_purchaseexpense','total_hospital_margin_amount','supplier_code','name_of_supplier',
                                            'to_pay_total','total_amount_in_rs','less_credit_note_amount_in_rs','net_final_amount_to_be_paid_in_rs','document_status']                                      
    pharmacy_field_list=['name','note_sheet_no','posting_date','item_of_purchaseexpense','supplier_code','name_of_supplier','total_amount'
                                    ,'advance_amount_already_paid_in_rs','net_final_amount_to_be_paid_in_rs','document_status']
    patient_refund_field_list=['name',"type_of_insurance","name_of_the_patient","ip__uhid_no","posting_date","total_bill","approval_of_tpa__insurance__corporate__ostf",
                                    "amount_deposited_by_patient","net_refundable_in_figures",'document_status']
    batch_payment_process=['name',"date","document_status","account_reference_no","bank_ac_no","bank_name","bank_address","account_reference_no",
                                            "account_post_date","audit_reference_no","audit_posting_date","cheque_no","cheque_date","total_amount"]

    doctype_name_filed_map=[{"parent":'PO Consumable',"fieldname":genral_field_list},{"parent":"PO Consignment","fieldname":po_consignment_field_list},
                    {"parent":"PO Material Management","fieldname":genral_field_list},{"parent":"Pharmacy","fieldname":pharmacy_field_list}
                    ,{"parent":"Non PO Contract","fieldname":genral_field_list},{"parent":"Non PO Non Contract","fieldname":genral_field_list},
                {"parent":"Patient Refund","fieldname":patient_refund_field_list},{"parent":"Batch Payment Process","fieldname":batch_payment_process}]

    field=[]
    for t in doctype_name_filed_map:
        fieldname=t["fieldname"]
        for j in fieldname:
            dofield=frappe.get_all("DocField",filters=[["parent","=",t['parent']],["fieldname","=",j]],fields=["label","fieldname","parent"])
            if dofield:
                field.append(dofield[0])
    
    rejection_email=frappe.get_all("Authorized Signature",{"rejection_email_status":"Mail Not Send"},
                                ['name',"parent","emp_id",'parenttype','transfer_to','disapproval_check',
                                "rejection_email_status","approval_status","remarks"])

    # {'name': 406, 'parent': 'PO-CON-21/12/2022-00001', 'emp_id': 'EMP-00027', 'parenttype': 'PO Consignment'}
    # {'name': 406, 'parent': 'PO-CON-21/12/2022-00001', 'emp_id': 'EMP-00027', 'parenttype': 'PO Consignment', 'transfer_to': 1, 'disapproval_check': 1}
    # {'name': 407, 'parent': 'PO-CON-21/12/2022-00001', 'emp_id': 'EMP-00027', 'parenttype': 'PO Consignment', 'transfer_to': 0, 'disapproval_check': 1}

    for re in rejection_email:
        emp_date_workflow=frappe.get_all("Employee",[["name","=",re['emp_id']]],['name','role','full_name','employee_number','email','department'])
        approval_status=''
        remarks=''
        for t in rejection_email:
            if t['parent']==re['parent'] and t['transfer_to']==1 and t['disapproval_check']==1:
                approval_status=t['approval_status']
                remarks=t['remarks']

        list_data=[]
        if re['parenttype']=="PO Consumable":
            flag_data=frappe.get_all(re['parenttype'],{"name":re['parent']},genral_field_list)
            flag_data[0]['doc_type']=re['parenttype']
            flag_data[0]['approval_status']=approval_status
            flag_data[0]['remarks']=remarks
            list_data.append(flag_data[0])
        elif re['parenttype']=="PO Consignment":
            flag_data=frappe.get_all(re['parenttype'],{"name":re['parent']},po_consignment_field_list)
            flag_data[0]['doc_type']=re['parenttype']
            flag_data[0]['approval_status']=approval_status
            flag_data[0]['remarks']=remarks
            list_data.append(flag_data[0])
        elif re['parenttype']=="PO Material Management":
            flag_data=frappe.get_all(re['parenttype'],{"name":re['parent']},genral_field_list)
            flag_data[0]['doc_type']=re['parenttype']
            flag_data[0]['approval_status']=approval_status
            flag_data[0]['remarks']=remarks
            list_data.append(flag_data[0])
        elif re['parenttype']=="Pharmacy":
            flag_data=frappe.get_all(re['parenttype'],{"name":re['parent']},pharmacy_field_list)
            flag_data[0]['doc_type']=re['parenttype']
            flag_data[0]['approval_status']=approval_status
            flag_data[0]['remarks']=remarks
            list_data.append(flag_data[0])
        elif re['parenttype']=="Non PO Contract":
            flag_data=frappe.get_all(re['parenttype'],{"name":re['parent']},genral_field_list)
            flag_data[0]['doc_type']=re['parenttype']
            flag_data[0]['approval_status']=approval_status
            flag_data[0]['remarks']=remarks
            list_data.append(flag_data[0])
        elif re['parenttype']=="Non PO Non Contract":
            flag_data=frappe.get_all(re['parenttype'],{"name":re['parent']},genral_field_list)
            flag_data[0]['doc_type']=re['parenttype']
            flag_data[0]['approval_status']=approval_status
            flag_data[0]['remarks']=remarks
            list_data.append(flag_data[0])
        elif re['parenttype']=="Patient Refund":
            flag_data=frappe.get_all(re['parenttype'],{"name":re['parent']},patient_refund_field_list)
            flag_data[0]['doc_type']=re['parenttype']
            flag_data[0]['approval_status']=approval_status
            flag_data[0]['remarks']=remarks
            list_data.append(flag_data[0])   
        elif re['parenttype']=="Batch Payment Process":
            flag_data=frappe.get_all(re['parenttype'],{"name":re['parent']},batch_payment_process)
            flag_data[0]['doc_type']=re['parenttype']
            flag_data[0]['approval_status']=approval_status
            flag_data[0]['remarks']=remarks
            list_data.append(flag_data[0])   
        report_scheduler_reject_trasfer(emp_date_workflow,flag_data,field)

    for re in rejection_email:
        frappe.db.sql(""" update `tabAuthorized Signature` set rejection_email_status="Mail Send" where name="%s" """%(re['name']))
        frappe.db.commit()   


def is_what_percent_of(num_a, num_b):
    return (num_a / num_b) * 100

def notification_for_approval():
    # bench --site erp.soulunileaders.com execute ims.tasks.notification_for_approval
    doctype_name=['PO Consumable',"PO Consignment","PO Material Management","Pharmacy","Non PO Contract","Non PO Non Contract",
                "Patient Refund"]

    genral_field_list= ['name','note_sheet_no','posting_date','item_of_purchaseexpense','supplier_code','name_of_supplier','total_amount_in_rs',
                        'tds_amount_to_be_deducted_in_rs','advance_amount_already_paid_in_rs','net_final_amount_to_be_paid_in_rs','document_status',
                        'amount_clearance_period_in_days']
    po_consignment_field_list=['name','note_sheet_no','posting_date','item_of_purchaseexpense','total_hospital_margin_amount','supplier_code','name_of_supplier',
                                            'to_pay_total','total_amount_in_rs','less_credit_note_amount_in_rs','net_final_amount_to_be_paid_in_rs','document_status']                                      
    pharmacy_field_list=['name','note_sheet_no','posting_date','item_of_purchaseexpense','supplier_code','name_of_supplier','total_amount'
                                    ,'advance_amount_already_paid_in_rs','net_final_amount_to_be_paid_in_rs','document_status',
                                    'amount_clearance_period_in_days']
    patient_refund_field_list=['name',"type_of_insurance","name_of_the_patient","ip__uhid_no","posting_date","total_bill","approval_of_tpa__insurance__corporate__ostf",
                                    "amount_deposited_by_patient","net_refundable_in_figures",'document_status']
    batch_payment_process=['name',"date","document_status","account_reference_no","bank_ac_no","bank_name","bank_address","account_reference_no",
                                            "account_post_date","audit_reference_no","audit_posting_date","cheque_no","cheque_date","total_amount"]

    doctype_name_filed_map=[{"parent":'PO Consumable',"fieldname":genral_field_list},{"parent":"PO Consignment","fieldname":po_consignment_field_list},
                    {"parent":"PO Material Management","fieldname":genral_field_list},{"parent":"Pharmacy","fieldname":pharmacy_field_list}
                    ,{"parent":"Non PO Contract","fieldname":genral_field_list},{"parent":"Non PO Non Contract","fieldname":genral_field_list},
                {"parent":"Patient Refund","fieldname":patient_refund_field_list},{"parent":"Batch Payment Process","fieldname":batch_payment_process}]

    field=[]
    for t in doctype_name_filed_map:
        fieldname=t["fieldname"]
        for j in fieldname:
            dofield=frappe.get_all("DocField",filters=[["parent","=",t['parent']],["fieldname","=",j]],fields=["label","fieldname","parent"])
            if dofield:
                field.append(dofield[0])
    
    priority=[{"type_priority":"Urgent","percentage":20},{"type_priority":"Normal","percentage":100},
                {"type_priority":"High Priority","percentage":40},{"type_priority":"Low Priority","percentage":150}]
    ########################################### "priority" wise taking the record 
    list_notsheet_not_paid=[]
    for pro in priority:
        for doc in doctype_name:
            if doc!="Patient Refund":
                type_priority=pro['type_priority']
                percentage=pro['percentage']
                data=frappe.get_all(doc,[["priority","=",pro['type_priority']],["payment_status","!=","Payment successful"],
                                        ["workflow_state","!=","Cancelled"]],
                                        ['name','posting_date','amount_clearance_period_in_days','priority','workflow_state',
                                        "payment_status","document_status",'batch_payment_no'])                       
                for t in data:
                    if t['workflow_state']!="Draft" and t['workflow_state']!="Verify and Save":
                        no_days=(date.today()-t['posting_date']).days
                        
                        result = is_what_percent_of(no_days, t['amount_clearance_period_in_days'])

                        if pro['percentage']<=result:
                            t['parenttype']=doc
                            t['threshold_percentage']=percentage
                            t['present_threshold_percentage']=result
                            t['no_days_consumed']=no_days
                            list_notsheet_not_paid.append(t)                 
            else:
                type_priority="Urgent"
                no_days=7
                percentage=100
                data=frappe.get_all(doc,[["payment_status","!=","Payment successful"],
                                        ["workflow_state","!=","Cancelled"]],
                                        ['name','posting_date','workflow_state',"payment_status","document_status",'batch_payment_no'])                       
                for t in data:
                    if t['workflow_state']!="Draft" and t['workflow_state']!="Verify and Save":
                        no_days_consumed=(date.today()-t['posting_date']).days
                        result = is_what_percent_of(no_days_consumed,no_days)
                        mail_cut_of_days=t['posting_date']+ timedelta(days=no_days)
                        if mail_cut_of_days<=date.today():
                            t['amount_clearance_period_in_days']=no_days
                            t['priority']=type_priority
                            t['parenttype']=doc
                            t['no_days_consumed']=no_days_consumed
                            t['threshold_percentage']=percentage
                            t['present_threshold_percentage']=result
                            list_notsheet_not_paid.append(t)    
    ###########################################  end "priority" wise taking the record 
    #################################### Taking urgent emp record #####################
    list_doc=[]
    for t in list_notsheet_not_paid:
        list_doc.append(t['parenttype'])
    list_doc=list(set(list_doc)) 
    doc_dict={} 
    for t in list_doc:
        doc_dict[t]=[]

    for t in list_notsheet_not_paid:
        doc_dict[t['parenttype']].append(t['name'])

    for t in doc_dict:
        doc_dict[t]=list(set(doc_dict[t]))

    list_emp=[]
    for t in doc_dict:
        for j in doc_dict[t]:
            data=frappe.get_all("Authorized Signature",{"parent":j},['emp_id','approval_status','previous_status','parent','parenttype'])
            if data:
                for k in data:
                    if k['approval_status']!="Draft" and k['approval_status']!="Verify and Save":
                        list_emp.append({'emp_id':k['emp_id'],'parent':k['parent'],'parenttype':k['parenttype']})
 
    emp_list=[]
    for t in list_emp:
        emp_list.append(t['emp_id'])
    emp_list=list(set(emp_list))

    emp_dict={}

    for t in emp_list:
        emp_dict[t]=[]

    for t in list_emp:
        emp_dict[t['emp_id']].append(t)
           
    
    for list_of_dictionaries in emp_dict:
        new_list = []
        for dictionary in emp_dict[list_of_dictionaries]:
            if dictionary not in new_list:
                new_list.append(dictionary)
        emp_dict[list_of_dictionaries]=  new_list

    for emp in emp_dict:
        for t in emp_dict[emp]:
            for j in list_notsheet_not_paid:
                if t['parent']==j["name"]:
                    # {'name': 'PO- CONSGT-00001', 'posting_date': datetime.date(2022, 12, 8), 
                    # 'amount_clearance_period_in_days': 10, 'priority': 'Normal', 'workflow_state': 'Passed for Payment', 
                    # 'payment_status': None, 'document_status': 'Passed for Payment', 'batch_payment_no': None, 
                    # 'doc_type': 'PO Consignment', 'threshold_percentage': 100, 'present_threshold_percentage': 140.0, 'no_days_consumed': 14}
                    t['priority']=j['priority']
                    t['workflow_state']=j['workflow_state']
                    t['payment_status']=j['payment_status']
                    t['document_status']=j['document_status']
                    t['batch_payment_no']=j['batch_payment_no']
                    t['threshold_percentage']=j['threshold_percentage']
                    t['present_threshold_percentage']=j['present_threshold_percentage']
                    t['no_days_consumed']=j['no_days_consumed']
                    t['future_role']=""
                    break

    for t in emp_dict:
        new_list = []
        for j in emp_dict[t]:
            if j['priority']=="Urgent":
                new_list.append(j)
        emp_dict[t]=new_list
    # print(emp_dict) ##### Receiving "Urgent" mail form the Authorized Signature
    #################################### End Taking urgent emp record #####################
    #################################### Holding of Notesheet role #################################
    for t in list_notsheet_not_paid:
        role=""
        if t['payment_status']!="Payment successful":
            if t['workflow_state']=="Passed for Payment":
                work_flow_data=frappe.get_all("Workflow",{"document_type":"Batch Payment Process",'is_active':1},["name"])
                work_flow_data=frappe.get_all("Workflow Document State",{"parent":work_flow_data[0]['name']},["state","allow_edit"])
                
                if t['batch_payment_no']==None:
                    role=work_flow_data[0]["allow_edit"]
                else:
                    for j in work_flow_data:
                        if j['state']==t['workflow_state']:
                            role=j['allow_edit']        
            else:
                work_flow_data=frappe.get_all("Workflow",{"document_type":t['parenttype'],'is_active':1},["name"])
                work_flow_data=frappe.get_all("Workflow Document State",{"parent":work_flow_data[0]['name']},["state","allow_edit"])
                for j in work_flow_data:
                    if j['state']==t['workflow_state']:
                        role=j['allow_edit']
        t['future_role']=role  
    
    future_emp_list=[]
    for t in list_notsheet_not_paid:
        emp_data=frappe.get_all("Employee",{"role":t['future_role']},["name","role"])
        for j in emp_data:
            future_emp_list.append(j)

    future_emp_new_list = []

    for dictionary in future_emp_list:
        if dictionary not in future_emp_new_list:
            future_emp_new_list.append(dictionary)    
    
    for t in future_emp_new_list:
        if t['name'] in emp_dict.keys():
            list_table_emp_mail=emp_dict[t['name']]
            for j in list_notsheet_not_paid:
                if j['future_role']==t['role']:
                    j['future_role']=""
                    j['emp_id']=t['name']
                    list_table_emp_mail.append(j)
        else:
            emp_dict[t['name']]=[]
            list_table_emp_mail=emp_dict[t['name']]
            for j in list_notsheet_not_paid:
                if j['future_role']==t['role']:
                    j['future_role']=""
                    j['emp_id']=t['name']
                    list_table_emp_mail.append(j)


    for list_of_dictionaries in emp_dict:
        new_list = []
        for dictionary in emp_dict[list_of_dictionaries]:
            if dictionary not in new_list:
                new_list.append(dictionary)
        emp_dict[list_of_dictionaries]=  new_list
    #################################### end Holding of Notesheet role #################################
    #################################### Notesheet role of Batch payment not started for batch payment #################################
    list_for_batch_payment=[]
    for t in list_notsheet_not_paid:
        if t['batch_payment_no']==None:
            list_for_batch_payment.append(t)
    batch_payment_note_creator_name=frappe.get_all("Workflow",{"document_type":"Batch Payment Process","is_active":1},['name'])[0]['name']   
    emp_list_data=[]
    if batch_payment_note_creator_name:
        batch_payment_note_creator_role=frappe.get_all('Workflow Document State',{"parent":batch_payment_note_creator_name},['allow_edit'])[0]['allow_edit']
        emp_list_data=frappe.get_all("Employee",{"role":batch_payment_note_creator_role},['name','role'])    

    for t in emp_list_data:
        if t['name'] in emp_dict.keys():
            list_table_emp_mail=emp_dict[t['name']]
            for j in list_notsheet_not_paid:
                if j['future_role']==t['role']:
                    j['future_role']=""
                    j['emp_id']=t['name']
                    list_table_emp_mail.append(j)
        else:
            emp_dict[t['name']]=[]
            list_table_emp_mail=emp_dict[t['name']]
            for j in list_notsheet_not_paid:
                if j['future_role']==t['role']:
                    j['future_role']=""
                    j['emp_id']=t['name']
                    list_table_emp_mail.append(j)


    for list_of_dictionaries in emp_dict:
        new_list = []
        for dictionary in emp_dict[list_of_dictionaries]:
            if dictionary not in new_list:
                new_list.append(dictionary)
        emp_dict[list_of_dictionaries]=  new_list

    #################################### Notesheet role of Batch payment not started for batch payment #################################
    for t in emp_dict:
        emp_data=frappe.get_all("Employee",{"name":t,"enabled":1},['name','role','full_name','employee_number','email','department'])
        if emp_data:
            notsheet_data=emp_dict[t]
            list_data_for_mail=[]
            for k in notsheet_data:
                for j in doctype_name_filed_map:
                    if j['parent']==k['parenttype']:
                        try:
                            data=frappe.get_all(j['parent'],{"name":k['parent']},j['fieldname'])
                            for l in data:
                                l['doctype']=k['parenttype']
                                l['threshold_percentage']=k['threshold_percentage']
                                l['present_threshold_percentage']=k['present_threshold_percentage']
                                l['no_days_consumed']=k['no_days_consumed']
                                l['priority']=k['priority']
                                list_data_for_mail.append(l)
                        except:
                            data=frappe.get_all(j['parent'],{"name":k['name']},j['fieldname'])  
                            for l in data:
                                l['doctype']=k['parenttype']
                                l['threshold_percentage']=k['threshold_percentage']
                                l['present_threshold_percentage']=k['present_threshold_percentage']
                                l['no_days_consumed']=k['no_days_consumed']
                                l['priority']=k['priority']
                                list_data_for_mail.append(l)

            report_holder_notesheet(emp_data,list_data_for_mail,field)     


def mail_for_noteceater():
    # bench --site erp.soulunileaders.com execute ims.tasks.mail_for_noteceater

    doctype_name=['PO Consumable',"PO Consignment","PO Material Management","Pharmacy","Non PO Contract","Non PO Non Contract",
                "Patient Refund"]
    ################################### Invoice Data ####################
    invoice_recv=frappe.get_all("Invoice Receival",{"invoice_status":"Passed for Notesheet"})
    for t in invoice_recv:
        t['doc_type']="Invoice Receival"

    invoice_recv_emp=[]      
    for t in doctype_name:
        if t!="Patient Refund":
            data=frappe.get_all("Workflow",{"document_type":t,"is_active":1},['name'])
            data=frappe.get_all("Workflow Document State",{"parent":data[0]['name'],"state":"Verify and Save"},['allow_edit'])
            role=data[0]['allow_edit']
            emp=frappe.get_all("Employee",{"role":role,"enabled":1},['name','role','full_name','employee_number','email','department'])
            for j in emp:
                invoice_recv_emp.append(j)
    ################################### Invoice Data ####################
    ############################# Note sheet data ##############
    pass_for_payment_data=[]            
    for t in doctype_name:   
        data=[]         
        data=frappe.get_all(t,[["workflow_state","=","Passed for Payment"],["batch_payment_no","=",""],["batch_payment_no","!=","Cancelled"]],['name'])
        for j in data:
            j['doc_type']=t
            pass_for_payment_data.append(j)



    data=frappe.get_all("Workflow",{"document_type":"Batch Payment Process","is_active":1},['name'])
    data=frappe.get_all("Workflow Document State",{"parent":data[0]['name'],"state":"Verify and Save"},['allow_edit'])
    role=data[0]['allow_edit']
    pass_for_payment_emp=frappe.get_all("Employee",{"role":role,"enabled":1},['name','role','full_name','employee_number','email','department'])
    ##################################### end Note sheet data###########    
    genral_field_list= ['name','priority','note_sheet_no','posting_date','item_of_purchaseexpense','supplier_code','name_of_supplier','total_amount_in_rs',
                        'tds_amount_to_be_deducted_in_rs','advance_amount_already_paid_in_rs','net_final_amount_to_be_paid_in_rs','document_status',
                        'amount_clearance_period_in_days']
    po_consignment_field_list=['name','priority','note_sheet_no','posting_date','item_of_purchaseexpense','total_hospital_margin_amount','supplier_code','name_of_supplier',
                                            'to_pay_total','total_amount_in_rs','less_credit_note_amount_in_rs','net_final_amount_to_be_paid_in_rs','document_status']                                      
    pharmacy_field_list=['name','priority','note_sheet_no','posting_date','item_of_purchaseexpense','supplier_code','name_of_supplier','total_amount'
                                    ,'advance_amount_already_paid_in_rs','net_final_amount_to_be_paid_in_rs','document_status',
                                    'amount_clearance_period_in_days']
    patient_refund_field_list=['name',"type_of_insurance","name_of_the_patient","ip__uhid_no","posting_date","total_bill","approval_of_tpa__insurance__corporate__ostf",
                                    "amount_deposited_by_patient","net_refundable_in_figures",'document_status']
    batch_payment_process=['name',"date","document_status","account_reference_no","bank_ac_no","bank_name","bank_address","account_reference_no",
                                            "account_post_date","audit_reference_no","audit_posting_date","cheque_no","cheque_date","total_amount"]
    invoice_data_fied=["name","company","type_of_invoice","invoice_no","invoice_date","type_of_supplier","supplier_code","supplier_name",
                        "remarks_if_any","posting_date","invoice_status","note_sheet_status","note_no","type_of_note_sheet","batch_payment_no",
                        "payment_status"]                                        

    doctype_name_filed_map=[{"parent":'PO Consumable',"fieldname":genral_field_list},{"parent":"PO Consignment","fieldname":po_consignment_field_list},
                    {"parent":"PO Material Management","fieldname":genral_field_list},{"parent":"Pharmacy","fieldname":pharmacy_field_list}
                    ,{"parent":"Non PO Contract","fieldname":genral_field_list},{"parent":"Non PO Non Contract","fieldname":genral_field_list},
                {"parent":"Patient Refund","fieldname":patient_refund_field_list},{"parent":"Batch Payment Process","fieldname":batch_payment_process}
                ,{"parent":"Invoice Receival","fieldname":invoice_data_fied}]

    field=[]
    for t in doctype_name_filed_map:
        fieldname=t["fieldname"]
        for j in fieldname:
            dofield=frappe.get_all("DocField",filters=[["parent","=",t['parent']],["fieldname","=",j]],fields=["label","fieldname","parent"])
            if dofield:
                field.append(dofield[0])
    ########################################## Field            
    emp_final_list={}
    for t in invoice_recv_emp:
        if t['name'] in emp_final_list.keys():
            pass
        else:
            emp_final_list[t['name']]=[]    
    for t in emp_final_list:
        for j in invoice_recv:
            emp_final_list[t].append(j)


    for t in pass_for_payment_emp:
        if t['name'] in emp_final_list.keys():
            for j in pass_for_payment_data:
                emp_final_list[t['name']].append(j)
        else:
            emp_final_list[t['name']]=[]          
            for j in pass_for_payment_data:
                emp_final_list[t['name']].append(j)               

    for list_of_dictionaries in emp_final_list:
        new_list = []
        for dictionary in emp_final_list[list_of_dictionaries]:
            if dictionary not in new_list:
                new_list.append(dictionary)
        emp_final_list[list_of_dictionaries]=  new_list
    # print(emp_final_list) 
    for t in emp_final_list:
        emp_data=frappe.get_all("Employee",{"name":t,"enabled":1},['name','role','full_name','employee_number','email','department'])
        if emp_data:
            notsheet_data=emp_final_list[t]
            list_data_for_mail=[]
            for k in notsheet_data:
                for j in doctype_name_filed_map:
                    if j['parent']==k['doc_type']:
                        try:
                            data=frappe.get_all(j['parent'],{"name":k['parent']},j['fieldname'])
                            for l in data:
                                l['doc_type']=k['doc_type']
                                list_data_for_mail.append(l)
                        except:
                            data=frappe.get_all(j['parent'],{"name":k['name']},j['fieldname'])  
                            for l in data:
                                l['doc_type']=k['doc_type']
                                list_data_for_mail.append(l) 
            notesheet_reminder_mail(field,emp_data,list_data_for_mail)
            


                        


                                

                           



        
        
