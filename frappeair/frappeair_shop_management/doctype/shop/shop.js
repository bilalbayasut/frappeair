// Copyright (c) 2024, Bilal and contributors
// For license information, please see license.txt

frappe.ui.form.on("Shop", {
	refresh(frm) {
        // Add a custom button to toggle status
        frm.add_custom_button(__('Mark as Available/Occupied'), function () {
            let new_status = frm.doc.status === 'Available' ? 'Occupied' : 'Available';

            // Confirm the action with the user
            frappe.confirm(
                `Are you sure you want to mark this shop as <b>${new_status}</b>?`,
                function () {
                    // Update the status
                    frm.set_value('status', new_status);
                    if (new_status == 'Available') {
                        frm.set_value('tenant',null)
                    }

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
    // // Update airport's shop count when shop status changes
    // status: function(frm) {
    //     if (frm.doc.airport) {
    //         frappe.call({
    //             method: 'frappe.client.get',
    //             args: {
    //                 doctype: 'Airport',
    //                 name: frm.doc.airport
    //             },
    //             callback: function(r) {
    //                 if (r.message) {
    //                     let airport = r.message;
                        
    //                     // Recalculate total shops
    //                     frappe.call({
    //                         method: 'frappe.client.get_list',
    //                         args: {
    //                             doctype: 'Shop',
    //                             filters: {
    //                                 'airport': frm.doc.airport,
    //                                 // 'status': 'Available'
    //                             },
    //                             fields: ['name', 'status']
    //                         },
    //                         callback: function(res) {
    //                             const response = res.message
    //                             // update total shops
    //                             airport.total_shops = response.length;
    //                             frappe.model.set_value('Airport', airport.name, 'total_shops', airport.total_shops);
    //                             // update available shops
    //                             const availableCount = response.filter(response => response.status === "Available").length;
    //                             airport.available_shops = availableCount;
    //                             frappe.model.set_value('Airport', airport.name, 'available_shops', airport.available_shops);
    //                             console.log(`${airport.name} updated`)
    //                         }
    //                     });
    //                 }
    //             }
    //         });
    //     }
    // }
});
