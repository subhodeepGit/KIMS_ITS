// Copyright (c) 2022, SOUL and contributors
// For license information, please see license.txt

frappe.ui.form.on('Batch Payment Process', {
	onload: function(frm) {
		var df1 = frappe.meta.get_docfield("Authorized Signature","transfer_to", cur_frm.doc.name);
		df1.hidden = 1;
		var df1 = frappe.meta.get_docfield("Authorized Signature","disapproval_check", cur_frm.doc.name);
		df1.hidden = 1;
		var df1 = frappe.meta.get_docfield("Authorized Signature","remarks", cur_frm.doc.name);
		df1.hidden = 1;
		}
});
frappe.ui.form.on("Batch Payment Process", {
	onload:function(frm){
		//cannot able to add rows
		frm.set_df_property("approval_hierarchy", "cannot_add_rows", true);
		//cannot able to delete rows
		frm.set_df_property("approval_hierarchy", "cannot_delete_rows", true);
	}
});
