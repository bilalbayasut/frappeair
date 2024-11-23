# Copyright (c) 2024, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class FlightPassenger(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		date_of_birth: DF.Date
		first_name: DF.Data
		last_name: DF.Data | None
		name: DF.Int | None
	# end: auto-generated types

	@property
	def full_name(self):
		if self.first_name and self.last_name:
			return f"{self.first_name} {self.last_name}"
		elif self.first_name:  # Last name is missing
			return self.first_name
		elif self.last_name:  # First name is missing
			return self.last_name
		else:  # Both are missing
			return ""
		# return f"{self.first_name} {self.last_name}"
