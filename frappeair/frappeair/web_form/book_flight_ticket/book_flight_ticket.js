frappe.ready(function() {
	// bind events here
	
	frappe.web_form.on('flight', function(field, value) {
		// console.log(`${field} - ${value}`)
		if (value) {
			// Fetch the selected vehicle's details
			frappe.call({
				method: 'frappe.client.get',
				args: {
					doctype: 'Airplane Ticket',
					// name: value
					name: 'Airasia-002-11-24-LAX-SUB'
				},
				callback: function(r) {
					console.log(`got value ${JSON.stringify(r.message.flight_price)}`)
					if (r.message) {
						// Set the price field based on the airplane flight_price
						frappe.web_form.set_value('flight_price', r.message.flight_price);
					}
				}
			});
		} else {
			// Clear the price if no vehicle is selected
			frappe.web_form.set_value('flight_price', null);
		}
	});
})
