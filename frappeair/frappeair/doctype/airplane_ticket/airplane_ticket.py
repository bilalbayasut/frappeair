# Copyright (c) 2024, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _

class AirplaneTicket(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.
	from typing import TYPE_CHECKING
	if TYPE_CHECKING:
		from frappe.types import DF

		amended_from: DF.Link | None
		departure_date: DF.Date
		departure_time: DF.Time
		destination_airport: DF.Link
		destination_airport_code: DF.Data | None
		duration_of_flight: DF.Duration
		flight: DF.Link
		passenger: DF.Link
		source_airport: DF.Link
		source_airport_code: DF.Data | None
		status: DF.Literal["Booked", "Checked-In", "Boarded"]

	def validate_unique_add_ons(self):
		 # Check for duplicate add-ons
			unique_add_ons = []
			seen_add_ons = set()

			for add_on in self.add_ons:
				if add_on.airplane_ticket_add_on_type in seen_add_ons:
					# Log the duplicate for debugging
					frappe.msgprint(
						_("Duplicate Add-on '{0}' found and removed.").format(add_on.airplane_ticket_add_on_type),
						alert=True,
					)
				else:
					seen_add_ons.add(add_on.airplane_ticket_add_on_type)
					unique_add_ons.append(add_on)

			# Overwrite the child table with only unique rows
			self.add_ons = unique_add_ons
	
	# end: auto-generated types
	def calculate_total_amount(self):
		total_amount = self.flight_price + sum(add_on.amount for add_on in self.add_ons)
		print(f"setting total_amount {total_amount}")
		self.total_amount = total_amount
	
	def validate(self):
		self.validate_unique_add_ons()
	
	def before_save(self):
		self.calculate_total_amount()
