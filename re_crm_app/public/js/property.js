frappe.ui.form.on("Property", {
  refresh(frm) {
    if (frm.is_new()) return;

    frm.add_custom_button("Generate Units", async () => {
      const r = await frappe.call({
        method: "re_crm_app.api.unit_generator.generate_units",
        args: { property_name: frm.doc.name },
      });
      const m = r.message || {};
      frappe.msgprint(`Units created: ${m.created || 0}<br>Skipped: ${m.skipped || 0}`);
    });

    frm.add_custom_button("Regenerate Units (Safe)", async () => {
      frappe.confirm(
        "This will delete all units under this Property and recreate them from the Unit Plan.<br><br>" +
          "<b>It will be blocked if any unit is Reserved/Sold/Rented.</b><br><br>Proceed?",
        async () => {
          const r = await frappe.call({
            method: "re_crm_app.api.unit_generator.regenerate_units",
            args: { property_name: frm.doc.name, confirm: 1 },
          });
          const m = r.message || {};
          frappe.msgprint(`Regenerated. Units created: ${m.created || 0}, skipped: ${m.skipped || 0}`);
        }
      );
    });
  },
});
