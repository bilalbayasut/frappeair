# Copyright (c) 2024, Bilal and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):
	def on_submit(self):
		self.status = "Completed"

	def before_validate(self):
		if not self.route:
			self.route = f"airplane-flights/{self.name}"
	

def update_tickets_gate(doc, method):
    """
    Update the Gate Number of all tickets related to the flight.
    """
    if doc.gate_number:  # Ensure a valid gate number is set
        # Fetch all tickets related to this flight
        tickets = frappe.get_all(
            "Airplane Ticket",
            filters={"flight": doc.name},
            fields=["name", "gate_number"]
        )

        for ticket in tickets:
            # Update the Gate Number for each ticket
            if ticket.gate_number != doc.gate_number:
                frappe.db.set_value(
                    "Airplane Ticket",
                    ticket["name"],
                    "gate_number",
                    doc.gate_number
                )

        frappe.msgprint(f"Updated Gate Number for {len(tickets)} tickets.")