import frappe
from frappe.model.document import Document

@frappe.whitelist()
def make_offer_letter(reservation_name: str) -> str:
    reservation = frappe.get_doc("Reservation", reservation_name)

    offer = frappe.new_doc("Offer Letter")
    offer.reservation = reservation.name
    offer.lead = reservation.lead
    offer.customer = reservation.customer
    offer.property_unit = reservation.property_unit

    # sensible defaults
    offer.offer_price = 0
    offer.deposit_amount = reservation.reservation_fee or 0
    offer.valid_until = reservation.expiry_date

    # optional: copy terms
    if reservation.get("terms"):
        offer.terms = reservation.terms

    offer.insert(ignore_permissions=True)
    return offer.name

@frappe.whitelist()
def make_sales_agreement(offer_letter_name: str) -> str:
    offer = frappe.get_doc("Offer Letter", offer_letter_name)

    agreement = frappe.new_doc("Sales Agreement")
    agreement.offer_letter = offer.name
    agreement.customer = offer.customer
    agreement.property_unit = offer.property_unit
    agreement.selling_price = offer.offer_price or 0
    agreement.deposit_amount = offer.deposit_amount or 0

    # copy terms if your Sales Agreement has terms field
    if offer.get("terms") and agreement.meta.has_field("terms"):
        agreement.terms = offer.terms

    # copy milestones -> payment schedule if your fieldnames match
    # Offer Letter child table: payment_plan (milestone, due_date, amount)
    # Sales Agreement child table: payment_schedule (description, due_date, amount)
    if offer.get("payment_plan") and agreement.meta.has_field("payment_schedule"):
        for row in offer.payment_plan:
            agreement.append("payment_schedule", {
                "description": row.get("milestone"),
                "due_date": row.get("due_date"),
                "amount": row.get("amount"),
            })

    agreement.insert(ignore_permissions=True)
    return agreement.name

@frappe.whitelist()
def generate_invoices_from_schedule(agreement_name: str) -> list[str]:
    ag = frappe.get_doc("Sales Agreement", agreement_name)

    if not ag.customer:
        frappe.throw("Customer is required on Sales Agreement.")

    created = []
    if not ag.get("payment_schedule"):
        return created

    for row in ag.payment_schedule:
        # skip if already invoiced
        if row.get("invoice_reference"):
            continue
        amt = row.get("amount") or 0
        if amt <= 0:
            continue

        inv = frappe.new_doc("Sales Invoice")
        inv.customer = ag.customer
        inv.posting_date = frappe.utils.nowdate()
        inv.due_date = row.get("due_date") or frappe.utils.nowdate()

        # your custom references (must exist as custom fields)
        if inv.meta.has_field("real_estate_agreement"):
            inv.real_estate_agreement = ag.name
        if inv.meta.has_field("property_unit"):
            inv.property_unit = ag.property_unit

        # Minimal invoice line:
        # Use a real Item in production. For now, assume you have an Item "REAL-ESTATE-SERVICE" or similar.
        # If you don't, create an Item and replace item_code below.
        inv.append("items", {
            "item_code": "REAL-ESTATE-SERVICE",
            "qty": 1,
            "rate": amt,
            "description": row.get("description") or f"Installment for Agreement {ag.name}",
        })

        inv.insert(ignore_permissions=True)
        created.append(inv.name)

        # write back reference
        row.invoice_reference = inv.name

    ag.save(ignore_permissions=True)
    return created
