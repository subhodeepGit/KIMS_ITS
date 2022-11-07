// Copyright (c) 2022, SOUL and contributors
// For license information, please see license.txt

frappe.ui.form.on('PO Consignment', {
	// refresh: function(frm) {

	// }
});
frappe.ui.form.on('Credit Note and PO', {	//Child table Name
	invoice_amount:function(frm, cdt, cdn){	//Child table field Name where you data enter
	var d = locals[cdt][cdn];
	var total = 0;
	let a= parseInt(total)
	frm.doc.details_of_invoices_credit_note_and_po.forEach(function(d)  { a = a+ d.invoice_amount; }); //Child table name and field name
	frm.set_value("total_amount_in_rs", a);			// Parent field name where calculation going to fetch
	refresh_field("total_amount_in_rs");
	frm.set_value("net_final_amount_to_be_paid_in_rs",a) // Parent field name where calculation going to fetch
	refresh_field("net_final_amount_to_be_paid_in_rs");
  },
  // When field is deleted from child table on that time calculation going to happend to the accordingly
  details_of_invoices_credit_note_and_po_remove:function(frm, cdt, cdn){ //Child table name
	var d = locals[cdt][cdn];
	var total = 0;
	let a= parseInt(total)
	frm.doc.details_of_invoices_credit_note_and_po.forEach(function(d) { a += d.invoice_amount; });
	frm.set_value("total_amount_in_rs", a);
	refresh_field("total_amount_in_rs");
	frm.set_value("net_final_amount_to_be_paid_in_rs",a)
	refresh_field("net_final_amount_to_be_paid_in_rs");
	}
});

frappe.ui.form.on('PO Consignment', {
	total_amount_in_rs: function(frm) {
		frm.trigger("cal");
		},
		cal(frm){
			var net_amount = 0;
			net_amount = cur_frm.doc.total_amount_in_rs - cur_frm.doc.less_credit_note_amount_in_rs
			frm.set_value("net_final_amount_to_be_paid_in_rs",net_amount)
			refresh_field("net_final_amount_to_be_paid_in_rs");
		}
	});

frappe.ui.form.on('PO Consignment',"less_credit_note_amount_in_rs", function(frm) {
	var net_amount = 0;
	net_amount = cur_frm.doc.total_amount_in_rs - cur_frm.doc.less_credit_note_amount_in_rs
	frm.set_value("net_final_amount_to_be_paid_in_rs",net_amount)
	refresh_field("net_final_amount_to_be_paid_in_rs");
});

frappe.ui.form.on("PO Consignment", {
	onload:function(frm){
		//cannot able to add rows
		frm.set_df_property("authorized_signature", "cannot_add_rows", true);
		//cannot able to delete rows
		frm.set_df_property("authorized_signature", "cannot_delete_rows", true);
	}
});
