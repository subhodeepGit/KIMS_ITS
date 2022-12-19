// Copyright (c) 2022, SOUL and contributors
// For license information, please see license.txt

frappe.ui.form.on('Invoice Receival', {
	type_of_supplier: function(frm) {
		if (frm.doc.type_of_supplier==""){
			frm.set_df_property("employee", "hidden", 1);
			frm.set_df_property("supplier_code", "hidden", 1);
			frm.set_df_property("employee_name", "hidden", 1);
			frm.set_df_property("supplier_name", "hidden", 1);
			frm.set_value('employee', '')
			frm.set_value('supplier_code', '')
		}
		if (frm.doc.type_of_supplier=="Employee"){
			frm.set_df_property("employee", "hidden", 0);
			frm.set_df_property("employee", "reqd", 1);
			frm.set_df_property("supplier_code", "hidden", 1);
			frm.set_df_property("employee_name", "hidden", 0);
			frm.set_df_property("supplier_name", "hidden", 1);
			frm.set_value('supplier_code', '')
		}
		else{
			frm.set_df_property("employee", "reqd", 0);
		}
		if (frm.doc.type_of_supplier=="Supplier"){
			frm.set_df_property("supplier_code", "hidden", 0);
			frm.set_df_property("employee", "hidden", 1);
			frm.set_df_property("supplier_code", "reqd", 1);
			frm.set_df_property("employee", "hidden", 1);
			frm.set_df_property("employee_name", "hidden", 1);
			frm.set_df_property("supplier_name", "hidden", 0);
			frm.set_value('employee', '')
			}
		else{
			frm.set_df_property("supplier_code", "reqd", 0);
		}
	}
});
frappe.ui.form.on('Invoice Receival', {
	onload: function(frm) {
		if (frm.doc.type_of_supplier==""){
			frm.set_df_property("employee", "hidden", 1);
			frm.set_df_property("supplier_code", "hidden", 1);
			frm.set_df_property("employee_name", "hidden", 1);
			frm.set_df_property("supplier_name", "hidden", 1);
			frm.set_value('employee', '')
			frm.set_value('supplier_code', '')
		}
		if (frm.doc.type_of_supplier=="Employee"){
			frm.set_df_property("employee", "hidden", 0);
			frm.set_df_property("employee", "reqd", 1);
			frm.set_df_property("supplier_code", "hidden", 1);
			frm.set_df_property("employee_name", "hidden", 0);
			frm.set_df_property("supplier_name", "hidden", 1);
			frm.set_value('supplier_code', '')
		}
		else{
			frm.set_df_property("employee", "reqd", 0);
		}
		if (frm.doc.type_of_supplier=="Supplier"){
			frm.set_df_property("supplier_code", "hidden", 0);
			frm.set_df_property("employee", "hidden", 1);
			frm.set_df_property("supplier_code", "reqd", 1);
			frm.set_df_property("employee", "hidden", 1);
			frm.set_df_property("employee_name", "hidden", 1);
			frm.set_df_property("supplier_name", "hidden", 0);
			frm.set_value('employee', '')
			}
		else{
			frm.set_df_property("supplier_code", "reqd", 0);
		}
	}
});