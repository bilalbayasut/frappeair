# Copyright (c) 2024, Bilal and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RentPayment(Document):
	def before_insert(doc, method):
		# Get shop settings
		shop_settings = frappe.get_single("Shop Settings")

		# Use default rent amount if not provided
		if not doc.rent_amount:
			doc.rent_amount = shop_settings.default_rent_amount
