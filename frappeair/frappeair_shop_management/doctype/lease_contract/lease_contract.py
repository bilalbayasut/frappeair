# Copyright (c) 2024, Bilal and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import nowdate
from frappe.model.document import Document


class LeaseContract(Document):
    def validate(self):
        # Update the Shop status and tenant when the Lease Contract is saved
        if self.shop:
            update_shop_status(self.shop)

    def after_insert(self):
        # Automatically create Rent Payment entries for the Lease Contract
        create_rent_payments(self)

    def on_trash(self):
        # Update the Shop status and tenant when the Lease Contract is deleted
        if self.shop:
            update_shop_status(self.shop)

        # Delete associated Rent Payment entries when the Lease Contract is deleted
        delete_rent_payments(self)


def update_shop_status(shop_name):
    # Fetch all related Lease Contracts for the shop
    lease_contracts = frappe.get_all(
        "Lease Contract",
        filters={"shop": shop_name},
        fields=["tenant", "status", "contract_start_date", "contract_end_date"],
        order_by="contract_end_date desc",  # Sort by end date to get the latest contract
    )

    shop = frappe.get_doc("Shop", shop_name)

    if lease_contracts:
        latest_contract = lease_contracts[0]

        # Check if the latest contract is Active or Expired
        if latest_contract["status"] in ["Active", "Expired"]:
            shop.tenant = latest_contract["tenant"]
            shop.status = "Occupied"
        else:  # If the latest contract is Terminated
            shop.tenant = None
            shop.status = "Available"
    else:
        # No contracts exist for this shop
        shop.tenant = None
        shop.status = "Available"

    shop.save()


def create_rent_payments(lease_contract):
    # Fetch the global default rent amount
    default_rent_amount = lease_contract.rent_amount or frappe.db.get_single_value(
        "Shop Settings", "default_rent_amount"
    )

    # Generate rent payments for each month within the contract period
    from dateutil.relativedelta import relativedelta
    from datetime import datetime

    start_date = lease_contract.contract_start_date
    end_date = lease_contract.contract_end_date

    current_date = start_date

    # Ensure current_date is a datetime object
    current_date = datetime.strptime(
        start_date, "%Y-%m-%d"
    )  # Convert start_date to datetime
    end_date = datetime.strptime(end_date, "%Y-%m-%d")  # Convert end_date to datetime

    while current_date <= end_date:
        # Create a Rent Payment for the current month
        rent_payment = frappe.get_doc(
            {
                "doctype": "Rent Payment",
                "lease_contract": lease_contract.name,
                # "tenant": lease_contract.tenant,
                "rent_amount_paid": default_rent_amount,
                "due_date": current_date.strftime("%Y-%m-%d"),
            }
        )
        rent_payment.insert()
        current_date += relativedelta(months=1)  # Increment by one month


def delete_rent_payments(lease_contract):
    # Delete all Rent Payment entries linked to the Lease Contract
    frappe.db.delete("Rent Payment", {"lease_contract": lease_contract.name})
