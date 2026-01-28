app_name = "re_crm_app"
app_title = "Re Crm App"
app_publisher = "Dunpaul"
app_description = "Real estate app"
app_email = "mainadunpaul@gmail.com"
app_license = "mit"

doctype_js = {
	"Reservation": "public/js/reservation.js",
	"Offer Letter": "public/js/offer_letter.js",
	"Property": "public/js/property.js",
}

doc_events = {
  "Reservation": {
    "on_update": "re_crm_app.doc_events.unit_status.reservation_on_update",
  },
  "Sales Agreement": {
    "on_update": "re_crm_app.doc_events.unit_status.sales_agreement_on_update",
  },
  "Property": {
    "before_delete": "re_crm_app.doc_events.property_guards.property_before_delete",
  },
}

doc_events.update({
  "Reservation": {
    "validate": "re_crm_app.doc_events.validation.reservation_validate",
    "on_update": "re_crm_app.doc_events.unit_status.reservation_on_update",
  },
  "Sales Agreement": {
    "validate": "re_crm_app.doc_events.validation.agreement_validate",
    "on_update": "re_crm_app.doc_events.unit_status.sales_agreement_on_update",
  },
  "Property Unit": {
    "on_update": "re_crm_app.doc_events.unit_stats.unit_on_update",
    "on_trash": "re_crm_app.doc_events.unit_stats.unit_on_trash",
  },
  "Offer Letter": {
    "validate": "re_crm_app.doc_events.payment_plan.offer_letter_validate",
  }
})

doctype_js.update({
  "Sales Agreement": "public/js/sales_agreement.js",
})



# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "re_crm_app",
# 		"logo": "/assets/re_crm_app/logo.png",
# 		"title": "Re Crm App",
# 		"route": "/re_crm_app",
# 		"has_permission": "re_crm_app.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/re_crm_app/css/re_crm_app.css"
# app_include_js = "/assets/re_crm_app/js/re_crm_app.js"

# include js, css files in header of web template
# web_include_css = "/assets/re_crm_app/css/re_crm_app.css"
# web_include_js = "/assets/re_crm_app/js/re_crm_app.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "re_crm_app/public/scss/website"

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

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "re_crm_app/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "re_crm_app.utils.jinja_methods",
# 	"filters": "re_crm_app.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "re_crm_app.install.before_install"
# after_install = "re_crm_app.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "re_crm_app.uninstall.before_uninstall"
# after_uninstall = "re_crm_app.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "re_crm_app.utils.before_app_install"
# after_app_install = "re_crm_app.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "re_crm_app.utils.before_app_uninstall"
# after_app_uninstall = "re_crm_app.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "re_crm_app.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"re_crm_app.tasks.all"
# 	],
# 	"daily": [
# 		"re_crm_app.tasks.daily"
# 	],
# 	"hourly": [
# 		"re_crm_app.tasks.hourly"
# 	],
# 	"weekly": [
# 		"re_crm_app.tasks.weekly"
# 	],
# 	"monthly": [
# 		"re_crm_app.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "re_crm_app.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "re_crm_app.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "re_crm_app.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["re_crm_app.utils.before_request"]
# after_request = ["re_crm_app.utils.after_request"]

# Job Events
# ----------
# before_job = ["re_crm_app.utils.before_job"]
# after_job = ["re_crm_app.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"re_crm_app.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

fixtures = [
    {
        "dt": "Workspace",
        "filters": [
            ["module", "in", ["Re Crm App"]]  # adjust module names if different; include "Home" if customized
        ]
    },
    # "Desk Page",  # captures desk layouts if customized
    "Module Def",  # for module visibility/icons/order in sidebar
    # Add these if you have custom reports/dashboards
    # "Report",
    # "Dashboard",
]
