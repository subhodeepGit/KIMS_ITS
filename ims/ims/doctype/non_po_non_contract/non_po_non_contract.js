// Copyright (c) 2022, SOUL and contributors
// For license information, please see license.txt

// frappe.ui.form.on('Non PO Non Contract', {
// 	// refresh: function(frm) {

// 	// }
// });
frappe.ui.form.on('Details Enclosed Bills', {	
	invoice_amount:function(frm, cdt, cdn){	
	var d = locals[cdt][cdn];
	var total = 0;
	let a= parseInt(total)
	frm.doc.details_of_enclosed_bills.forEach(function(d)  { a = a+ d.invoice_amount; }); 
	frm.set_value("total_amount_in_rs", a);			
	refresh_field("total_amount_in_rs");
	frm.set_value("net_final_amount_to_be_paid_in_rs",a) 
	refresh_field("net_final_amount_to_be_paid_in_rs");
  },
  details_of_enclosed_bills_remove:function(frm, cdt, cdn){ 
	var d = locals[cdt][cdn];
	var total = 0;
	let a= parseInt(total)
	frm.doc.details_of_enclosed_bills.forEach(function(d) { a += d.invoice_amount; });
	frm.set_value("total_amount_in_rs", a);
	refresh_field("total_amount_in_rs");
	frm.set_value("net_final_amount_to_be_paid_in_rs",a)
	refresh_field("net_final_amount_to_be_paid_in_rs");
	}
});

frappe.ui.form.on('Non PO Non Contract',"advance_amount_already_paid_in_rs", function(frm) {
	var net_amount = 0;
	net_amount = cur_frm.doc.total_amount_in_rs - cur_frm.doc.tds_amount_to_be_deducted_in_rs - cur_frm.doc.advance_amount_already_paid_in_rs
	frm.set_value("net_final_amount_to_be_paid_in_rs",net_amount)
	refresh_field("net_final_amount_to_be_paid_in_rs");
});
frappe.ui.form.on('Non PO Non Contract',"tds_amount_to_be_deducted_in_rs", function(frm) {
	var net_amount = 0;
	net_amount = cur_frm.doc.total_amount_in_rs - cur_frm.doc.advance_amount_already_paid_in_rs - cur_frm.doc.tds_amount_to_be_deducted_in_rs
	frm.set_value("net_final_amount_to_be_paid_in_rs",net_amount)
	refresh_field("net_final_amount_to_be_paid_in_rs");
});
frappe.ui.form.on('Non PO Non Contract',"net_final_amount_to_be_paid_in_rs", function(frm) {
	var net_amount = 0;
	net_amount = cur_frm.doc.total_amount_in_rs - cur_frm.doc.tds_amount_to_be_deducted_in_rs - cur_frm.doc.advance_amount_already_paid_in_rs
	frm.set_value("net_final_amount_to_be_paid_in_rs",net_amount)
	refresh_field("net_final_amount_to_be_paid_in_rs");
});
frappe.ui.form.on('Non PO Non Contract',"net_final_amount_to_be_paid_in_rs", function(frm) {
	var net_amount = 0;
	net_amount = cur_frm.doc.total_amount_in_rs - cur_frm.doc.advance_amount_already_paid_in_rs - cur_frm.doc.tds_amount_to_be_deducted_in_rs
	frm.set_value("net_final_amount_to_be_paid_in_rs",net_amount)
	refresh_field("net_final_amount_to_be_paid_in_rs");
});
frappe.ui.form.on('Non PO Non Contract', {
	total_amount_in_rs: function(frm) {
	var net_amount = 0;
	net_amount = cur_frm.doc.total_amount_in_rs - cur_frm.doc.advance_amount_already_paid_in_rs - cur_frm.doc.tds_amount_to_be_deducted_in_rs
	frm.set_value("net_final_amount_to_be_paid_in_rs",net_amount)
	refresh_field("net_final_amount_to_be_paid_in_rs");
	}
});

frappe.ui.form.on("Non PO Non Contract", {
	onload:function(frm){
		//cannot able to add rows
		frm.set_df_property("authorized_signature", "cannot_add_rows", true);
		//cannot able to delete rows
		frm.set_df_property("authorized_signature", "cannot_delete_rows", true);
}
});
frappe.ui.form.on("Non PO Non Contract", {
	onload:function(frm){
	if (frm.doc.type_of_supplier==""){
		frm.set_df_property("employee", "hidden", 1);
		frm.set_df_property("supplier_code", "hidden", 1);
		frm.set_df_property("employee_name", "hidden", 1);
			frm.set_df_property("name_of_supplier", "hidden", 1);
			frm.set_value('employee', '')
			frm.set_value('supplier_code', '')
		}
		if (frm.doc.type_of_supplier=="Employee"){
			frm.set_df_property("employee", "hidden", 0);
			frm.set_df_property("employee", "reqd", 1);
			frm.set_df_property("supplier_code", "hidden", 1);
			frm.set_df_property("employee_name", "hidden", 0);
			frm.set_df_property("name_of_supplier", "hidden", 1);
			frm.set_value('supplier_code', '')
			// 
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
			frm.set_df_property("name_of_supplier", "hidden", 0);
			frm.set_value('employee', '')
			}
		else{
			frm.set_df_property("supplier_code", "reqd", 0);
			}
}
});
frappe.ui.form.on("Non PO Non Contract", {
	type_of_supplier:function(frm){
		if (frm.doc.type_of_supplier==""){
			frm.set_df_property("employee", "hidden", 1);
			frm.set_df_property("supplier_code", "hidden", 1);
			frm.set_df_property("employee_name", "hidden", 1);
			frm.set_df_property("name_of_supplier", "hidden", 1);
			frm.set_value('employee', '')
			frm.set_value('supplier_code', '')
		}
		if (frm.doc.type_of_supplier=="Employee"){
			frm.set_df_property("employee", "hidden", 0);
			frm.set_df_property("employee", "reqd", 1);
			frm.set_df_property("supplier_code", "hidden", 1);
			frm.set_df_property("employee_name", "hidden", 0);
			frm.set_df_property("name_of_supplier", "hidden", 1);
			frm.set_value('supplier_code', '')
			// 
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
			frm.set_df_property("name_of_supplier", "hidden", 0);
			frm.set_value('employee', '')
			}
		else{
			frm.set_df_property("supplier_code", "reqd", 0);
		}
}
});

frappe.ui.form.on('Non PO Non Contract', {
	supplier_code: function(frm) {
		if (frm.doc.type_of_supplier=="Supplier"){
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

	}
});


frappe.ui.form.on('Non PO Non Contract', {
	employee: function(frm) {
		if (frm.doc.type_of_supplier=="Employee"){
			frappe.call({
				method: 'ims.ims.doctype.non_po_non_contract.non_po_non_contract.emp_clearance_period',
				args: {
					employee:frm.doc.employee
				},
				callback: function(r) {
					if(r.message){
					frm.set_value("amount_clearance_period_in_days",r.message)
					}
					frm.refresh()
					frm.refresh_field("employee")
			}
			})
		}

	}
});

// Child table field Mandatory when workflow state in draft
frappe.ui.form.on('Non PO Non Contract', {
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
					frm.set_df_property("type_of_supplier",'read_only', 1)
					frm.set_df_property("employee",'read_only', 1)
					frm.set_df_property("purchase_order_no",'read_only', 1)
					frm.set_df_property("date_of_purchase_order",'read_only', 1)
					frm.set_df_property("master_invoice_attachment",'read_only', 1)
					frm.set_df_property("note_sheet_attachment",'read_only', 1)
				}
		
				if (frm.doc.workflow_state=="Approved by Medical Superintendent"){
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
					frm.set_df_property("amount_clearance_period_in_days",'read_only', 1)
				}
				else{
					frm.set_df_property("profit_center",'read_only', 1)
					frm.set_df_property("document_number",'read_only', 1)
					frm.set_df_property("ref_no",'read_only', 1)
					frm.set_df_property("document_date",'read_only', 1)
					frm.set_df_property("attach_journal_voucher",'read_only', 1)
					frm.set_df_property("amount_clearance_period_in_days",'read_only', 0)
				}
				if (frm.doc.workflow_state=="Passed for Payment"){
					frm.set_df_property("amount_clearance_period_in_days",'read_only', 1)
				}
				else{
					frm.set_df_property("amount_clearance_period_in_days",'read_only', 0)
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

frappe.ui.form.on('Non PO Non Contract', {
	refresh: function(frm) {
		frappe.call({
            method: "ims.ims.doctype.non_po_non_contract.non_po_non_contract.get_table_attachments",
            callback: function(r) { 
                if (r.message){

					frm.fields_dict["details_of_enclosed_bills"].grid.add_custom_button(__('Download Attachments'), 
					function() {
						const attachment_map = r.message
						
						var urls = [];
						let selected = frm.get_selected();
						let sel = selected["details_of_enclosed_bills"];
						for (var i = 0; i < cur_frm.doc.details_of_enclosed_bills.length; i++) {
							for (var j = 0; j < sel.length; j++) {
								if(sel[j]==cur_frm.doc.details_of_enclosed_bills[i].name){
									var att1 = attachment_map;
									var iter1 = att1.values();
									for (let ele1 of iter1) {
										var att_fld=ele1['att_fieldname'];
										var chk_fld=ele1['chk_fieldname'];
										var att_fld_data=cur_frm.doc.details_of_enclosed_bills[i][att_fld];
										var chk_fld_data=cur_frm.doc.details_of_enclosed_bills[i][chk_fld];
										var idx_data=cur_frm.doc.details_of_enclosed_bills[i].idx;
										var rename_data = att_fld + idx_data;
										if(chk_fld_data == 1) {
											var url_obj = {dwnld : att_fld_data, rename : rename_data};
											urls.push(url_obj);
										}

									}
								}
							}
						}
						// console.log(urls);

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
				frm.fields_dict["details_of_enclosed_bills"].grid.grid_buttons.find('.btn-custom').removeClass('btn-default').addClass('btn-primary');
            	} 
			}
        })
	},
});	

frappe.ui.form.on('Non PO Non Contract', {
	refresh: function(frm) {
		if(frm.is_new()!=1){
			frappe.call({
				method: "ims.ims.doctype.non_po_non_contract.non_po_non_contract.get_action_acess",
				args: {
					self:frm.doc
				},
				callback: function(r) { 
					if (r.message!=0){
						$('.actions-btn-group').hide();
						$('.primary-action').prop('hidden', true);
						frm.refresh();
					}
					
				}
			})
		}
		// $('.primary-action').prop('hidden', true); //hide save button
		// $('.actions-btn-group').hide(); //hide all button
		}
});


frappe.ui.form.on('Non PO Non Contract', {
	setup: function(frm) {
		frm.set_query("employee_id", "third_party_verification", function(doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: [
					['Employee', 'third_party_employee', '=', 1],
				]
			};
		});
	},
});

frappe.ui.form.on('Non PO Non Contract', {
	setup:function(frm) { 
		frm.set_query("invoice_receival_no","details_of_enclosed_bills", function(_doc, cdt, cdn) {
			return {
			filters: [
				["employee",'=', frm.doc.employee],
				["supplier_code",'=', frm.doc.supplier_code],
				['Invoice Receival', 'invoice_status', '=', "Passed for Notesheet"]
			],
			};   
		}); 
	},
	
});