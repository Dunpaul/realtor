import frappe

def _set_unit_status(unit_name: str, status: str):
    if not unit_name:
        return
    if not frappe.db.exists("Property Unit", unit_name):
        return
    frappe.db.set_value("Property Unit", unit_name, "availability_status", status)

def reservation_on_update(doc, method=None):
    # Reserve unit when reservation is Active
    if doc.status == "Active":
        _set_unit_status(doc.property_unit, "Reserved")
    # Release unit if cancelled/expired (optional)
    if doc.status in ("Cancelled", "Expired"):
        # Only release if not sold by another agreement
        _set_unit_status(doc.property_unit, "Available")

def sales_agreement_on_update(doc, method=None):
    if doc.status in ("Active", "Completed"):
        _set_unit_status(doc.property_unit, "Sold")
    if doc.status in ("Terminated",):
        _set_unit_status(doc.property_unit, "Available")
