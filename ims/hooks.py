from . import __version__ as app_version

app_name = "ims"
app_title = "Ims"
app_publisher = "SOUL"
app_description = "IMS"
app_email = "soul@soul.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ims/css/ims.css"
# app_include_js = "/assets/ims/js/ims.js"

# include js, css files in header of web template
# web_include_css = "/assets/ims/css/ims.css"
# web_include_js = "/assets/ims/js/ims.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "ims/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "ims.utils.jinja_methods",
#	"filters": "ims.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "ims.install.before_install"
# after_install = "ims.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "ims.uninstall.before_uninstall"
# after_uninstall = "ims.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ims.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	# "*": {
	# 	"on_update": "method",
	# 	"on_cancel": "method",
	# 	"on_trash": "method"
	# }
    "File": {
		"validate": "ims.ims.validations.file.validate",
	},
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"cron": {
		"30 8,12,16 * * *": [
			"ims.tasks.cron_tab"
		],
		"30 8,12,16 * * *": [
			"ims.tasks.reject_transfer"
		],
		"30 8,12,16 * * *": [
			"ims.tasks.notification_for_approval"
		],
		"30 8,12,16 * * *": [
			"ims.tasks.notesheet_reminder_mail"
		],
		"*/5 * * * *": [
			"ims.employee_permission_schedular.employee_user"
		]
	},
}
#	"all": [
#		"ims.tasks.all"
#	],
#	"daily": [
#		"ims.tasks.daily"
#	],
#	"hourly": [
#		"ims.tasks.hourly"
#	],
#	"weekly": [
#		"ims.tasks.weekly"
#	],
#	"monthly": [
#		"ims.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "ims.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "ims.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "ims.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"ims.auth.validate"
# ]

# fixtures = [
# 	{"dt": "Custom DocPerm", "filters": [
# 		[
# 			"parent", "not in", [
# 				"DocType"
# 			]
# 		]
# # 	]},
# 	{"dt": "Workflow"},
#     {"dt": "Workflow State"},
#     {"dt": "Workflow Action Master"},
    # {"dt": "Module Profile"},
# ]