// Copyright (c) 2024, Bilal and contributors
// For license information, please see license.txt

frappe.ui.form.on("Rent Payment", {
	refresh(frm) {
        // Add the "Print Receipt" button
        frm.add_custom_button(__('Print Receipt'), function() {
            // Open the print view with the selected print format
            const print_format = 'Rent Payment'; // Replace with your print format name

            const print_url = frappe.urllib.get_full_url(`/printview?doctype=Rent Payment&name=${frm.doc.name}&trigger_print=1&format=${encodeURIComponent(print_format)}&no_letterhead=1`);

            // Open the print URL in a new tab
            window.open(print_url, '_blank');
        }); // Add the button under the "Actions" group
	},
});
