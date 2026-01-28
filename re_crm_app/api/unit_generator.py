import frappe

def _pad(n: int, width: int = 3) -> str:
    return str(n).zfill(width)

@frappe.whitelist()
def generate_units(property_name: str) -> dict:
    prop = frappe.get_doc("Property", property_name)

    if not prop.get("unit_plan"):
        frappe.throw("No Unit Plan found. Add unit types and counts first.")

    created = 0
    skipped = 0
    created_units = []

    # Optional: base prefix from property name (safe slug-ish)
    base_prefix = (prop.name or "PROP").upper().replace(" ", "-")

    for plan in prop.unit_plan:
        unit_type = plan.get("unit_type")
        qty = int(plan.get("count") or 0)
        if not unit_type or qty <= 0:
            continue

        prefix = (plan.get("code_prefix") or f"{base_prefix}-{unit_type}").upper().replace(" ", "-")
        start_number = int(plan.get("start_number") or 1)

        for i in range(start_number, start_number + qty):
            unit_code = f"{prefix}-{_pad(i)}"

            # Idempotent: do not recreate if it exists
            if frappe.db.exists("Property Unit", unit_code):
                skipped += 1
                continue

            unit = frappe.new_doc("Property Unit")
            unit.property = prop.name
            unit.unit_code = unit_code
            unit.unit_type = unit_type
            unit.availability_status = "Available"

            # Defaults from plan
            if plan.get("size"):
                unit.size = plan.size
            if plan.get("listing_price") is not None:
                unit.listing_price = plan.listing_price
            if plan.get("rent_price") is not None:
                unit.rent_price = plan.rent_price

            unit.insert(ignore_permissions=True)
            created += 1
            created_units.append(unit.name)

    return {
        "created": created,
        "skipped": skipped,
        "units": created_units[:50],  # avoid huge payload
    }

@frappe.whitelist()
def regenerate_units(property_name: str, confirm: int = 0) -> dict:
    if not confirm:
        frappe.throw("Confirmation required.")

    # Only delete units that belong to this property
    unit_names = frappe.get_all("Property Unit", filters={"property": property_name}, pluck="name")

    # Safety: Do not delete units that are reserved/sold/rented
    locked = frappe.get_all(
        "Property Unit",
        filters={"property": property_name, "availability_status": ["in", ["Reserved", "Sold", "Rented"]]},
        pluck="name",
    )
    if locked:
        frappe.throw(
            "Cannot regenerate because some units are Reserved/Sold/Rented:\n" + "\n".join(locked[:20])
        )

    for name in unit_names:
        frappe.delete_doc("Property Unit", name, ignore_permissions=True, force=1)

    # Reuse your existing generator
    return generate_units(property_name)
