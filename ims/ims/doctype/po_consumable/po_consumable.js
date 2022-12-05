// Copyright (c) 2022, SOUL and contributors
// For license information, please see license.txt

// Child table Calculation
frappe.ui.form.on('Details of Invoices and PO', {	//Child table Name
	invoices_amountin_rs:function(frm, cdt, cdn){	//Child table field Name where you data enter
	var d = locals[cdt][cdn];
	var total = 0;
	let a= parseInt(total)
	frm.doc.details_of_invoices_and_po.forEach(function(d)  { a = a+ d.invoices_amountin_rs; }); //Child table name and field name
	frm.set_value("total_amount_in_rs", a);			// Parent field name where calculation going to fetch
	refresh_field("total_amount_in_rs");
	frm.set_value("net_final_amount_to_be_paid_in_rs",a) // Parent field name where calculation going to fetch
	refresh_field("net_final_amount_to_be_paid_in_rs");
  },
  // When field is deleted from child table on that time calculation going to happend to the accordingly
  details_of_invoices_and_po_remove:function(frm, cdt, cdn){ //Child table name
	var d = locals[cdt][cdn];
	var total = 0;
	let a= parseInt(total)
	frm.doc.details_of_invoices_and_po.forEach(function(d) { a += d.invoices_amountin_rs; });
	frm.set_value("total_amount_in_rs", a);
	refresh_field("total_amount_in_rs");
	frm.set_value("net_final_amount_to_be_paid_in_rs",a)
	refresh_field("net_final_amount_to_be_paid_in_rs");
	}
});

// Calculation
frappe.ui.form.on('PO Consumable',"advance_amount_already_paid_in_rs", function(frm) {
	var net_amount = 0;
	net_amount = cur_frm.doc.total_amount_in_rs - cur_frm.doc.tds_amount_to_be_deducted_in_rs - cur_frm.doc.advance_amount_already_paid_in_rs
	frm.set_value("net_final_amount_to_be_paid_in_rs",net_amount)
	refresh_field("net_final_amount_to_be_paid_in_rs");
});
frappe.ui.form.on('PO Consumable',"tds_amount_to_be_deducted_in_rs", function(frm) {
	var net_amount = 0;
	net_amount = cur_frm.doc.total_amount_in_rs - cur_frm.doc.advance_amount_already_paid_in_rs - cur_frm.doc.tds_amount_to_be_deducted_in_rs
	frm.set_value("net_final_amount_to_be_paid_in_rs",net_amount)
	refresh_field("net_final_amount_to_be_paid_in_rs");
});
frappe.ui.form.on('PO Consumable',"net_final_amount_to_be_paid_in_rs", function(frm) {
	var net_amount = 0;
	net_amount = cur_frm.doc.total_amount_in_rs - cur_frm.doc.tds_amount_to_be_deducted_in_rs - cur_frm.doc.advance_amount_already_paid_in_rs
	frm.set_value("net_final_amount_to_be_paid_in_rs",net_amount)
	refresh_field("net_final_amount_to_be_paid_in_rs");
});
frappe.ui.form.on('PO Consumable',"net_final_amount_to_be_paid_in_rs", function(frm) {
	var net_amount = 0;
	net_amount = cur_frm.doc.total_amount_in_rs - cur_frm.doc.advance_amount_already_paid_in_rs - cur_frm.doc.tds_amount_to_be_deducted_in_rs
	frm.set_value("net_final_amount_to_be_paid_in_rs",net_amount)
	refresh_field("net_final_amount_to_be_paid_in_rs");
});
frappe.ui.form.on('PO Consumable', {
	total_amount_in_rs: function(frm) {
	var net_amount = 0;
	net_amount = cur_frm.doc.total_amount_in_rs - cur_frm.doc.advance_amount_already_paid_in_rs - cur_frm.doc.tds_amount_to_be_deducted_in_rs
	frm.set_value("net_final_amount_to_be_paid_in_rs",net_amount)
	refresh_field("net_final_amount_to_be_paid_in_rs");
	}
});

// Child table field Mandatory when workflow state in draft
frappe.ui.form.on('PO Consumable', {
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


frappe.ui.form.on("PO Consumable", {
	onload:function(frm){
		//cannot able to add rows
		frm.set_df_property("authorized_signature", "cannot_add_rows", true);
		//cannot able to delete rows
		frm.set_df_property("authorized_signature", "cannot_delete_rows", true);
		if (frm.doc.workflow_state=="Passed for Payment" || frm.doc.workflow_state=="Draft"){
			frm.set_df_property("third_party_verification", "cannot_add_rows", true);
			frm.set_df_property("third_party_verification", "cannot_delete_rows", true);
		}
	},

});

// frappe.ui.form.on('PO Consumable', {
// 	refresh: function(frm) {
// 		if(frm.doc.workflow_state=="Approved by Director"){
// 			frm.set_df_property('audit_ref_no', 'reqd', 1)
// 		}
// 	}
// });
// frappe.ui.form.on('PO Consumable', {
// 	refresh: function(frm) {
// 		// $('.primary-action').prop('hidden', true); //hide save button
// 		$('.btn-primary').hide(); //hide all button
// 		}
// });

frappe.ui.form.on('PO Consumable', {
	supplier_code: function(frm) {
		frappe.call({
			method: 'ims.ims.doctype.po_consumable.po_consumable.clearance_period',
			args: {
				supplier:frm.doc.supplier_code
			},
			callback: function(r) {
				frm.set_value("amount_clearance_period_in_days",r.message)
			}
		})

	}
});

// frappe.ui.form.on('PO Consumable', {
//     refresh: function(frm) {
// 		frm.fields_dict["details_of_invoices_and_po"].grid.add_custom_button(__('Download Attachments'), 
// 		function() {
// 			var urls = [];
// 			let selected = frm.get_selected();
// 			// alert(JSON.stringify(selected));
// 			let sel = selected["details_of_invoices_and_po"];
// 			// alert(sel);
// 			// code to download selected rows
// 			for (var i = 0; i < cur_frm.doc.details_of_invoices_and_po.length; i++) {
// 				// alert(cur_frm.doc.details_of_invoices_and_po[i].name)
// 				for (var j = 0; j < sel.length; j++) {
// 					if(sel[j]==cur_frm.doc.details_of_invoices_and_po[i].name){
// 						// alert(cur_frm.doc.details_of_invoices_and_po[i].name)
// 						const data = cur_frm.doc.details_of_invoices_and_po[i].invoice_attachment;
// 						const data1 = cur_frm.doc.details_of_invoices_and_po[i].credit_memo;
// 						const data2 = cur_frm.doc.details_of_invoices_and_po[i].document_attachment;
// 						const data3 = cur_frm.doc.details_of_invoices_and_po[i].purchase_received_note_attachment;
// 						const data4 = cur_frm.doc.details_of_invoices_and_po[i].po_attachment;
// 						const data5 = cur_frm.doc.details_of_invoices_and_po[i].bill_summary;
// 						const data6 = cur_frm.doc.details_of_invoices_and_po[i].comparative_statement_attachment;
// 						const data7 = cur_frm.doc.details_of_invoices_and_po[i].delivery_challan;
// 						const data8 = cur_frm.doc.details_of_invoices_and_po[i].grn;
// 						const data9 = cur_frm.doc.details_of_invoices_and_po[i].purchase_notesheet_attachment;
// 						// const a = document.createElement('a');
// 						// a.href = data;
						
// 						// a.download = data.split('/').pop();
// 						// document.body.appendChild(a);
// 						// a.click();
// 						// document.body.removeChild(a);
						
// 						if (cur_frm.doc.details_of_invoices_and_po[i].invoice_attachment_1 == 1){
// 							urls.push(data);
// 						}
// 						if (cur_frm.doc.details_of_invoices_and_po[i].credit_memo_attachment == 1){
// 							urls.push(data1);
// 						}
// 						if (cur_frm.doc.details_of_invoices_and_po[i].document_attachment_1 == 1){
// 							urls.push(data2);
// 						}
// 						if (cur_frm.doc.details_of_invoices_and_po[i].purchase_received_note == 1){
// 							urls.push(data3);
// 						}
// 						if (cur_frm.doc.details_of_invoices_and_po[i].po_attachment_attachment == 1){
// 							urls.push(data4);
// 						}
// 						if (cur_frm.doc.details_of_invoices_and_po[i].bill_summary_attachment == 1){
// 							urls.push(data5);
// 						}
// 						if (cur_frm.doc.details_of_invoices_and_po[i].comparative_statement == 1){
// 							urls.push(data6);
// 						}
// 						if (cur_frm.doc.details_of_invoices_and_po[i].delivery_challan_attachment == 1){
// 							urls.push(data7);
// 						}
// 						if (cur_frm.doc.details_of_invoices_and_po[i].grn_attachment == 1){
// 							urls.push(data8);
// 						}
// 						if (cur_frm.doc.details_of_invoices_and_po[i].purchase_notesheet == 1){
// 							urls.push(data9);
// 						}
						
// 					}
// 				}
// 				}
// 				console.log(urls);

// 				var interval = setInterval(download, 400, urls);

// 				function download(urls) {
// 				var url = urls.pop();

// 				var a = document.createElement("a");
// 				a.download = url.split('/').pop();
// 				document.body.appendChild(a);
// 				a.setAttribute('href', url);
// 				// a.setAttribute('target', '_blank');
// 				document.body.removeChild(a);
// 				a.click();

// 				if (urls.length == 0) {
// 					clearInterval(interval);
// 				}
// 				}

// 		});
// 	frm.fields_dict["details_of_invoices_and_po"].grid.grid_buttons.find('.btn-custom').removeClass('btn-default').addClass('btn-primary');
// 	}
// });




frappe.ui.form.on('PO Consumable', {
	refresh: function(frm) {
		frappe.call({
            method: "ims.ims.doctype.po_consumable.po_consumable.get_table_attachments",
            callback: function(r) { 
                if (r.message){

					frm.fields_dict["details_of_invoices_and_po"].grid.add_custom_button(__('Download Attachments'), 
					function() {
						const attachment_map = r.message
						
						var urls = [];
						let selected = frm.get_selected();
						let sel = selected["details_of_invoices_and_po"];
						for (var i = 0; i < cur_frm.doc.details_of_invoices_and_po.length; i++) {
							for (var j = 0; j < sel.length; j++) {
								if(sel[j]==cur_frm.doc.details_of_invoices_and_po[i].name){
									var att1 = attachment_map;
									var iter1 = att1.values();
									for (let ele1 of iter1) {
										var att_fld=ele1['att_fieldname'];
										var chk_fld=ele1['chk_fieldname'];
										var att_fld_data=cur_frm.doc.details_of_invoices_and_po[i][att_fld];
										var chk_fld_data=cur_frm.doc.details_of_invoices_and_po[i][chk_fld];
										var idx_data=cur_frm.doc.details_of_invoices_and_po[i].idx;
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
				frm.fields_dict["details_of_invoices_and_po"].grid.grid_buttons.find('.btn-custom').removeClass('btn-default').addClass('btn-primary');
            	} 
			}
        })
	},
});	