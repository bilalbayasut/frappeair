import frappe


def get_context(context):
    # Query the shops with status "Available"
    available_shops = frappe.get_all(
        "Shop", filters={"status": "Available"}, fields=["name", "shop_number"]
    )

    # Make the available_shops variable accessible in the template
    context.available_shops = available_shops
    return context
