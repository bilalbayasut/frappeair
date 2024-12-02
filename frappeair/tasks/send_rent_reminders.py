import frappe
from frappe.utils import nowdate


def send_rent_reminders():

    # Check if rent reminders are enabled in configuration
    config = frappe.get_doc("Shop Settings")
    if not config.enable_rent_reminders:
        return

    # Find active rent contracts due this month
    contracts = frappe.get_all(
        "Lease Contract",
        filters={"status": "Active", "contract_end_date": [">=", nowdate()]},
        fields=[
            "tenant",
            "shop",
            "contract_start_date",
            "contract_end_date",
            "rent_amount",
            "status",
        ],
    )
    print(f"we have {len(contracts)} contracts")
    for contract in contracts:
        # Fetch details like tenant, shop, rent amount, etc.
        tenant = frappe.get_doc("Tenant", contract.tenant)
        shop = frappe.get_doc("Shop", contract.shop)
        rent_amount = contract.rent_amount
        due_date = contract.contract_end_date
        # Compose the email message
        email_subject = f"Rent Payment Reminder for Shop {shop.shop_number}"
        email_message = f"""
        Dear {tenant.tenant_name},

        This is a reminder that the rent for your shop ({shop.shop_number} - {shop.shop_name}) is due on {due_date}.
        The rent amount is {frappe.format(rent_amount, 'Currency')}.
        
        Please make the payment to avoid late fees.
        
        Ignore this email if you have already made payment.

        Thank you,
        The Airport Authority
        """
        print(email_message)
        try:
            # Send the email
            frappe.sendmail(
                recipients=tenant.email, subject=email_subject, message=email_message
            )
        except Exception as e:
            print(e)
