import frappe

def cron():
    print("\n\n\n\n")
    print("In scheduler")
    # bench --site erp.soulunileaders.com execute ims.tasks.cron
    doctype_name=['PO Consumable',"PO Consignment","PO Material Management","Pharmacy","Non PO Contract","Non PO Non Contract"
                "Patient Refund","Batch Payment Process"]
    for doc in doctype_name:
        print(doc)
        
