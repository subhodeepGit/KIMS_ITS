// Copyright (c) 2022, SOUL and contributors
// For license information, please see license.txt

// frappe.ui.form.on('Batch Payment Process', {
// 	onload: function(frm) {
// 		var df1 = frappe.meta.get_docfield("Authorized Signature","transfer_to", cur_frm.doc.name);
// 		df1.hidden = 1;
// 		var df1 = frappe.meta.get_docfield("Authorized Signature","disapproval_check", cur_frm.doc.name);
// 		df1.hidden = 1;
// 		var df1 = frappe.meta.get_docfield("Authorized Signature","remarks", cur_frm.doc.name);
// 		df1.hidden = 1;
// 		}
// });
frappe.ui.form.on("Batch Payment Process", {
	onload:function(frm){
		//cannot able to add rows
		frm.set_df_property("approval_hierarchy", "cannot_add_rows", true);
		//cannot able to delete rows
		frm.set_df_property("approval_hierarchy", "cannot_delete_rows", true);
	}
});
frappe.ui.form.on("Batch Payment Process", {
	onload:function(frm){
		if(frm.doc.workflow_state!="Draft" && frm.doc.workflow_state!="Verify and Save"){
			frm.set_df_property("table_26", "cannot_add_rows", true);
			frm.set_df_property("table_26", "cannot_delete_rows", true);
			frm.set_df_property("vendor_wise_payment_details", "cannot_add_rows", true);
			frm.set_df_property("vendor_wise_payment_details", "cannot_delete_rows", true);
			// frm.set_df_property("company",'read_only', 0)
	}
}
});

frappe.ui.form.on("Batch Payment Process", {
	//  open of pop up 
	get_outstanding_amount: function(frm) {
		const today = frappe.datetime.get_today();
		const fields = [
			{fieldtype:"Section Break", label: __("Posting Date")},
			{fieldtype:"Date", label: __("From Date"),
				fieldname:"from_posting_date", default:frappe.datetime.add_days(today, -30)},
			{fieldtype:"Column Break"},
			{fieldtype:"Date", label: __("To Date"), fieldname:"to_posting_date", default:today},	
			{fieldtype:"Section Break", label: __("Type of Invoice")},
			{fieldtype:"Select", label: __("Invoice"),
				fieldname:"invoice", options: ["","PO Consumable","PO Consignment","PO Material Management","Pharmacy","Non PO Contract","Non PO Non Contract"]},
			{fieldtype:"Section Break", label: __("Type of Invoice")},
			{fieldtype:"Select", label: __("Priority"),
				fieldname:"priority", options: ["","Urgent","Normal","High Priority","Low Priority"]},
			{fieldtype:"Section Break", label: __("Vendor")},
			{fieldtype:"Link", label: __("Vendor"),fieldname:"vendor", options: "Supplier",
				default:frm.doc.supplier_code,
				"get_query": function() {
					return {
						"filters": {"company": frm.doc.company}
					}
				}
			},
			{fieldtype:"Section Break", label: __("Outstanding Amount")},
			{fieldtype:"Float", label: __("Greater Than Amount"),
				fieldname:"outstanding_amt_greater_than", default: 0},
			{fieldtype:"Column Break"},
			{fieldtype:"Float", label: __("Less Than Amount"), fieldname:"outstanding_amt_less_than"},
			{fieldtype:"Section Break"},
		];
		frappe.prompt(fields, function(filters){
			frappe.flags.allocate_payment_amount = true;
			frm.events.validate_filters_data(frm, filters);
			frm.doc.vendor = filters.supplier_code;
			frm.events.get_outstanding_documents(frm, filters);
			// frm.events.get_child_data(frm,filters);
		}, __("Filters"), __("Get Outstanding Documents"));
	},

	validate_filters_data: function(frm, filters) {
		const fields = {
			'Posting Date': ['from_posting_date', 'to_posting_date'],
			'Advance Amount': ['from_posting_date', 'to_posting_date'],
		};

		for (let key in fields) {
			let from_field = fields[key][0];
			let to_field = fields[key][1];

			if (filters[from_field] && !filters[to_field]) {
				frappe.throw(
					__("Error: {0} is mandatory field", [to_field.replace(/_/g, " ")])
				);
			} else if (filters[from_field] && filters[from_field] > filters[to_field]) {
				frappe.throw(
					__("{0}: {1} must be less than {2}", [key, from_field.replace(/_/g, " "), to_field.replace(/_/g, " ")])
				);
			}
		}
	},
	get_outstanding_documents: function(frm, filters) {
		frm.clear_table("table_26");
		var args={
			"company": frm.doc.company,
			"posting_date": frm.doc.posting_date,
			"priority": frm.doc.priority,
			"vendor": frm.doc.supplier_code,
		}

		for (let key in filters) {
			args[key] = filters[key];
		}

		return frappe.call({
			method: "ims.ims.doctype.batch_payment_process.batch_payment_process.get_outstanding_amount",
			args:{
				args:args
			},
			
			
			callback: function(r) {
				if(r.message){
					frappe.model.clear_table(frm.doc, 'table_26');
					(r.message).forEach(element => {
						var c = frm.add_child("table_26")
						c.vendor_name=element.name_of_supplier
						c.vendor_code=element.supplier_code
						c.document_no=element.document_number
						c.document_date=element.document_date
						c.ifsc_code=element.ifsc_code
						c.ac_no=element.bank_ac_no
						c.amount=element.net_final_amount_to_be_paid_in_rs
						c.amount1=element.net_final_amount_to_be_paid_in_rs
						c.ac_holder_name=element.account_holder_name
						c.bank_name=element.bank_name
						c.branch=element.bank_address
						c.invoice_tracking_number=element.name
						c.approve=element.workflow_state
					});
				} 
				frm.refresh();
				frm.refresh_field("table_26")
			}
		});
	},
	get_child_data: function(frm, filters) {
		frm.clear_table("vendor_wise_payment_details");
		var args={
			"company": frm.doc.company,
			"posting_date": frm.doc.posting_date,
			"priority": frm.doc.priority,
			"vendor": frm.doc.supplier_code,
		}

		for (let key in filters) {
			args[key] = filters[key];
		}

		return frappe.call({
			method: "ims.ims.doctype.batch_payment_process.batch_payment_process.merge_same_vendor",
			args:{
				args:args
			},
			
			
			callback: function(r) {
				if(r.message){
					frappe.model.clear_table(frm.doc, 'vendor_wise_payment_details');
					(r.message).forEach(element => {
						var c = frm.add_child("vendor_wise_payment_details")
						c.ifsc_code=element.ifsc_code
						c.ac_no=element.ac_no
						c.amount=element.amount
						c.ac_holder_name=element.ac_holder_name
						c.bank_name=element.bank_name
						c.branch=element.branch
						c.vendor_name=element.name_of_supplier
						c.vendor_code=element.supplier_code
					});
				} 
				frm.refresh();
				frm.refresh_field("vendor_wise_payment_details")
			}
		});
	}
});
