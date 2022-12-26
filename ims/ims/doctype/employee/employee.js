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


frappe.ui.form.on('Employee', {
	onload: function(frm) {
		if (frappe.session.user==frm.doc.email){
			frm.set_df_property("new_password", "read_only", 0);
			frm.set_df_property("enabled", "read_only", 1);
			frm.set_df_property("first_name", "read_only", 1);
			frm.set_df_property("middle_name", "read_only", 1);
			frm.set_df_property("last_name", "read_only", 1);
			frm.set_df_property("salutation", "read_only", 1);
			frm.set_df_property("employment_type", "read_only", 1);
			frm.set_df_property("mobile_no", "read_only", 0);
			frm.set_df_property("company", "read_only", 1);
			frm.set_df_property("status", "read_only", 1);
			frm.set_df_property("gender", "read_only", 0);
			frm.set_df_property("date_of_birth", "read_only", 0);
			frm.set_df_property("date_of_joining", "read_only", 1);
			frm.set_df_property("employee_number", "read_only", 1);
			frm.set_df_property("email", "read_only", 1);
			frm.set_df_property("emergency_contact_name", "hidden", 0);
			frm.set_df_property("emergency_phone", "hidden", 0);
			frm.set_df_property("relation", "hidden", 0);
			frm.set_df_property("department", "read_only", 1);
			frm.set_df_property("designation", "read_only", 1);
			frm.set_df_property("reports_to", "read_only", 0);
			frm.set_df_property("grade", "read_only", 0);
			frm.set_df_property("branch", "read_only", 0);
			frm.set_df_property("third_party_employee", "read_only", 1);
			frm.set_df_property("role", "read_only", 1);
			frm.set_df_property("signature", "read_only", 0);
			frm.set_df_property("account_holder_name", "hidden", 0);
			frm.set_df_property("bank_ac_no", "hidden", 0);
			frm.set_df_property("bank_name", "hidden", 0);
			frm.set_df_property("amount_clearance_period_in_days", "hidden", 0);
			frm.set_df_property("ifsc_code", "hidden", 0);
			frm.set_df_property("branch_name", "hidden", 0);
			frm.set_df_property("bank_address", "hidden", 0);
		}
		else{
			frm.set_df_property("new_password", "read_only", 1);
			frm.set_df_property("enabled", "read_only", 1);
			frm.set_df_property("first_name", "read_only", 1);
			frm.set_df_property("middle_name", "read_only", 1);
			frm.set_df_property("last_name", "read_only", 1);
			frm.set_df_property("salutation", "read_only", 1);
			frm.set_df_property("employment_type", "read_only", 1);
			frm.set_df_property("mobile_no", "read_only", 1);
			frm.set_df_property("company", "read_only", 1);
			frm.set_df_property("status", "read_only", 1);
			frm.set_df_property("gender", "hidden", 1);
			frm.set_df_property("date_of_birth", "read_only", 1);
			frm.set_df_property("date_of_joining", "read_only", 1);
			frm.set_df_property("employee_number", "read_only", 1);
			frm.set_df_property("email", "read_only", 1);
			frm.set_df_property("emergency_contact_name", "hidden", 1);
			frm.set_df_property("emergency_phone", "hidden", 1);
			frm.set_df_property("relation", "hidden", 1);
			frm.set_df_property("department", "read_only", 1);
			frm.set_df_property("designation", "read_only", 1);
			frm.set_df_property("reports_to", "read_only", 1);
			frm.set_df_property("grade", "read_only", 1);
			frm.set_df_property("branch", "read_only", 1);
			frm.set_df_property("third_party_employee", "read_only", 1);
			frm.set_df_property("role", "read_only", 1);
			frm.set_df_property("signature", "read_only", 1);
			frm.set_df_property("account_holder_name", "hidden", 1);
			frm.set_df_property("bank_ac_no", "hidden", 1);
			frm.set_df_property("bank_name", "hidden", 1);
			frm.set_df_property("amount_clearance_period_in_days", "hidden", 1);
			frm.set_df_property("ifsc_code", "hidden", 1);
			frm.set_df_property("branch_name", "hidden", 1);
			frm.set_df_property("bank_address", "hidden", 1);
		}
		if (frappe.session.user=="Administrator" || frappe.user.has_role(["System Manager"])){
			frm.set_df_property("new_password", "read_only", 0);
			frm.set_df_property("enabled", "read_only", 0);
			frm.set_df_property("first_name", "read_only", 0);
			frm.set_df_property("middle_name", "read_only", 0);
			frm.set_df_property("last_name", "read_only", 0);
			frm.set_df_property("salutation", "read_only", 0);
			frm.set_df_property("employment_type", "read_only", 0);
			frm.set_df_property("mobile_no", "read_only", 0);
			frm.set_df_property("company", "read_only", 0);
			frm.set_df_property("status", "read_only", 0);
			frm.set_df_property("gender", "read_only", 0);
			frm.set_df_property("date_of_birth", "read_only", 0);
			frm.set_df_property("date_of_joining", "read_only", 0);
			frm.set_df_property("employee_number", "read_only", 0);
			frm.set_df_property("email", "read_only", 0);
			frm.set_df_property("emergency_contact_name", "hidden", 0);
			frm.set_df_property("emergency_phone", "hidden", 0);
			frm.set_df_property("relation", "hidden", 0);
			frm.set_df_property("department", "read_only", 0);
			frm.set_df_property("designation", "read_only", 0);
			frm.set_df_property("reports_to", "read_only", 0);
			frm.set_df_property("grade", "read_only", 0);
			frm.set_df_property("branch", "read_only", 0);
			frm.set_df_property("third_party_employee", "read_only", 0);
			frm.set_df_property("role", "read_only", 0);
			frm.set_df_property("signature", "read_only", 0);
			frm.set_df_property("account_holder_name", "hidden", 0);
			frm.set_df_property("bank_ac_no", "hidden", 0);
			frm.set_df_property("bank_name", "hidden", 0);
			frm.set_df_property("amount_clearance_period_in_days", "hidden", 0);
			frm.set_df_property("ifsc_code", "hidden", 0);
			frm.set_df_property("branch_name", "hidden", 0);
			frm.set_df_property("bank_address", "hidden", 0);
		}
	}
});
