// Copyright (c) 2022, SOUL and contributors
// For license information, please see license.txt

frappe.ui.form.on('Role Permission Setting', {
	role:function(frm){
	frm.clear_table("table_2")
	frappe.call({
		method:"ims.ims.doctype.role_permission_setting.role_permission_setting.get_doctype_list",
		args: {
			role: frm.doc.role,
		},
		callback: function(r){
			if(r.message) {
				// alert(r.message)
				(r.message).forEach(element => {
					var c = frm.add_child("table_2")
					// c.fees_category = element.fees_category ["name","select","read","write","create","del","report","export","import","print"]
					c.doctype_name = element.doctype_name
					c.select = element.select
					c.read = element.read
					c.write = element.write
					c.create = element.create
					c.del_data = element.del_data
					c.report = element.report
					c.export = element.export
					c.import_data = element.import_data
					c.print = element.print
				});
				frm.refresh_field("table_2")
			}
		}
	})
},
onload:function(frm){
	//cannot able to add rows
	frm.set_df_property("table_2", "cannot_add_rows", true);
}
});



