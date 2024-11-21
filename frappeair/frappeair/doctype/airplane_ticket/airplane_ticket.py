# Copyright (c) 2024, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _

class AirplaneTicket(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	def validate_unique_add_ons(self):
		add_on_names = set()  # Set to store unique add-ons
		for row in self.add_ons:  # Assuming "add_ons" is the child table fieldname
			if row.airplane_ticket_add_on_type in add_on_names:
				frappe.throw(_("Duplicate Add-on: {0}").format(row.airplane_ticket_add_on_type))
			add_on_names.add(row.airplane_ticket_add_on_type)

	def validate(self):
		self.validate_unique_add_ons()

	
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
	
	def before_submit(self):
		self.calculate_total_amount()
	# end: auto-generated types
	def calculate_total_amount(self):
		# self.total_amount = self.total_amount + self.flight_price
		self.total_amount = self.flight_price + sum(add_on.price for add_on in self.add_ons)
