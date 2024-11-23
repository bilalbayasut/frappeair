// Copyright (c) 2024, Frappe Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airline", {
	refresh(frm) {
        if (frm.doc.website) {
            frm.add_custom_button('Visit Website', function () {
                window.open(frm.doc.website, '_blank');
            }).addClass('btn-primary');
        }
	},
});
