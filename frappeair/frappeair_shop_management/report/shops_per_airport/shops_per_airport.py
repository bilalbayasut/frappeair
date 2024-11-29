# Copyright (c) 2024, Ambibuzz and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns = [
        {
            "fieldname": "airport",
            "label": "Airport",
            "fieldtype": "Link",
            "options": "Airport",
            "width": 150,
        },
        {
            "fieldname": "total_shops",
            "label": "Total Shops",
            "fieldtype": "Int",
            "width": 120,
        },
        {
            "fieldname": "available_shops",
            "label": "Available Shops",
            "fieldtype": "Int",
            "width": 120,
        },
        {
            "fieldname": "leased_shops",
            "label": "Leased Shops",
            "fieldtype": "Int",
            "width": 120,
        },
    ]

    # Query to fetch data grouped by airport
    data = frappe.db.sql(
        """
        SELECT
            s.airport AS airport,
            COUNT(s.name) AS total_shops,
            SUM(CASE WHEN s.status = 'Available' THEN 1 ELSE 0 END) AS available_shops,
            SUM(CASE WHEN s.status = 'Occupied' THEN 1 ELSE 0 END) AS leased_shops
        FROM `tabShop` s
        GROUP BY s.airport
    """,
        as_dict=True,
    )

    return columns, data
