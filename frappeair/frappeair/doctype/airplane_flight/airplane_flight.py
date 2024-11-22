# Copyright (c) 2024, Bilal and contributors
# For license information, please see license.txt

# import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):
	def on_submit(self):
		self.status = "Completed"

	def before_validate(self):
		if not self.route:
			self.route = f"airplane-flights/{self.name}"
		# if self.status == "Scheduled":
		# 	self.is_published = True