from re_crm_app.utils.property_stats import update_property_counters

def unit_on_update(doc, method=None):
    update_property_counters(doc.property)

def unit_on_trash(doc, method=None):
    update_property_counters(doc.property)
