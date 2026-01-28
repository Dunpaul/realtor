import frappe

def property_before_delete(doc, method=None):
    # Block delete if any Property Unit references this Property
    exists = frappe.db.exists("Property Unit", {"property": doc.name})
    if exists:
        frappe.throw(f"Cannot delete Property '{doc.name}' because it has Property Units. Delete units first.")
