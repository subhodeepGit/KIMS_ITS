// Copyright (c) 2022, SOUL and contributors
// For license information, please see license.txt

frappe.ui.form.on('Patient Refund', "amount_deposited_by_patient", function(frm) {
	var net_amount = 0;
	net_amount = (cur_frm.doc.amount_deposited_by_patient - cur_frm.doc.cash_refund) - (cur_frm.doc.total_bill - cur_frm.doc.approval_of_tpa__insurance__corporate__ostf - cur_frm.doc.less__non_admissible_item__discount_amount - cur_frm.doc.less__approval_approval_letter_to_be_attached)
	frm.set_value("net_refundable_in_figures",net_amount)
	refresh_field("net_refundable_in_figures");	
});
frappe.ui.form.on('Patient Refund', "approval_of_tpa__insurance__corporate__ostf", function(frm) {
	var net_amount = 0;
	net_amount = (cur_frm.doc.amount_deposited_by_patient - cur_frm.doc.cash_refund) - (cur_frm.doc.total_bill - cur_frm.doc.approval_of_tpa__insurance__corporate__ostf - cur_frm.doc.less__non_admissible_item__discount_amount - cur_frm.doc.less__approval_approval_letter_to_be_attached)
	frm.set_value("net_refundable_in_figures",net_amount)
	refresh_field("net_refundable_in_figures");
});
frappe.ui.form.on('Patient Refund', "cash_refund", function(frm) {
	var net_amount = 0;
	net_amount = (cur_frm.doc.amount_deposited_by_patient - cur_frm.doc.cash_refund) - (cur_frm.doc.total_bill - cur_frm.doc.approval_of_tpa__insurance__corporate__ostf - cur_frm.doc.less__non_admissible_item__discount_amount - cur_frm.doc.less__approval_approval_letter_to_be_attached)
	frm.set_value("net_refundable_in_figures",net_amount)
	refresh_field("net_refundable_in_figures");
});
frappe.ui.form.on('Patient Refund', "total_bill", function(frm) {
	var net_amount = 0;
	net_amount = (cur_frm.doc.amount_deposited_by_patient - cur_frm.doc.cash_refund) - (cur_frm.doc.total_bill - cur_frm.doc.approval_of_tpa__insurance__corporate__ostf - cur_frm.doc.less__non_admissible_item__discount_amount - cur_frm.doc.less__approval_approval_letter_to_be_attached)
	frm.set_value("net_refundable_in_figures",net_amount)
	refresh_field("net_refundable_in_figures");	
});
frappe.ui.form.on('Patient Refund', "less__non_admissible_item__discount_amount", function(frm) {
	var net_amount = 0;
	net_amount = (cur_frm.doc.amount_deposited_by_patient - cur_frm.doc.cash_refund) - (cur_frm.doc.total_bill - cur_frm.doc.approval_of_tpa__insurance__corporate__ostf - cur_frm.doc.less__non_admissible_item__discount_amount - cur_frm.doc.less__approval_approval_letter_to_be_attached)
	frm.set_value("net_refundable_in_figures",net_amount)
	refresh_field("net_refundable_in_figures");
});
frappe.ui.form.on('Patient Refund', "less__approval_approval_letter_to_be_attached", function(frm) {
	var net_amount = 0;
	net_amount = (cur_frm.doc.amount_deposited_by_patient - cur_frm.doc.cash_refund) - (cur_frm.doc.total_bill - cur_frm.doc.approval_of_tpa__insurance__corporate__ostf - cur_frm.doc.less__non_admissible_item__discount_amount - cur_frm.doc.less__approval_approval_letter_to_be_attached)
	frm.set_value("net_refundable_in_figures",net_amount)
	refresh_field("net_refundable_in_figures");
});
frappe.ui.form.on('Patient Refund', "ip__uhid_no", function(frm) {
	var ip ="";
	ip = cur_frm.doc.ip__uhid_no;
	frm.set_value("patient_ip_no",ip);
	refresh_field("patient_ip_no");
});
frappe.ui.form.on('Patient Refund', "name_of_the_patient", function(frm) {
	var name_patient = "";
	name_patient = cur_frm.doc.name_of_the_patient;
	frm.set_value("patients_name",name_patient);
	refresh_field("patients_name");
});
frappe.ui.form.on('Patient Refund', {
	ifsc_code: function(frm) {
		frappe.call({
			method: 'ims.ims.doctype.supplier.supplier.ifsc_code',
			
			args: {
				ifsc_code:frm.doc.ifsc_code,
			},
			callback: function(r) {
				var out_put=r.message
				frm.set_value("name_of_the_bank",out_put['BANK'])
				frm.set_value("branch",out_put['BRANCH'])
				frm.set_value("bank_address",out_put['ADDRESS'])
			}
		})

	}
});