function addMonths(dateStr, months) {
  const d = frappe.datetime.str_to_obj(dateStr);
  d.setMonth(d.getMonth() + months);
  return frappe.datetime.obj_to_str(d);
}

function cycleToMonths(cycle) {
  switch (cycle) {
    case "Monthly": return 1;
    case "Quarterly": return 3;
    case "Semi-Annual": return 6;
    case "Annual": return 12;
    default: return 1;
  }
}

function round2(n) {
  return Math.round((n + Number.EPSILON) * 100) / 100;
}

function generateMilestones(frm) {
  const cycle = frm.doc.payment_cycle;
  const start = frm.doc.schedule_start_date;
  const n = cint(frm.doc.installments || 0);

  const offer = flt(frm.doc.offer_price || 0);
  const deposit = flt(frm.doc.deposit_amount || 0);
  const balance = offer - deposit;

  if (!cycle || !start || !n || n <= 0) return;
  if (balance <= 0) {
    frappe.msgprint("Balance is zero/negative. Adjust offer price and deposit.");
    return;
  }

  const step = cycleToMonths(cycle);

  // Clear existing rows
  frm.clear_table("payment_plan");

  const baseAmt = round2(balance / n);
  let allocated = 0;

  for (let i = 1; i <= n; i++) {
    const due = addMonths(start, step * (i - 1));
    let amt = baseAmt;

    // last installment adjusts rounding
    if (i === n) {
      amt = round2(balance - allocated);
    }

    allocated += amt;

    const row = frm.add_child("payment_plan");
    row.milestone = `${cycle} Installment ${i}/${n}`;
    row.due_date = due;
    row.amount = amt;
  }

  frm.refresh_field("payment_plan");
}

frappe.ui.form.on("Offer Letter", {
  payment_cycle: generateMilestones,
  schedule_start_date: generateMilestones,
  installments: generateMilestones,
  offer_price: generateMilestones,
  deposit_amount: generateMilestones,

  refresh(frm) {
    if (!frm.is_new()) {
      frm.add_custom_button("Generate Payment Plan", () => generateMilestones(frm));
    }
  },
});
