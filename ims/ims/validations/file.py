import frappe
import os


def validate(doc,method):
    file_size(doc)


def file_size(doc):
    attached_to_doctype=doc.attached_to_doctype
    file_name = doc.file_url.split('/')[-1]
    public_file_path = frappe.get_site_path('public', 'files', file_name)
    url=public_file_path
    ext=os.path.splitext(url)
    extstr=ext[1]
    ext_list=[".pdf"]
    doctype_list=["PO Consumable","PO Material Management","PO Consignment","Pharmacy","Non PO Non Contract","Non PO Contract","Patient Refund"]

    for i in doctype_list:
        if i==attached_to_doctype:
            for t in ext_list:
                if t==extstr:
                    pass
                else:
                    return frappe.throw("Attachment is not a PDF File!! Please try again.")
        else:
            pass