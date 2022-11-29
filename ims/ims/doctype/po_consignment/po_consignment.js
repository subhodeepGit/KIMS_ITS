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
	frm.doc.details_of_invoices_credit_note_and_po.forEach(function(d)  { a = a+ d.invoice_amount;}); //Child table name and field name
	frm.set_value("total_amount_in_rs", a);			// Parent field name where calculation going to fetch
	refresh_field("total_amount_in_rs");
	frm.set_value("net_final_amount_to_be_paid_in_rs", a); // Parent field name where calculation going to fetch
	refresh_field("net_final_amount_to_be_paid_in_rs");
   },
  // When field is deleted from child table on that time calculation going to happend to the accordingly
    details_of_invoices_credit_note_and_po_remove:function(frm, cdt, cdn){ //Child table name
	var d = locals[cdt][cdn];
	var total = 0;
	let a= parseInt(total);
	var total1 = 0;
	let b= parseInt(total1);
	var total2 = 0;
	let c= parseInt(total2);
	frm.doc.details_of_invoices_credit_note_and_po.forEach(function(d) { a += d.invoice_amount; b += d.hospital_margin_amount; c += d.to_pay;});
	frm.set_value("total_amount_in_rs", a);
	refresh_field("total_amount_in_rs");
	frm.set_value("net_final_amount_to_be_paid_in_rs",a)
	refresh_field("net_final_amount_to_be_paid_in_rs");
	frm.set_value("total_hospital_margin_amount",b)
	refresh_field("total_hospital_margin_amount");
	frm.set_value("to_pay_total",c)
	refresh_field("to_pay_total");
	},
	hospital_margin_amount:function(frm, cdt, cdn){	//Child table field Name where you data enter
		var d = locals[cdt][cdn];
		var total = 0;
		let a= parseInt(total)
		frm.doc.details_of_invoices_credit_note_and_po.forEach(function(d)  { a = a+ d.hospital_margin_amount;}); //Child table name and field name
		frm.set_value("total_hospital_margin_amount", a);			
		refresh_field("total_hospital_margin_amount");
	},
	to_pay:function(frm, cdt, cdn){	//Child table field Name where you data enter
		var d = locals[cdt][cdn];
		var total = 0;
		let b= parseInt(total)
		frm.doc.details_of_invoices_credit_note_and_po.forEach(function(d)  { b = b+ d.to_pay;}); //Child table name and field name
		frm.set_value("to_pay_total", b);			
		refresh_field("to_pay_total");
	},
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

frappe.ui.form.on('PO Consignment', {
	supplier_code: function(frm) {
		frappe.call({
			method: 'ims.ims.doctype.po_consignment.po_consignment.clearance_period',
			args: {
				supplier:frm.doc.supplier_code
			},
			callback: function(r) {
				frm.set_value("amount_clearance_period_in_days",r.message)
			}
		})

	}
});