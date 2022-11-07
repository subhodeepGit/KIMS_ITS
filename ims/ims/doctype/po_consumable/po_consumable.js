<<<<<<< HEAD
=======
// Copyright (c) 2022, SOUL and contributors
// For license information, please see license.txt

// Child table Calculation
frappe.ui.form.on('Details of Invoices and PO', {	//Child table Name
	invoices_amountin_rs:function(frm, cdt, cdn){	//Child table field Name where you data enter
	var d = locals[cdt][cdn];
	var total = 0;
	let a= parseInt(total)
	frm.doc.details_of_invoices_and_po.forEach(function(d)  { a = a+ d.invoices_amountin_rs; }); //Child table name and field name
	frm.set_value("total_amount_in_rs", a);			// Parent field name where calculation going to fetch
	refresh_field("total_amount_in_rs");
	frm.set_value("net_final_amount_to_be_paid_in_rs",a) // Parent field name where calculation going to fetch
	refresh_field("net_final_amount_to_be_paid_in_rs");
  },
  // When field is deleted from child table on that time calculation going to happend to the accordingly
  details_of_invoices_and_po_remove:function(frm, cdt, cdn){ //Child table name
	var d = locals[cdt][cdn];
	var total = 0;
	let a= parseInt(total)
	frm.doc.details_of_invoices_and_po.forEach(function(d) { a += d.invoices_amountin_rs; });
	frm.set_value("total_amount_in_rs", a);
	refresh_field("total_amount_in_rs");
	frm.set_value("net_final_amount_to_be_paid_in_rs",a)
	refresh_field("net_final_amount_to_be_paid_in_rs");
	}
});

// Calculation
frappe.ui.form.on('PO Consumable',"advance_amount_already_paid_in_rs", function(frm) {
	var net_amount = 0;
	net_amount = cur_frm.doc.total_amount_in_rs - cur_frm.doc.tds_amount_to_be_deducted_in_rs - cur_frm.doc.advance_amount_already_paid_in_rs
	frm.set_value("net_final_amount_to_be_paid_in_rs",net_amount)
	refresh_field("net_final_amount_to_be_paid_in_rs");
});
frappe.ui.form.on('PO Consumable',"tds_amount_to_be_deducted_in_rs", function(frm) {
	var net_amount = 0;
	net_amount = cur_frm.doc.total_amount_in_rs - cur_frm.doc.advance_amount_already_paid_in_rs - cur_frm.doc.tds_amount_to_be_deducted_in_rs
	frm.set_value("net_final_amount_to_be_paid_in_rs",net_amount)
	refresh_field("net_final_amount_to_be_paid_in_rs");
});
frappe.ui.form.on('PO Consumable',"net_final_amount_to_be_paid_in_rs", function(frm) {
	var net_amount = 0;
	net_amount = cur_frm.doc.total_amount_in_rs - cur_frm.doc.tds_amount_to_be_deducted_in_rs - cur_frm.doc.advance_amount_already_paid_in_rs
	frm.set_value("net_final_amount_to_be_paid_in_rs",net_amount)
	refresh_field("net_final_amount_to_be_paid_in_rs");
});
frappe.ui.form.on('PO Consumable',"net_final_amount_to_be_paid_in_rs", function(frm) {
	var net_amount = 0;
	net_amount = cur_frm.doc.total_amount_in_rs - cur_frm.doc.advance_amount_already_paid_in_rs - cur_frm.doc.tds_amount_to_be_deducted_in_rs
	frm.set_value("net_final_amount_to_be_paid_in_rs",net_amount)
	refresh_field("net_final_amount_to_be_paid_in_rs");
});
frappe.ui.form.on('PO Consumable', {
	total_amount_in_rs: function(frm) {
	var net_amount = 0;
	net_amount = cur_frm.doc.total_amount_in_rs - cur_frm.doc.advance_amount_already_paid_in_rs - cur_frm.doc.tds_amount_to_be_deducted_in_rs
	frm.set_value("net_final_amount_to_be_paid_in_rs",net_amount)
	refresh_field("net_final_amount_to_be_paid_in_rs");
	}
});

// Child table field Mandatory when workflow state in draft
frappe.ui.form.on('PO Consumable', {
	before_load: function(frm) {
		frm.trigger("mandatory_field");
		},
		mandatory_field(frm){
			if(frm.doc.workflow_state=="Draft"){
				frm.set_value("document_status","Invoice in Draft State")
				refresh_field("document_status");
				var df1 = frappe.meta.get_docfield("Details of Invoices and PO","po_attachment", cur_frm.doc.name);
				df1.reqd = 1;
			}
		},
		before_save: function(frm) {
			frm.trigger("mandatory_field");
		},
});

frappe.ui.form.on("PO Consumable", {
	onload:function(frm){
		//cannot able to add rows
		frm.set_df_property("authorized_signature", "cannot_add_rows", true);
		//cannot able to delete rows
		frm.set_df_property("authorized_signature", "cannot_delete_rows", true);
	}
});

// frappe.ui.form.on('PO Consumable', {
// 	refresh: function(frm) {
// 		if(frm.doc.workflow_state=="Approved by Director"){
// 			frm.set_df_property('audit_ref_no', 'reqd', 1)
// 		}
// 	}
// });
// frappe.ui.form.on('PO Consumable', {
// 	refresh: function(frm) {
// 		// $('.primary-action').prop('hidden', true); //hide save button
// 		$('.btn-primary').hide(); //hide all button
// 		}
// });
>>>>>>> 18061d6b6d39e33d217b4a78a12da4db25bf152a
