import frappe
from frappe import utils
from ims.ims.notification.custom_notification import report_scheduler,report_scheduler_reject_trasfer



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
            # print(cancelation_section)                    
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
            




    
            


                        


                                

                           



        
        
