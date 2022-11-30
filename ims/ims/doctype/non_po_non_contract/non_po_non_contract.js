// Copyright (c) 2022, SOUL and contributors
// For license information, please see license.txt

// frappe.ui.form.on('Non PO Non Contract', {
// 	// refresh: function(frm) {

// 	// }
// });
frappe.ui.form.on('Details Enclosed Bills', {	
	invoice_amount:function(frm, cdt, cdn){	
	var d = locals[cdt][cdn];
	var total = 0;
	let a= parseInt(total)
	frm.doc.details_of_enclosed_bills.forEach(function(d)  { a = a+ d.invoice_amount; }); 
	frm.set_value("total_amount_in_rs", a);			
	refresh_field("total_amount_in_rs");
	frm.set_value("net_final_amount_to_be_paid_in_rs",a) 
	refresh_field("net_final_amount_to_be_paid_in_rs");
  },
  details_of_enclosed_bills_remove:function(frm, cdt, cdn){ 
	var d = locals[cdt][cdn];
	var total = 0;
	let a= parseInt(total)
	frm.doc.details_of_enclosed_bills.forEach(function(d) { a += d.invoice_amount; });
	frm.set_value("total_amount_in_rs", a);
	refresh_field("total_amount_in_rs");
	frm.set_value("net_final_amount_to_be_paid_in_rs",a)
	refresh_field("net_final_amount_to_be_paid_in_rs");
	}
});

frappe.ui.form.on('Non PO Non Contract',"advance_amount_already_paid_in_rs", function(frm) {
	var net_amount = 0;
	net_amount = cur_frm.doc.total_amount_in_rs - cur_frm.doc.tds_amount_to_be_deducted_in_rs - cur_frm.doc.advance_amount_already_paid_in_rs
	frm.set_value("net_final_amount_to_be_paid_in_rs",net_amount)
	refresh_field("net_final_amount_to_be_paid_in_rs");
});
frappe.ui.form.on('Non PO Non Contract',"tds_amount_to_be_deducted_in_rs", function(frm) {
	var net_amount = 0;
	net_amount = cur_frm.doc.total_amount_in_rs - cur_frm.doc.advance_amount_already_paid_in_rs - cur_frm.doc.tds_amount_to_be_deducted_in_rs
	frm.set_value("net_final_amount_to_be_paid_in_rs",net_amount)
	refresh_field("net_final_amount_to_be_paid_in_rs");
});
frappe.ui.form.on('Non PO Non Contract',"net_final_amount_to_be_paid_in_rs", function(frm) {
	var net_amount = 0;
	net_amount = cur_frm.doc.total_amount_in_rs - cur_frm.doc.tds_amount_to_be_deducted_in_rs - cur_frm.doc.advance_amount_already_paid_in_rs
	frm.set_value("net_final_amount_to_be_paid_in_rs",net_amount)
	refresh_field("net_final_amount_to_be_paid_in_rs");
});
frappe.ui.form.on('Non PO Non Contract',"net_final_amount_to_be_paid_in_rs", function(frm) {
	var net_amount = 0;
	net_amount = cur_frm.doc.total_amount_in_rs - cur_frm.doc.advance_amount_already_paid_in_rs - cur_frm.doc.tds_amount_to_be_deducted_in_rs
	frm.set_value("net_final_amount_to_be_paid_in_rs",net_amount)
	refresh_field("net_final_amount_to_be_paid_in_rs");
});
frappe.ui.form.on('Non PO Non Contract', {
	total_amount_in_rs: function(frm) {
	var net_amount = 0;
	net_amount = cur_frm.doc.total_amount_in_rs - cur_frm.doc.advance_amount_already_paid_in_rs - cur_frm.doc.tds_amount_to_be_deducted_in_rs
	frm.set_value("net_final_amount_to_be_paid_in_rs",net_amount)
	refresh_field("net_final_amount_to_be_paid_in_rs");
	}
});

frappe.ui.form.on("Non PO Non Contract", {
	onload:function(frm){
		//cannot able to add rows
		frm.set_df_property("authorized_signature", "cannot_add_rows", true);
		//cannot able to delete rows
		frm.set_df_property("authorized_signature", "cannot_delete_rows", true);
}
});
frappe.ui.form.on("Non PO Non Contract", {
	onload:function(frm){
	if (frm.doc.type_of_supplier==""){
		frm.set_df_property("employee", "hidden", 1);
		frm.set_df_property("supplier_code", "hidden", 1);
	}
}
});
frappe.ui.form.on("Non PO Non Contract", {
	type_of_supplier:function(frm){
		if (frm.doc.type_of_supplier==""){
			frm.set_df_property("employee", "hidden", 1);
			frm.set_df_property("supplier_code", "hidden", 1);
			frm.set_df_property("employee_name", "hidden", 1);
			frm.set_df_property("name_of_supplier", "hidden", 1);
			frm.set_value('employee', '')
			frm.set_value('supplier_code', '')

		}
		if (frm.doc.type_of_supplier=="Employee"){
			frm.set_df_property("employee", "hidden", 0);
			frm.set_df_property("employee", "reqd", 1);
			frm.set_df_property("supplier_code", "hidden", 1);
			frm.set_df_property("employee_name", "hidden", 0);
			frm.set_df_property("name_of_supplier", "hidden", 1);
			frm.set_value('supplier_code', '')
		}
		if (frm.doc.type_of_supplier=="Supplier"){
			frm.set_df_property("supplier_code", "hidden", 0);
			frm.set_df_property("supplier_code", "reqd", 1);
			frm.set_df_property("employee", "hidden", 1);
			frm.set_df_property("employee_name", "hidden", 1);
			frm.set_df_property("name_of_supplier", "hidden", 0);
			frm.set_value('employee', '')
}
}
});