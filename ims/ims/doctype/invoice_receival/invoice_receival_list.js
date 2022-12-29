if (!frappe.user.has_role(["Administrator","System Manager"])){ 
    frappe.listview_settings['Invoice Receival'] = {
        onload: function(me) {
            $(".filter-selector").hide();
            frappe.route_options = {
                "owner": frappe.session.user,
            };
        }
    }
}
