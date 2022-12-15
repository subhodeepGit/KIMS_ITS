import frappe

def cron():
    print("\n\n\n\n")
    # bench --site erp.soulunileaders.com execute ims.tasks.cron
    # doctype_name=['PO Consumable',"PO Consignment","PO Material Management","Pharmacy","Non PO Contract","Non PO Non Contract"
    #             "Patient Refund","Batch Payment Process"]
    genral_field_list= ['name','note_sheet_no','posting_date','item_of_purchaseexpense','supplier_code','name_of_supplier','total_amount_in_rs',
                        'tds_amount_to_be_deducted_in_rs','advance_amount_already_paid_in_rs','net_final_amount_to_be_paid_in_rs','document_status']
    po_consignment_field_list=['name','note_sheet_no','posting_date','item_of_purchaseexpense','total_hospital_margin_amount','supplier_code','name_of_supplier',
                                            'to_pay_total','total_amount_in_rs','less_credit_note_amount_in_rs','net_final_amount_to_be_paid_in_rs','document_status'] 
    pharmacy_field_list=['name','note_sheet_no','posting_date','item_of_purchaseexpense','supplier_code','name_of_supplier','total_amount'
                                    ,'advance_amount_already_paid_in_rs','net_final_amount_to_be_paid_in_rs','document_status']
    patient_refund_field_list=['name',"type_of_insurance","name_of_the_patient","ip__uhid_no","posting_date","total_bill","approval_of_tpa__insurance__corporate__ostf",
                                    "amount_deposited_by_patient","net_refundable_in_figures",'document_status']                                

    emp_date_workflow=frappe.get_all("Employee",[["enabled","=",1],["role","!=","Null"]],
                                        ['name','role','full_name','employee_number','email','department'])
    active_workflow=frappe.get_all("Workflow",{"is_active":1},['name','document_type'])

    for emp_wf in emp_date_workflow:
        emp_name=emp_wf['name']
        if emp_wf['role']!=None and emp_wf['role']!="":
            states_list=[]
            ################################################ Inward Letter
            inward_letter=[]
            for aw in active_workflow:
                workflow_document_state=frappe.get_all("Workflow Document State",[["parent","=",aw],["allow_edit","=",emp_wf['role']]],
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
            # print("\n\n")
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
                            final_passed_for_payment.append(flag_data[0])                            
                if t=='PO Consignment':
                    if pass_for_payment_section[t]:
                        for j in pass_for_payment_section[t]:
                            flag_data=frappe.get_all(t,{"name":j},po_consignment_field_list)
                            final_passed_for_payment.append(flag_data[0])                   
                if t=="Pharmacy":
                    if pass_for_payment_section[t]:
                        for j in pass_for_payment_section[t]:
                            flag_data=frappe.get_all(t,{"name":j},pharmacy_field_list)
                            final_passed_for_payment.append(flag_data[0])
                if t=="Patient Refund":
                    if pass_for_payment_section[t]:
                        for j in pass_for_payment_section[t]:
                            flag_data=frappe.get_all(t,{"name":j},patient_refund_field_list)
                            final_passed_for_payment.append(flag_data[0])
            # print(emp_wf['name'])
            # print(final_passed_for_payment)
            ####################################### End Pass for Payment section   
            ####################################### Payment status from batch payment 
            # (Logic:- which of the invoice emp has approved and batch payment is completed with spacification of payment status of the success or failure note sheet spacific as on sys date )
            import datetime
            today_day=datetime.datetime(2022, 12, 8, 0, 0)
            for t in data:
                if t["approval_status"]=="Payment Done":
                    doc_date=frappe.get_all(t['parenttype'],{"name":t['parent']},['name','document_status'])
                    print(doc_date)
                    pass                      

                           



        
        
