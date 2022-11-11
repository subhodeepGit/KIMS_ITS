// Copyright (c) 2022, SOUL and contributors
// For license information, please see license.txt

frappe.ui.form.on('Patient Refund', "amount_deposited_by_patient", function(frm) {
		var net_amount = 0;
		net_amount = cur_frm.doc.amount_deposited_by_patient - cur_frm.doc.approval_of_tpa__insurance__corporate__ostf - cur_frm.doc.cash_refund - cur_frm.doc.total_bill - cur_frm.doc.less__non_admissible_item__discount_amount
		frm.set_value("net_refundable_in_figures",net_amount)
		refresh_field("net_refundable_in_figures");
		
});
frappe.ui.form.on('Patient Refund', "approval_of_tpa__insurance__corporate__ostf", function(frm) {
	var net_amount = 0;
	net_amount = cur_frm.doc.amount_deposited_by_patient - cur_frm.doc.approval_of_tpa__insurance__corporate__ostf - cur_frm.doc.cash_refund - cur_frm.doc.total_bill - cur_frm.doc.less__non_admissible_item__discount_amount
	frm.set_value("net_refundable_in_figures",net_amount)
	refresh_field("net_refundable_in_figures");
	
});
frappe.ui.form.on('Patient Refund', "cash_refund", function(frm) {
	var net_amount = 0;
	net_amount = cur_frm.doc.amount_deposited_by_patient - cur_frm.doc.approval_of_tpa__insurance__corporate__ostf - cur_frm.doc.cash_refund - cur_frm.doc.total_bill - cur_frm.doc.less__non_admissible_item__discount_amount
	frm.set_value("net_refundable_in_figures",net_amount)
	refresh_field("net_refundable_in_figures");
	
});
frappe.ui.form.on('Patient Refund', "total_bill", function(frm) {
	var net_amount = 0;
	net_amount = cur_frm.doc.amount_deposited_by_patient - cur_frm.doc.approval_of_tpa__insurance__corporate__ostf - cur_frm.doc.cash_refund - cur_frm.doc.total_bill - cur_frm.doc.less__non_admissible_item__discount_amount
	frm.set_value("net_refundable_in_figures",net_amount)
	refresh_field("net_refundable_in_figures");
	
});
frappe.ui.form.on('Patient Refund', "less__non_admissible_item__discount_amount", function(frm) {
	var net_amount = 0;
	net_amount = cur_frm.doc.amount_deposited_by_patient - cur_frm.doc.approval_of_tpa__insurance__corporate__ostf - cur_frm.doc.cash_refund - cur_frm.doc.total_bill - cur_frm.doc.less__non_admissible_item__discount_amount
	frm.set_value("net_refundable_in_figures",net_amount)
	refresh_field("net_refundable_in_figures");
	
});