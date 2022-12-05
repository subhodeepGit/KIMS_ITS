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
	frm.set_value("to_pay_total", a); // Parent field name where calculation going to fetch
	refresh_field("to_pay_total");
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
	frm.set_value("less_credit_note_amount_in_rs",b)
	refresh_field("less_credit_note_amount_in_rs");
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
		frm.set_value("less_credit_note_amount_in_rs", a);
		refresh_field("less_credit_note_amount_in_rs");
	},
	// to_pay:function(frm, cdt, cdn){	//Child table field Name where you data enter
	// 	var d = locals[cdt][cdn];
	// 	var total = 0;
	// 	let b= parseInt(total)
	// 	frm.doc.details_of_invoices_credit_note_and_po.forEach(function(d)  { b = b+ d.to_pay;}); //Child table name and field name
	// 	frm.set_value("to_pay_total", b);			
	// 	refresh_field("to_pay_total");
	// },
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
		},
});

frappe.ui.form.on('PO Consignment',"less_credit_note_amount_in_rs", function(frm) {
	var net_amount = 0;
	net_amount = cur_frm.doc.total_amount_in_rs - cur_frm.doc.less_credit_note_amount_in_rs
	frm.set_value("net_final_amount_to_be_paid_in_rs",net_amount)
	refresh_field("net_final_amount_to_be_paid_in_rs");
	frm.set_value("to_pay_total",net_amount)
	refresh_field("to_pay_total");
});

frappe.ui.form.on("PO Consignment", {
	onload:function(frm){
		//cannot able to add rows
		frm.set_df_property("authorized_signature", "cannot_add_rows", true);
		//cannot able to delete rows
		frm.set_df_property("authorized_signature", "cannot_delete_rows", true);
		if (frm.doc.workflow_state=="Passed for Payment" || frm.doc.workflow_state=="Draft"){
			frm.set_df_property("third_party_verification", "cannot_add_rows", true);
			frm.set_df_property("third_party_verification", "cannot_delete_rows", true);
		}
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

frappe.ui.form.on("Credit Note and PO", "hospital_margin_amount", function(frm, cdt, cdn){
	var d = locals[cdt][cdn];
		d.to_pay=d.invoice_amount-d.hospital_margin_amount
		refresh_field("to_pay", d.name, d.parentfield);
	});

frappe.ui.form.on("Credit Note and PO", "invoice_amount", function(frm, cdt, cdn){
	var d = locals[cdt][cdn];
		d.to_pay=d.invoice_amount-d.hospital_margin_amount
		refresh_field("to_pay", d.name, d.parentfield);
	});

// Child table field Mandatory when workflow state in draft
frappe.ui.form.on('PO Consignment', {
	before_load: function(frm) {
		frm.trigger("mandatory_field");
		},
		mandatory_field(frm){
			// frm.set_df_property('note_sheet_no', 'read_only', 1);
			if(frm.doc.workflow_state=="Draft"){
				frm.set_value("document_status","Invoice in Draft State")
				refresh_field("document_status");
				var df1 = frappe.meta.get_docfield("Details of Invoices and PO","po_attachment_attachment", cur_frm.doc.name);
				df1.reqd = 1; // not working
			}
			
			if(frm.is_new()==1){
				frm.set_df_property('note_sheet_no', 'read_only', 0)
				frm.set_df_property('company', 'read_only', 0)
				frm.set_df_property('date_of_note_sheet', 'read_only', 0)
				frm.set_df_property('name_of_schooldepartment', 'read_only', 0)
				frm.set_df_property('for_which_department', 'read_only', 0)
				frm.set_df_property("item_of_purchaseexpense",'read_only', 0)
				frm.set_df_property("supplier_code",'read_only', 0)
				frm.set_df_property("audit_ref_no",'read_only', 1)
				frm.set_df_property("today_date",'read_only', 1)
				frm.set_df_property("profit_center",'read_only', 1)
				frm.set_df_property("document_number",'read_only', 1)
				frm.set_df_property("ref_no",'read_only', 1)
				frm.set_df_property("document_date",'read_only', 1)
				frm.set_df_property("attach_journal_voucher",'read_only', 1)
				// frm.set_df_property("third_party_verification", "cannot_add_rows", true);
				// frm.set_df_property("third_party_verification", "cannot_delete_rows", true);
			}
			else{
				if(frm.doc.workflow_state=="Draft" || frm.doc.workflow_state=="Verify and Save" ){
					frm.set_df_property('note_sheet_no', 'read_only', 0)
					frm.set_df_property('company', 'read_only', 0)
					frm.set_df_property('date_of_note_sheet', 'read_only', 0)
					frm.set_df_property('name_of_schooldepartment', 'read_only', 0)
					frm.set_df_property('for_which_department', 'read_only', 0)
					frm.set_df_property("item_of_purchaseexpense",'read_only', 0)
					frm.set_df_property("supplier_code",'read_only', 0)
				}
				else{
					frm.set_df_property('note_sheet_no', 'read_only', 1)
					frm.set_df_property('company', 'read_only', 1)
					frm.set_df_property('date_of_note_sheet', 'read_only', 1)
					frm.set_df_property('name_of_schooldepartment', 'read_only', 1)
					frm.set_df_property('for_which_department', 'read_only', 1)
					frm.set_df_property("item_of_purchaseexpense",'read_only', 1)
					frm.set_df_property("supplier_code",'read_only', 1)
				}
		
				if (frm.doc.workflow_state=="Approved by Director, Administration"){
					frm.set_df_property("audit_ref_no", "reqd", 1);
					frm.set_df_property("today_date", "reqd", 1);
					frm.set_df_property("audit_ref_no",'read_only', 0)
					frm.set_df_property("today_date",'read_only', 0)
				}
				else {
					frm.set_df_property("audit_ref_no",'read_only', 1)
					frm.set_df_property("today_date",'read_only', 1)
				}
				if (frm.doc.workflow_state=="Journal Entry by Account Dept."){
					frm.set_df_property("profit_center",'read_only', 0)
					frm.set_df_property("document_number",'read_only', 0)
					frm.set_df_property("ref_no",'read_only', 0)
					frm.set_df_property("document_date",'read_only', 0)
					frm.set_df_property("attach_journal_voucher",'read_only', 0)
					frm.set_df_property("profit_center",'reqd', 1)
					frm.set_df_property("document_number",'reqd', 1)
					frm.set_df_property("ref_no",'reqd', 1)
					frm.set_df_property("document_date",'reqd', 1)
					frm.set_df_property("attach_journal_voucher",'reqd', 1)
				}
				else{
					frm.set_df_property("profit_center",'read_only', 1)
					frm.set_df_property("document_number",'read_only', 1)
					frm.set_df_property("ref_no",'read_only', 1)
					frm.set_df_property("document_date",'read_only', 1)
					frm.set_df_property("attach_journal_voucher",'read_only', 1)
				}
				// eval:(doc.workflow_state=="Approved by Director, Administration");/
				// eval:(doc.workflow_state=="Approved by Director, Administration");today_dateToday
				// eval:(doc.workflow_state=="Passed for Payment") || (doc.workflow_state=="Cancelled")
				// eval:(doc.workflow_state=="Passed for Payment") || (doc.workflow_state=="Cancelled")
// 				eval:(doc.workflow_state=="Approved by Director, Administration") || (doc.workflow_state=="Bill Received by Audit") || (doc.workflow_state=="Approved by Audit User") || (doc.workflow_state=="Approved by Pro VC") || (doc.workflow_state=="Journal Entry by Account Dept.") || (doc.workflow_state=="Passed for Payment")
				// || (doc.workflow_state=="Approved by Auditor(Audit Verification)")
				// eval:(doc.workflow_state=="Journal Entry by Account Dept.") || (doc.workflow_state=="Passed for Payment");

			}
		},
		before_save: function(frm) {
			frm.trigger("mandatory_field");
		},
});	


frappe.ui.form.on('PO Consignment', {
	refresh: function(frm) {
		frappe.call({
            method: "ims.ims.doctype.po_consignment.po_consignment.get_table_attachments",
            callback: function(r) { 
                if (r.message){

					frm.fields_dict["details_of_invoices_credit_note_and_po"].grid.add_custom_button(__('Download Attachments'), 
					function() {
						const attachment_map = r.message
						
						var urls = [];
						let selected = frm.get_selected();
						let sel = selected["details_of_invoices_credit_note_and_po"];
						for (var i = 0; i < cur_frm.doc.details_of_invoices_credit_note_and_po.length; i++) {
							for (var j = 0; j < sel.length; j++) {
								if(sel[j]==cur_frm.doc.details_of_invoices_credit_note_and_po[i].name){
									var att1 = attachment_map;
									var iter1 = att1.values();
									for (let ele1 of iter1) {
										var att_fld=ele1['att_fieldname'];
										var chk_fld=ele1['chk_fieldname'];
										var att_fld_data=cur_frm.doc.details_of_invoices_credit_note_and_po[i][att_fld];
										var chk_fld_data=cur_frm.doc.details_of_invoices_credit_note_and_po[i][chk_fld];
										var idx_data=cur_frm.doc.details_of_invoices_credit_note_and_po[i].idx;
										var rename_data = att_fld + idx_data;
										if(chk_fld_data == 1) {
											var url_obj = {dwnld : att_fld_data, rename : rename_data};
											urls.push(url_obj);
										}

									}
								}
							}
						}
						console.log(urls);

						var interval = setInterval(download, 400, urls);

						function download(urls) {
							let url = new Array();
							url = urls.pop();

							var a = document.createElement("a");
							a.download =  url['dwnld'].split('/').pop();
							a.setAttribute('download', url['rename']);
							document.body.appendChild(a);
							a.setAttribute('href', url['dwnld']);
							document.body.removeChild(a);
							a.click();

							if (urls.length == 0) {
								clearInterval(interval);
							}
						}


						
					});
				frm.fields_dict["details_of_invoices_credit_note_and_po"].grid.grid_buttons.find('.btn-custom').removeClass('btn-default').addClass('btn-primary');
            	} 
			}
        })
	},
});	