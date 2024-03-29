// Copyright (c) 2022, SOUL and contributors
// For license information, please see license.txt

frappe.ui.form.on('Patient Refund', "amount_deposited_by_patient", function(frm) {
	var net_amount = 0;
	net_amount = (cur_frm.doc.amount_deposited_by_patient - cur_frm.doc.cash_refund) - (cur_frm.doc.total_bill - cur_frm.doc.approval_of_tpa__insurance__corporate__ostf - cur_frm.doc.less__non_admissible_item__discount_amount - cur_frm.doc.less__approval_approval_letter_to_be_attached)
	frm.set_value("net_refundable_in_figures",net_amount)
	refresh_field("net_refundable_in_figures");
	
	frm.set_value("refund_amount",net_amount)
	refresh_field("refund_amount");	
});
frappe.ui.form.on('Patient Refund', "approval_of_tpa__insurance__corporate__ostf", function(frm) {
	var net_amount = 0;
	net_amount = (cur_frm.doc.amount_deposited_by_patient - cur_frm.doc.cash_refund) - (cur_frm.doc.total_bill - cur_frm.doc.approval_of_tpa__insurance__corporate__ostf - cur_frm.doc.less__non_admissible_item__discount_amount - cur_frm.doc.less__approval_approval_letter_to_be_attached)
	frm.set_value("net_refundable_in_figures",net_amount)
	refresh_field("net_refundable_in_figures");

	frm.set_value("refund_amount",net_amount)
	refresh_field("refund_amount");	
});
frappe.ui.form.on('Patient Refund', "cash_refund", function(frm) {
	var net_amount = 0;
	net_amount = (cur_frm.doc.amount_deposited_by_patient - cur_frm.doc.cash_refund) - (cur_frm.doc.total_bill - cur_frm.doc.approval_of_tpa__insurance__corporate__ostf - cur_frm.doc.less__non_admissible_item__discount_amount - cur_frm.doc.less__approval_approval_letter_to_be_attached)
	frm.set_value("net_refundable_in_figures",net_amount)
	refresh_field("net_refundable_in_figures");

	frm.set_value("refund_amount",net_amount)
	refresh_field("refund_amount");	
});
frappe.ui.form.on('Patient Refund', "total_bill", function(frm) {
	var net_amount = 0;
	net_amount = (cur_frm.doc.amount_deposited_by_patient - cur_frm.doc.cash_refund) - (cur_frm.doc.total_bill - cur_frm.doc.approval_of_tpa__insurance__corporate__ostf - cur_frm.doc.less__non_admissible_item__discount_amount - cur_frm.doc.less__approval_approval_letter_to_be_attached)
	frm.set_value("net_refundable_in_figures",net_amount)
	refresh_field("net_refundable_in_figures");
	
	frm.set_value("refund_amount",net_amount)
	refresh_field("refund_amount");	
});
frappe.ui.form.on('Patient Refund', "less__non_admissible_item__discount_amount", function(frm) {
	var net_amount = 0;
	net_amount = (cur_frm.doc.amount_deposited_by_patient - cur_frm.doc.cash_refund) - (cur_frm.doc.total_bill - cur_frm.doc.approval_of_tpa__insurance__corporate__ostf - cur_frm.doc.less__non_admissible_item__discount_amount - cur_frm.doc.less__approval_approval_letter_to_be_attached)
	frm.set_value("net_refundable_in_figures",net_amount)
	refresh_field("net_refundable_in_figures");

	frm.set_value("refund_amount",net_amount)
	refresh_field("refund_amount");	
});
frappe.ui.form.on('Patient Refund', "less__approval_approval_letter_to_be_attached", function(frm) {
	var net_amount = 0;
	net_amount = (cur_frm.doc.amount_deposited_by_patient - cur_frm.doc.cash_refund) - (cur_frm.doc.total_bill - cur_frm.doc.approval_of_tpa__insurance__corporate__ostf - cur_frm.doc.less__non_admissible_item__discount_amount - cur_frm.doc.less__approval_approval_letter_to_be_attached)
	frm.set_value("net_refundable_in_figures",net_amount)
	refresh_field("net_refundable_in_figures");

	frm.set_value("refund_amount",net_amount)
	refresh_field("refund_amount");	
});
frappe.ui.form.on('Patient Refund', "ip__uhid_no", function(frm) {
	var ip ="";
	ip = cur_frm.doc.ip__uhid_no;
	frm.set_value("patient_ip_no",ip);
	refresh_field("patient_ip_no");
	frm.set_value("data_61",ip);
	refresh_field("data_61");
	frm.set_value("mrn_no",ip);
	refresh_field("mrn_no");
});
frappe.ui.form.on('Patient Refund', "account_holder_name", function(frm) {
	var ip ="";
	ip = cur_frm.doc.account_holder_name;
	frm.set_value("name_of_the_person",ip);
	refresh_field("name_of_the_person");
});
frappe.ui.form.on('Patient Refund', "name_of_the_patient", function(frm) {
	var name_patient = "";
	name_patient = cur_frm.doc.name_of_the_patient;
	frm.set_value("patients_name",name_patient);
	refresh_field("patients_name");
	frm.set_value("patients_name_self",name_patient);
	refresh_field("patients_name_self");
	frm.set_value("data_62",name_patient);
	refresh_field("data_62");
});
frappe.ui.form.on('Patient Refund', "approval_of_tpa__insurance__corporate__ostf", function(frm) {
	var amount_patient = "";
	amount_patient = cur_frm.doc.approval_of_tpa__insurance__corporate__ostf;
	frm.set_value("approved_amount",amount_patient);
	refresh_field("approved_amount");
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

frappe.ui.form.on("Patient Refund", {
	onload:function(frm){
		//cannot able to add rows
		frm.set_df_property("authorized_signature", "cannot_add_rows", true);
		//cannot able to delete rows
		frm.set_df_property("authorized_signature", "cannot_delete_rows", true);
	}
});


// frm.set_df_property("approval_attachment",'reqd', 1)
// Child table field Mandatory when workflow state in draft
// frappe.ui.form.on('Patient Refund', {
// 	before_load: function(frm) {
// 		frm.trigger("mandatory_field");
// 		},
// 		mandatory_field(frm){
			
// 			if (frm.doc.less__approval_approval_letter_to_be_attached!=0){
// 				alert("ok")
// 				frm.set_df_property("approval_attachment",'reqd', 1)
// 			}
// 		},
// 		before_save: function(frm) {
// 			frm.trigger("mandatory_field");
// 		},
// });

frappe.ui.form.on('Patient Refund', {
	less__approval_approval_letter_to_be_attached:function(frm){
		frm.trigger("mandatory");
	},
	mandatory(frm){
		if (frm.doc.less__approval_approval_letter_to_be_attached!=0){
			frm.set_df_property("approval_attachment",'reqd', 1)
			refresh_field("approval_attachment");
		}
		else{
			frm.set_df_property("approval_attachment",'reqd', 0)
			refresh_field("approval_attachment");
		}
	}
})

frappe.ui.form.on('Patient Refund', {
	concern_person:function(frm){
		if (frm.doc.concern_person!=""){
			frm.set_df_property("relationship",'reqd', 1)
			frm.set_df_property("self_declaration_form",'reqd', 1)
			frm.set_df_property("date_of_signature",'reqd', 1)
		}
		else{
			frm.set_df_property("relationship",'reqd', 0)
			frm.set_df_property("self_declaration_form",'reqd', 0)
			frm.set_df_property("date_of_signature",'reqd', 0)
		}

	},
})
frappe.ui.form.on('Patient Refund', {
	setup:function(frm){
		const date = new Date();
		let day = date.getDate();
		let month = date.getMonth() + 1;
		let year = date.getFullYear();
		// This arrangement can be altered based on how we want the date's format to appear.
		let currentDate = `${day}-${month}-${year}`;
		frm.set_query('type_of_insurance',function(){
			return{
				filters:[
				['Reason of Refund Master', 'validity_start_date', '<=', currentDate],
				['Reason of Refund Master', 'validity_end_date', '>=', currentDate ]
			]
			}
		})
		frm.set_query('name_of_the_insurance',function(){
			return{
				filters:[
				['Health Insurance Name', 'validity_start_date', '<=', currentDate],
				['Health Insurance Name', 'validity_end_date', '>=', currentDate ]
			]
			}
		})
	},
	type_of_insurance:function(frm){

		if (frm.doc.type_of_insurance!=""){
			frappe.call({
				method: 'ims.ims.doctype.patient_refund.patient_refund.insurance_check',
				args: {
					type_of_insurance:frm.doc.type_of_insurance,
				},
				callback: function(r) { 
					if (r.message){
						var out_put=r.message[0]
						// console.log(out_put['insurance_mandatory_check'])
						frm.set_df_property("approved_amount",'reqd', out_put['insurance_mandatory_check'])
						frm.set_df_property("name_of_the_insurance",'reqd', out_put['insurance_mandatory_check'])
						frm.set_df_property("insurance_details_attachment",'reqd', out_put['insurance_mandatory_check'])
					}
				}
			})
			// frm.set_df_property("approved_amount",'reqd', 1)
			// frm.set_df_property("name_of_the_insurance",'reqd', 1)
			// frm.set_df_property("insurance_details_attachment",'reqd', 1)
		}
		else{
			// frm.set_df_property("approved_amount",'reqd', 0)
			frm.set_df_property("name_of_the_insurance",'reqd', 0)
			frm.set_df_property("insurance_details_attachment",'reqd', 0)
		}

	},
})

frappe.ui.form.on('Patient Refund', {
	before_load: function(frm) {
		frm.trigger("mandatory_field");
		},
		mandatory_field(frm){
			// frm.set_df_property('note_sheet_no', 'read_only', 1);
			if(frm.doc.workflow_state=="Draft"){
				frm.set_value("document_status","Patient Refund in Draft State")
				refresh_field("document_status");
			}
			if(frm.is_new()==1){
				frm.set_df_property('name_of_the_patient', 'read_only', 0)
				frm.set_df_property('company', 'read_only', 0)
				frm.set_df_property('ip__uhid_no', 'read_only', 0)
				frm.set_df_property('name_of_schooldepartment', 'read_only', 0)
				frm.set_df_property('department', 'read_only', 0)
				frm.set_df_property("approval_attachment",'read_only', 0)
				frm.set_df_property("amount_deposited",'read_only', 0)
				frm.set_df_property("amount_deposited_through",'read_only', 0)
				frm.set_df_property("date_of_submission_of_fees",'read_only', 0)
				frm.set_df_property("date_of_cancellation",'read_only', 0)
				frm.set_df_property("doc_attached",'read_only', 0)
				frm.set_df_property("account_type",'read_only', 0)
				frm.set_df_property("joint_account_holder_name",'read_only', 0)
				frm.set_df_property("account_holder_relation_with_the_patient",'read_only', 0)
				frm.set_df_property("concern_person",'read_only', 0)
				frm.set_df_property("relationship",'read_only', 0)
				frm.set_df_property("self_declaration_form",'read_only', 0)
				// frm.set_df_property("patients_name_self",'read_only', 0)
				frm.set_df_property("date_of_signature",'read_only', 0)
				frm.set_df_property("bill_no",'read_only', 0)
				frm.set_df_property("bill_date",'read_only', 0)
				frm.set_df_property("final_bill",'read_only', 0)
				frm.set_df_property("date_of_refund",'read_only', 0)
				frm.set_df_property("refund_no",'read_only', 0)
				frm.set_df_property("refund_amount",'read_only', 0)
				frm.set_df_property("refund_sheet_attachment",'read_only', 0)
				frm.set_df_property("total_amount_refunded",'read_only', 0)
				frm.set_df_property("refund_attachment",'read_only', 0)
				frm.set_df_property("type_of_insurance",'read_only', 0)
				// frm.set_df_property("approved_amount",'read_only', 0)
				frm.set_df_property("name_of_the_insurance",'read_only', 0)
				frm.set_df_property("insurance_details_attachment",'read_only', 0)
				frm.set_df_property("xerox_copy_of_any_itenty_proof",'read_only', 0)
				frm.set_df_property("reason_of_cancellation",'read_only', 0)
				frm.set_df_property("ifsc_code",'read_only', 0)
				frm.set_df_property("account_no",'read_only', 0)
				

				// frm.set_df_property("third_party_verification", "cannot_add_rows", true);
				// frm.set_df_property("third_party_verification", "cannot_delete_rows", true);
			}
			else{
				if(frm.doc.workflow_state=="Draft" || frm.doc.workflow_state=="Verify and Save" ){
					frm.set_df_property('name_of_the_patient', 'read_only', 0)
					frm.set_df_property('company', 'read_only', 0)
					frm.set_df_property('ip__uhid_no', 'read_only', 0)
					frm.set_df_property('name_of_schooldepartment', 'read_only', 0)
					frm.set_df_property('department', 'read_only', 0)
					frm.set_df_property("approval_attachment",'read_only', 0)
					frm.set_df_property("amount_deposited",'read_only', 0)
					frm.set_df_property("amount_deposited_through",'read_only', 0)
					frm.set_df_property("date_of_submission_of_fees",'read_only', 0)
					frm.set_df_property("date_of_cancellation",'read_only', 0)
					frm.set_df_property("doc_attached",'read_only', 0)
					frm.set_df_property("account_type",'read_only', 0)
					frm.set_df_property("joint_account_holder_name",'read_only', 0)
					frm.set_df_property("account_holder_relation_with_the_patient",'read_only', 0)
					frm.set_df_property("concern_person",'read_only', 0)
					frm.set_df_property("relationship",'read_only', 0)
					frm.set_df_property("self_declaration_form",'read_only', 0)
					// frm.set_df_property("patients_name_self",'read_only', 0)
					frm.set_df_property("date_of_signature",'read_only', 0)
					frm.set_df_property("bill_no",'read_only', 0)
					frm.set_df_property("bill_date",'read_only', 0)
					frm.set_df_property("final_bill",'read_only', 0)
					frm.set_df_property("date_of_refund",'read_only', 0)
					frm.set_df_property("refund_no",'read_only', 0)
					frm.set_df_property("refund_amount",'read_only', 0)
					frm.set_df_property("refund_sheet_attachment",'read_only', 0)
					frm.set_df_property("total_amount_refunded",'read_only', 0)
					frm.set_df_property("refund_attachment",'read_only', 0)
					frm.set_df_property("type_of_insurance",'read_only', 0)
					// frm.set_df_property("approved_amount",'read_only', 0)
					frm.set_df_property("name_of_the_insurance",'read_only', 0)
					frm.set_df_property("insurance_details_attachment",'read_only', 0)
					frm.set_df_property("xerox_copy_of_any_itenty_proof",'read_only', 0)
					frm.set_df_property("reason_of_cancellation",'read_only', 0)
					frm.set_df_property("ifsc_code",'read_only', 0)
					frm.set_df_property("account_no",'read_only', 0)
				}
				else{
					frm.set_df_property('name_of_the_patient', 'read_only', 1)
					frm.set_df_property('company', 'read_only', 1)
					frm.set_df_property('ip__uhid_no', 'read_only', 1)
					frm.set_df_property('name_of_schooldepartment', 'read_only', 1)
					frm.set_df_property('department', 'read_only', 1)
					frm.set_df_property("approval_attachment",'read_only', 1)
					frm.set_df_property("amount_deposited",'read_only', 1)
					frm.set_df_property("amount_deposited_through",'read_only', 1)
					frm.set_df_property("date_of_submission_of_fees",'read_only', 1)
					frm.set_df_property("date_of_cancellation",'read_only', 1)
					frm.set_df_property("doc_attached",'read_only', 1)
					frm.set_df_property("account_type",'read_only', 1)
					frm.set_df_property("joint_account_holder_name",'read_only', 1)
					frm.set_df_property("account_holder_relation_with_the_patient",'read_only', 1)
					frm.set_df_property("concern_person",'read_only', 1)
					frm.set_df_property("relationship",'read_only', 1)
					frm.set_df_property("self_declaration_form",'read_only', 1)
					frm.set_df_property("account_holder_name",'read_only', 1)
					frm.set_df_property("date_of_signature",'read_only', 1)
					frm.set_df_property("bill_no",'read_only', 1)
					frm.set_df_property("bill_date",'read_only', 1)
					frm.set_df_property("final_bill",'read_only', 1)
					frm.set_df_property("date_of_refund",'read_only', 1)
					frm.set_df_property("refund_no",'read_only', 1)
					frm.set_df_property("refund_amount",'read_only', 1)
					frm.set_df_property("refund_sheet_attachment",'read_only', 1)
					frm.set_df_property("total_amount_refunded",'read_only', 1)
					frm.set_df_property("refund_attachment",'read_only', 1)
					frm.set_df_property("type_of_insurance",'read_only', 1)
					// frm.set_df_property("approved_amount",'read_only', 1)
					frm.set_df_property("name_of_the_insurance",'read_only', 1)
					frm.set_df_property("insurance_details_attachment",'read_only', 1)
					frm.set_df_property("xerox_copy_of_any_itenty_proof",'read_only', 1)
					frm.set_df_property("reason_of_cancellation",'read_only', 1)
					frm.set_df_property("ifsc_code",'read_only', 1)
					frm.set_df_property("account_no",'read_only', 1)
				}
				if (frm.doc.workflow_state=="Passed for Payment"){
					frm.set_df_property("total_bill",'read_only', 1)
				}

			}
		},
		before_save: function(frm) {
			frm.trigger("mandatory_field");
		},
});

frappe.ui.form.on('Patient Refund', {
    refresh: function(frm) {
      frm.add_custom_button(__('Download Attachments'), function(){
		var urls=[];
        var data = frm.doc.approval_attachment;
		urls.push(data);
		var data1 = frm.doc.doc_attached;
		urls.push(data1);
		var data2 = frm.doc.self_declaration_form;
		urls.push(data2);
		var data3 = frm.doc.final_bill;
		urls.push(data3);
		var data4 = frm.doc.refund_sheet_attachment;
		urls.push(data4);
		var data5 = frm.doc.refund_attachment;
		urls.push(data5);
		var data6 = frm.doc.insurance_details_attachment;
		urls.push(data6);
		var data7 = frm.doc.xerox_copy_of_any_itenty_proof;
		urls.push(data7);

		urls = urls.filter(function( element ) {
			return element !== undefined;
		});

		var interval = setInterval(download, 400, urls);

		function download(urls) {
			let url = new Array();
			url = urls.pop();

			var a = document.createElement("a");
			a.download =  url.split('/').pop();
			document.body.appendChild(a);
			a.setAttribute('href', url);
			document.body.removeChild(a);
			a.click();

			if (urls.length == 0) {
				clearInterval(interval);
			}
		}

    },
	);
  }
});
