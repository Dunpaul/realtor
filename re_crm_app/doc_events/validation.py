import frappe

def reservation_validate(doc, method=None):
    if not doc.property_unit:
        return
    status = frappe.db.get_value("Property Unit", doc.property_unit, "availability_status")
    # allow editing same reservation
    if status in ("Reserved", "Sold", "Rented"):
        # allow if current doc is already linked and active? keep simple for now:
        if doc.is_new():
            frappe.throw(f"Unit {doc.property_unit} is currently {status}. Choose another unit.")

def agreement_validate(doc, method=None):
    if not doc.property_unit:
        return
    status = frappe.db.get_value("Property Unit", doc.property_unit, "availability_status")
    if status in ("Sold", "Rented"):
        if doc.is_new():
            frappe.throw(f"Unit {doc.property_unit} is already {status}.")
