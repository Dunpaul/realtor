import frappe

def update_property_counters(property_name: str):
    if not property_name or not frappe.db.exists("Property", property_name):
        return

    total = frappe.db.count("Property Unit", {"property": property_name})
    available = frappe.db.count("Property Unit", {"property": property_name, "availability_status": "Available"})
    reserved = frappe.db.count("Property Unit", {"property": property_name, "availability_status": "Reserved"})
    sold = frappe.db.count("Property Unit", {"property": property_name, "availability_status": "Sold"})

    frappe.db.set_value("Property", property_name, {
        "total_units": total,
        "available_units": available,
        "reserved_units": reserved,
        "sold_units": sold,
    })
