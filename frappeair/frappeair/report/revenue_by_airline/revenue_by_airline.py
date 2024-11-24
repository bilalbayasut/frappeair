import frappe
from frappe import _

def execute(filters=None):
    # Define the columns
    columns = [
        {
            "fieldname": "airline",
            "label": _("Airline"),
            "fieldtype": "Data",  # Keeping it Data since we extract airline names from the flight field
            "width": 200,
        },
        {
            "fieldname": "revenue",
            "label": _("Revenue"),
            "fieldtype": "Currency",
            "width": 150,
        },
    ]

    # List of airlines (manually defined or fetched from your system)
    airlines = ["Airasia", "IndiGo", "Alaska Airlines"]  # Add all known airlines here

    # Prepare the revenue data
    data = []
    total_revenue = 0

    for airline in airlines:
        # Calculate total revenue for each airline using SQL query with LIKE
        revenue = frappe.db.sql(
            """
            SELECT SUM(flight_price) 
            FROM `tabAirplane Ticket` 
            WHERE flight LIKE %s
            """,
            f"{airline}%",  # Match flights starting with the airline name
        )[0][0] or 0

        total_revenue += revenue

        # Add to the data
        data.append({
            "airline": airline,
            "revenue": revenue,
        })

    # Append the total row
    data.append({
        "airline": _("Total"),
        "revenue": total_revenue,
    })

    # Add chart and summary
    chart = {
        "data": {
            "labels": [row["airline"] for row in data[:-1]],  # Exclude the total row from the chart
            "datasets": [{"values": [row["revenue"] for row in data[:-1]]}],
        },
        "type": "donut",
    }

    summary = [
        {"label": _("Total Revenue"), "value": frappe.utils.fmt_money(total_revenue)}
    ]

    return columns, data, None, chart, summary
