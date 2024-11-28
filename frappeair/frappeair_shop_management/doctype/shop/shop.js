// Copyright (c) 2024, Bilal and contributors
// For license information, please see license.txt

frappe.ui.form.on("Shop", {
	refresh(frm) {
        // Add a custom button to toggle status
        frm.add_custom_button(__('Mark as Available/Leased'), function () {
            let new_status = frm.doc.status === 'Available' ? 'Leased' : 'Available';

            // Confirm the action with the user
            frappe.confirm(
                `Are you sure you want to mark this shop as <b>${new_status}</b>?`,
                function () {
                    // Update the status
                    frm.set_value('status', new_status);

                    // Save the document
                    frm.save()
                        .then(() => {
                            frappe.msgprint(`Shop has been marked as <b>${new_status}</b>.`);
                        })
                        .catch((error) => {
                            console.error(error);
                            frappe.msgprint('An error occurred while updating the status.');
                        });
                }
            );
        });
	},
});
