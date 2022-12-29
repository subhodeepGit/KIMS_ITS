if (!frappe.user.has_role(["Administrator","System Manager"])){ 
    frappe.listview_settings['Employee'] = {
        onload: function(me) {
            $(".filter-selector").hide();
            frappe.route_options = {
                "email": frappe.session.user,
            };
        }
    }
}