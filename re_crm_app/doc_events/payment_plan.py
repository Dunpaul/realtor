import frappe
from frappe.utils import add_months, getdate

def _cycle_to_months(cycle: str) -> int:
    return {
        "Monthly": 1,
        "Quarterly": 3,
        "Semi-Annual": 6,
        "Annual": 12,
    }.get(cycle, 1)

def _round2(v: float) -> float:
    return round(float(v or 0), 2)

def offer_letter_validate(doc, method=None):
    # Only run if the scheduling fields are present and meaningful
    cycle = doc.get("payment_cycle")
    start_date = doc.get("schedule_start_date")
    installments = int(doc.get("installments") or 0)

    # If user hasn't opted into schedule fields, don't interfere
    if not cycle or not start_date or installments <= 0:
        return

    offer_price = float(doc.get("offer_price") or 0)
    deposit = float(doc.get("deposit_amount") or 0)
    balance = offer_price - deposit

    if balance <= 0:
        frappe.throw("Offer Price must be greater than Deposit Amount to generate a payment plan.")

    # If table exists and looks intentionally maintained, you can choose either:
    # A) enforce regeneration always
    # B) regenerate only if empty
    #
    # I recommend B to avoid frustrating users who intentionally customize amounts/dates.
    if doc.get("payment_plan") and len(doc.payment_plan) > 0:
        return

    # Generate payment_plan rows
    step = _cycle_to_months(cycle)
    start = getdate(start_date)

    doc.set("payment_plan", [])
    base_amt = _round2(balance / installments)

    allocated = 0.0
    for i in range(1, installments + 1):
        due = add_months(start, step * (i - 1))

        amt = base_amt
        if i == installments:
            amt = _round2(balance - allocated)

        allocated += amt

        doc.append("payment_plan", {
            "milestone": f"{cycle} Installment {i}/{installments}",
            "due_date": due,
            "amount": amt
        })
