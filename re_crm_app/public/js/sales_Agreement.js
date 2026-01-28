frappe.ui.form.on("Sales Agreement", {
  refresh(frm) {
    if (!frm.is_new()) {
      frm.add_custom_button("Generate Invoices", async () => {
        const r = await frappe.call({
          method: "re_crm_app.api.sales_flow.generate_invoices_from_schedule",
          args: { agreement_name: frm.doc.name },
        });

        const created = r.message || [];
        if (!created.length) {
          frappe.msgprint("No invoices created (either no schedule or already invoiced).");
          return;
        }
        frappe.msgprint(`Created invoices: ${created.join(", ")}`);
        frm.reload_doc();
      });
    }
  },
});
