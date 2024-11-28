# Copyright (c) 2024, Bilal and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import nowdate
from frappe.model.document import Document


class LeaseContract(Document):
	def save(self):
		if not self.status:  # If the status is not set, set it
			self.status = 'Due'

		if self.contract_end_date < nowdate():
			if self.status != 'Paid':  # Check if it's overdue and not paid
				self.status = 'Overdue'
		elif self.contract_start_date <= nowdate() <= self.contract_end_date:
			if self.status != 'Paid':  # Check if the lease is active and rent is not paid yet
				self.status = 'Due'



def update_lease_contract_status(doc, method):
    # Ensure that the status is only updated automatically
    if not doc.status:  # If the status is not set, set it
        doc.status = 'Due'

    if doc.contract_end_date < nowdate():
        if doc.status != 'Paid':  # Check if it's overdue and not paid
            doc.status = 'Overdue'
    elif doc.contract_start_date <= nowdate() <= doc.contract_end_date:
        if doc.status != 'Paid':  # Check if the lease is active and rent is not paid yet
            doc.status = 'Due'

# Hook this logic into the Lease Contract Doctype (in hooks.py)
def on_update(doc, method):
    update_lease_contract_status(doc, method)
