# Copyright (c) 2024, Bilal and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Shop(Document):
    def on_update(self):
        self.update_shops_count()

    def after_insert(self):
        self.update_shops_count()

    def after_delete(self):
        self.update_shops_count()

    def update_shops_count(self):
        """Update airport shop counts after shop status changes."""
        if self.airport:
            # Get the airport document
            airport = frappe.get_doc("Airport", self.airport)

            # Get all shops linked to this airport
            shops = frappe.get_all(
                "Shop", filters={"airport": self.airport}, fields=["name", "status"]
            )

            # Update total shops count
            airport.total_shops = len(shops)

            # Update available shops count
            available_count = sum(1 for shop in shops if shop["status"] == "Available")
            airport.available_shops = available_count
            # Save the updated airport document
            airport.save()
            frappe.msgprint(f"{airport.name} shop counts updated.")
