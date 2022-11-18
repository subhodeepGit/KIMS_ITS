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

frappe.ui.form.on("Batch Payment Process", {
	//  open of pop up 
	get_outstanding_amount: function(frm) {
		const today = frappe.datetime.get_today();
		const fields = [
			{fieldtype:"Section Break", label: __("Posting Date")},
			{fieldtype:"Date", label: __("From Date"),
				fieldname:"from_posting_date", default:frappe.datetime.add_days(today, -30)},
			{fieldtype:"Column Break"},
			{fieldtype:"Date", label: __("To Date"), fieldname:"to_posting_date", default:today},
			{fieldtype:"Section Break", label: __("Due Date")},
			{fieldtype:"Date", label: __("From Date"), fieldname:"from_due_date"},
			{fieldtype:"Column Break"},
			{fieldtype:"Date", label: __("To Date"), fieldname:"to_due_date"},
			{fieldtype:"Section Break", label: __("Outstanding Amount")},
			{fieldtype:"Float", label: __("Greater Than Amount"),
				fieldname:"outstanding_amt_greater_than", default: 0},
			{fieldtype:"Column Break"},
			{fieldtype:"Float", label: __("Less Than Amount"), fieldname:"outstanding_amt_less_than"},
			{fieldtype:"Section Break"},
			// {fieldtype:"Link", label:__("Cost Center"), fieldname:"cost_center", options:"Cost Center",
			// default:frm.doc.cost_center,
			// 	"get_query": function() {
			// 		return {
			// 			"filters": {"company": frm.doc.company}
			// 		}
			// 	}
			// },
			// {fieldtype:"Column Break"},
			{fieldtype:"Section Break"},
			{fieldtype:"Check", label: __("Allocate Payment Amount"), fieldname:"allocate_payment_amount", default:1},
		];
		frappe.prompt(fields, function(filters){
			frappe.flags.allocate_payment_amount = true;
			frm.events.validate_filters_data(frm, filters);
			// frm.doc.cost_center = filters.cost_center;
			frm.events.get_outstanding_documents(frm, filters);
		}, __("Filters"), __("Get Outstanding Documents"));
	},

	validate_filters_data: function(frm, filters) {
		const fields = {
			'Posting Date': ['from_posting_date', 'to_posting_date'],
			'Due Date': ['from_posting_date', 'to_posting_date'],
			'Advance Amount': ['from_posting_date', 'to_posting_date'],
		};

		for (let key in fields) {
			let from_field = fields[key][0];
			let to_field = fields[key][1];

			if (filters[from_field] && !filters[to_field]) {
				frappe.throw(
					__("Error: {0} is mandatory field", [to_field.replace(/_/g, " ")])
				);
			} else if (filters[from_field] && filters[from_field] > filters[to_field]) {
				frappe.throw(
					__("{0}: {1} must be less than {2}", [key, from_field.replace(/_/g, " "), to_field.replace(/_/g, " ")])
				);
			}
		}
	},
	get_outstanding_documents: function(frm, filters) {
		frm.clear_table("table_26");
		frappe.call({
			method: "ims.ims.doctype.batch_payment_process.batch_payment_process.get_outstanding_amount",
			args:{
				company: frm.doc.company,

			},
			
			callback: function(r) {
				if(r.message){
					frappe.model.clear_table(frm.doc, 'table_26');
					(r.message).forEach(element => {
						var c = frm.add_child("table_26")
						c.vendor_name=element.name_of_supplier
						c.vendor_code=element.supplier_code
					});
				} 
				frm.refresh();
				frm.refresh_field("table_26")
			}
		});
	}
});
