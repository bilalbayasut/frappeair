// Copyright (c) 2024, Bilal and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
	// Trigger when the form is refreshed or loaded
    refresh: function (frm) {
        calculate_total_amount(frm);
        assign_seat_number(frm);
    },

    // Trigger when flight_price is updated
    flight_price: function (frm) {
        calculate_total_amount(frm);
    }
});
// Function to calculate total amount
function calculate_total_amount(frm) {
    // Calculate the total amount from flight_price and add_ons
    let total_amount = frm.doc.flight_price || 0;

    if (frm.doc.add_ons) {
        total_amount += frm.doc.add_ons.reduce((sum, add_on) => {
            return sum + (add_on.amount || 0);
        }, 0);
    }

    // Set the calculated total_amount
    frm.set_value('total_amount', total_amount);

    // Optional: Provide real-time feedback to the user
    frappe.show_alert({
        title: __('Total Amount Updated'),
        message: __('The total amount has been recalculated to {0}', [total_amount]),
        indicator: 'blue',
    });
}

function assign_seat_number(frm) {
    // Ensure "Actions" dropdown exists
    if (!frm.page.actions_btn_group) {
        frm.page.add_action_icon_group();
    }

    // Add a custom button under the Actions dropdown
    frm.page.add_action_item('Set Seat Number', function () {
        // Create a dialog to input the seat number
        const dialog = new frappe.ui.Dialog({
            title: 'Set Seat Number',
            fields: [
                {
                    label: 'Seat Number',
                    fieldname: 'seat',
                    fieldtype: 'Data',
                    reqd: 1, // Make the field required
                },
            ],
            primary_action_label: 'Set Seat',
            primary_action(values) {
                // Set the seat number to the Seat field in the form
                if (values.seat) {
                    frm.set_value('seat', values.seat);
                    dialog.hide(); // Close the dialog after setting the value
                } else {
                    frappe.msgprint(__('Please enter a seat number.'));
                }
            },
        });

        // Show the dialog
        dialog.show();
    });
}

frappe.ui.form.on('Airplane Ticket Add-on Item', {
    validate: function (frm) {
        console.log(`validated ${frm}`);
    },
    airplane_ticket_add_on_type: function(frm, cdt, cdn) {
        console.log(`item ${cdt} ${cdn}`)
        const child = locals[cdt][cdn];
        const add_ons = frm.doc.add_ons || [];

        // Check for duplicate add-ons
        const duplicate = add_ons.filter(row => row.airplane_ticket_add_on_type === child.airplane_ticket_add_on_type && row.name !== child.name);

        if (duplicate.length > 0) {
            // Clear the field and show a user-friendly message
            frappe.msgprint({
                title: __('Duplicate Add-on'),
                message: __('The add-on "{0}" has already been added. Please choose a different add-on.', [child.airplane_ticket_add_on_type]),
                indicator: 'orange'
            });

            frappe.model.set_value(cdt, cdn, 'airplane_ticket_add_on_type', null); // Clear the value
        }
    },
    amount: function(frm, cdt, cdn){
        calculate_total_amount(frm)
    },
    // Trigger when add_ons child table is modified
    add_ons_add: function (frm) {
        calculate_total_amount(frm);
    },
    add_ons_remove: function (frm) {
        calculate_total_amount(frm);
    },
    add_ons: function (frm) {
        calculate_total_amount(frm);
    },
});

