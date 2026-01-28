frappe.ui.form.on("Reservation", {
  refresh(frm) {
    if (!frm.is_new()) {
      frm.add_custom_button("Create Offer Letter", async () => {
        const r = await frappe.call({
          method: "re_crm_app.api.sales_flow.make_offer_letter",
          args: { reservation_name: frm.doc.name },
        });

        if (r.message) {
          frappe.set_route("Form", "Offer Letter", r.message);
        }
      });
    }
  },
});
