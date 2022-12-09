// Copyright (c) 2022, SOUL and contributors
// For license information, please see license.txt

frappe.ui.form.on('Third-Party Verification', {
	// refresh: function(frm) {
	// 	// $('.primary-action').prop('hidden', true); //hide save button
	// 	$('.btn-primary').hide(); //hide all button
	// 	}
});
frappe.ui.form.on('Third-Party Verification', {
	refresh: function(frm) {
		if(frm.doc.workflow_state=="Draft" || frm.is_new()==1){
			frm.set_df_property('review_comment', 'reqd', 0)
			frm.set_df_property('review_document', 'reqd', 0)
		}else{
			frm.set_df_property('review_comment', 'reqd', 1)
			frm.set_df_property('review_document', 'reqd', 1)
		}
	}
});