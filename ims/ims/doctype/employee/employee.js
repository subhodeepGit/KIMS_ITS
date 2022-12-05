// Copyright (c) 2022, SOUL and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee', {
	ifsc_code: function(frm) {
		frappe.call({
			method: 'ims.ims.doctype.supplier.supplier.ifsc_code',
			
			args: {
				ifsc_code:frm.doc.ifsc_code,
			},
			callback: function(r) {
				var out_put=r.message
				frm.set_value("bank_name",out_put['BANK'])
				frm.set_value("branch_name",out_put['BRANCH'])
				frm.set_value("bank_address",out_put['ADDRESS'])
			}
		})

	}
});
