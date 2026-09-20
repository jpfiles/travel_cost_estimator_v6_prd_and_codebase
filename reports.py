import csv
from html import escape
from io import StringIO


def generate_text_report(travel_request):
    """
    Generate a formatted plain-text travel cost report.

    Args:
        travel_request: Completed travel-request dictionary.

    Returns:
        A formatted plain-text report.
    """

    traveler = travel_request["traveler"]
    major_bookings = travel_request["major_bookings"]
    other_expenses = travel_request["other_expenses"]
    per_diem = travel_request["per_diem"]
    totals = travel_request["totals"]

    report_lines = []

    report_lines.append("TRAVEL COST ESTIMATE")
    report_lines.append("=" * 50)
    report_lines.append("")

    report_lines.append("TRAVELER INFORMATION")
    report_lines.append("-" * 50)
    report_lines.append(
        f"Traveler: {traveler['name']}"
    )
    report_lines.append(
        f"Destination: {traveler['destination']}"
    )
    report_lines.append(
        f"Departure Date: {traveler['departure_date']}"
    )
    report_lines.append(
        f"Return Date: {traveler['return_date']}"
    )
    report_lines.append("")

    report_lines.append("MAJOR BOOKINGS")
    report_lines.append("-" * 50)

    for booking in major_bookings.values():
        if booking["included"]:
            report_lines.append(
                f"{booking['display_name']}: "
                f"${booking['cost']:.2f}"
            )

    report_lines.append(
        "Major Bookings Total: "
        f"${totals['major_bookings']:.2f}"
    )
    report_lines.append("")

    report_lines.append("OTHER EXPENSES")
    report_lines.append("-" * 50)

    for expense in other_expenses.values():
        if expense["included"]:
            report_lines.append(
                f"{expense['display_name']}: "
                f"${expense['cost']:.2f}"
            )

    report_lines.append(
        "Other Expenses Total: "
        f"${totals['other_expenses']:.2f}"
    )
    report_lines.append("")

    report_lines.append("PER DIEM")
    report_lines.append("-" * 50)
    report_lines.append(
        f"Meals Rate: ${per_diem['meals_rate']:.2f}"
    )
    report_lines.append(
        "Incidentals Rate: "
        f"${per_diem['incidentals_rate']:.2f}"
    )
    report_lines.append(
        "Combined M&IE Rate: "
        f"${per_diem['daily_rate']:.2f}"
    )
    report_lines.append(
        f"Travel Days: {per_diem['travel_days']}"
    )
    report_lines.append(
        f"Full-Rate Days: {per_diem['full_rate_days']}"
    )
    report_lines.append(
        "Travel-Rate Days (75%): "
        f"{per_diem['travel_rate_days']}"
    )
    report_lines.append(
        "Meals Subtotal: "
        f"${per_diem['meals_total']:.2f}"
    )
    report_lines.append(
        "Incidentals Subtotal: "
        f"${per_diem['incidentals_total']:.2f}"
    )
    report_lines.append(
        f"Per Diem Total: ${totals['per_diem']:.2f}"
    )
    report_lines.append("")

    report_lines.append("TOTAL ESTIMATED COST")
    report_lines.append("=" * 50)
    report_lines.append(
        f"${totals['grand_total']:.2f}"
    )

    return "\n".join(report_lines)


def generate_csv_report(travel_request):
    """
    Generate a CSV travel cost report.

    Args:
        travel_request: Completed travel-request dictionary.

    Returns:
        CSV-formatted report content as a string.
    """

    traveler = travel_request["traveler"]
    major_bookings = travel_request["major_bookings"]
    other_expenses = travel_request["other_expenses"]
    per_diem = travel_request["per_diem"]
    totals = travel_request["totals"]

    output = StringIO(newline="")
    writer = csv.writer(output)

    writer.writerow(
        [
            "Section",
            "Item",
            "Description",
            "Amount",
        ]
    )

    writer.writerow(
        [
            "Traveler Information",
            "Traveler",
            traveler["name"],
            "",
        ]
    )
    writer.writerow(
        [
            "Traveler Information",
            "Destination",
            traveler["destination"],
            "",
        ]
    )
    writer.writerow(
        [
            "Traveler Information",
            "Departure Date",
            traveler["departure_date"],
            "",
        ]
    )
    writer.writerow(
        [
            "Traveler Information",
            "Return Date",
            traveler["return_date"],
            "",
        ]
    )

    for booking in major_bookings.values():
        if booking["included"]:
            writer.writerow(
                [
                    "Major Bookings",
                    booking["display_name"],
                    booking["description"],
                    f"{booking['cost']:.2f}",
                ]
            )

    for expense in other_expenses.values():
        if expense["included"]:
            writer.writerow(
                [
                    "Other Expenses",
                    expense["display_name"],
                    "",
                    f"{expense['cost']:.2f}",
                ]
            )

    writer.writerow(
        [
            "Per Diem",
            "Meals Rate",
            "",
            f"{per_diem['meals_rate']:.2f}",
        ]
    )
    writer.writerow(
        [
            "Per Diem",
            "Incidentals Rate",
            "",
            f"{per_diem['incidentals_rate']:.2f}",
        ]
    )
    writer.writerow(
        [
            "Per Diem",
            "Combined M&IE Rate",
            "",
            f"{per_diem['daily_rate']:.2f}",
        ]
    )
    writer.writerow(
        [
            "Per Diem",
            "Travel Days",
            "",
            str(per_diem["travel_days"]),
        ]
    )
    writer.writerow(
        [
            "Per Diem",
            "Full-Rate Days",
            "",
            str(per_diem["full_rate_days"]),
        ]
    )
    writer.writerow(
        [
            "Per Diem",
            "Travel-Rate Days (75%)",
            "",
            str(per_diem["travel_rate_days"]),
        ]
    )
    writer.writerow(
        [
            "Per Diem",
            "Meals Subtotal",
            "",
            f"{per_diem['meals_total']:.2f}",
        ]
    )
    writer.writerow(
        [
            "Per Diem",
            "Incidentals Subtotal",
            "",
            f"{per_diem['incidentals_total']:.2f}",
        ]
    )

    writer.writerow(
        [
            "Totals",
            "Major Bookings Total",
            "",
            f"{totals['major_bookings']:.2f}",
        ]
    )
    writer.writerow(
        [
            "Totals",
            "Other Expenses Total",
            "",
            f"{totals['other_expenses']:.2f}",
        ]
    )
    writer.writerow(
        [
            "Totals",
            "Per Diem Total",
            "",
            f"{totals['per_diem']:.2f}",
        ]
    )
    writer.writerow(
        [
            "Totals",
            "Grand Total",
            "",
            f"{totals['grand_total']:.2f}",
        ]
    )

    return output.getvalue()


def generate_html_report(travel_request):
    """
    Generate a complete HTML travel cost report.

    User-provided text is HTML-escaped before it is inserted into
    the document.

    Args:
        travel_request: Completed travel-request dictionary.

    Returns:
        A complete HTML document as a string.
    """

    traveler = travel_request["traveler"]
    major_bookings = travel_request["major_bookings"]
    other_expenses = travel_request["other_expenses"]
    per_diem = travel_request["per_diem"]
    totals = travel_request["totals"]

    html_lines = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '    <meta charset="UTF-8">',
        (
            '    <meta name="viewport" '
            'content="width=device-width, initial-scale=1.0">'
        ),
        "    <title>Travel Cost Estimate</title>",
        "    <style>",
        "        body {",
        (
            "            font-family: Arial, Helvetica, "
            "sans-serif;"
        ),
        "            max-width: 900px;",
        "            margin: 40px auto;",
        "            padding: 0 24px;",
        "            color: #222222;",
        "            line-height: 1.5;",
        "        }",
        "        h1 {",
        "            color: #1f4e78;",
        "            margin-bottom: 8px;",
        "        }",
        "        h2 {",
        "            margin-top: 32px;",
        "            color: #1f4e78;",
        "        }",
        "        table {",
        "            width: 100%;",
        "            border-collapse: collapse;",
        "            margin-top: 12px;",
        "        }",
        "        th, td {",
        "            border: 1px solid #d9d9d9;",
        "            padding: 10px 12px;",
        "            text-align: left;",
        "        }",
        "        th {",
        "            background-color: #1f4e78;",
        "            color: white;",
        "        }",
        "        td.amount {",
        "            text-align: right;",
        "            white-space: nowrap;",
        "        }",
        "        tr.grand-total {",
        "            font-weight: bold;",
        "            background-color: #eaf2f8;",
        "        }",
        "    </style>",
        "</head>",
        "<body>",
        "    <h1>Travel Cost Estimate</h1>",
        "    <h2>Traveler Information</h2>",
        (
            "    <p><strong>Traveler:</strong> "
            f"{escape(str(traveler['name']))}</p>"
        ),
        (
            "    <p><strong>Destination:</strong> "
            f"{escape(str(traveler['destination']))}</p>"
        ),
        (
            "    <p><strong>Departure Date:</strong> "
            f"{escape(str(traveler['departure_date']))}</p>"
        ),
        (
            "    <p><strong>Return Date:</strong> "
            f"{escape(str(traveler['return_date']))}</p>"
        ),
        "    <h2>Major Bookings</h2>",
        "    <table>",
        "        <thead>",
        (
            "            <tr><th>Item</th>"
            "<th>Description</th><th>Amount</th></tr>"
        ),
        "        </thead>",
        "        <tbody>",
    ]

    included_bookings = [
        booking
        for booking in major_bookings.values()
        if booking["included"]
    ]

    if included_bookings:
        for booking in included_bookings:
            html_lines.append(
                "            <tr>"
                f"<td>{escape(str(booking['display_name']))}</td>"
                f"<td>{escape(str(booking['description']))}</td>"
                '<td class="amount">'
                f"${booking['cost']:.2f}</td>"
                "</tr>"
            )
    else:
        html_lines.append(
            '            <tr><td colspan="3">'
            "No major bookings selected.</td></tr>"
        )

    html_lines.extend(
        [
            "            <tr>",
            (
                '                <td colspan="2">'
                "<strong>Major Bookings Total</strong></td>"
            ),
            (
                '                <td class="amount">'
                f"<strong>${totals['major_bookings']:.2f}"
                "</strong></td>"
            ),
            "            </tr>",
            "        </tbody>",
            "    </table>",
            "    <h2>Other Expenses</h2>",
            "    <table>",
            "        <thead>",
            (
                "            <tr><th>Item</th>"
                "<th>Amount</th></tr>"
            ),
            "        </thead>",
            "        <tbody>",
        ]
    )

    included_expenses = [
        expense
        for expense in other_expenses.values()
        if expense["included"]
    ]

    if included_expenses:
        for expense in included_expenses:
            html_lines.append(
                "            <tr>"
                f"<td>{escape(str(expense['display_name']))}</td>"
                '<td class="amount">'
                f"${expense['cost']:.2f}</td>"
                "</tr>"
            )
    else:
        html_lines.append(
            '            <tr><td colspan="2">'
            "No other expenses selected.</td></tr>"
        )

    html_lines.extend(
        [
            "            <tr>",
            (
                "                <td>"
                "<strong>Other Expenses Total</strong></td>"
            ),
            (
                '                <td class="amount">'
                f"<strong>${totals['other_expenses']:.2f}"
                "</strong></td>"
            ),
            "            </tr>",
            "        </tbody>",
            "    </table>",
            "    <h2>Per Diem</h2>",
            "    <table>",
            "        <tbody>",
            (
                "            <tr><td>Meals Rate</td>"
                '<td class="amount">'
                f"${per_diem['meals_rate']:.2f}</td></tr>"
            ),
            (
                "            <tr><td>Incidentals Rate</td>"
                '<td class="amount">'
                f"${per_diem['incidentals_rate']:.2f}</td></tr>"
            ),
            (
                "            <tr><td>Combined M&amp;IE Rate</td>"
                '<td class="amount">'
                f"${per_diem['daily_rate']:.2f}</td></tr>"
            ),
            (
                "            <tr><td>Travel Days</td>"
                '<td class="amount">'
                f"{per_diem['travel_days']}</td></tr>"
            ),
            (
                "            <tr><td>Full-Rate Days</td>"
                '<td class="amount">'
                f"{per_diem['full_rate_days']}</td></tr>"
            ),
            (
                "            <tr><td>Travel-Rate Days (75%)</td>"
                '<td class="amount">'
                f"{per_diem['travel_rate_days']}</td></tr>"
            ),
            (
                "            <tr><td>Meals Subtotal</td>"
                '<td class="amount">'
                f"${per_diem['meals_total']:.2f}</td></tr>"
            ),
            (
                "            <tr><td>Incidentals Subtotal</td>"
                '<td class="amount">'
                f"${per_diem['incidentals_total']:.2f}</td></tr>"
            ),
            (
                "            <tr><td>"
                "<strong>Per Diem Total</strong></td>"
                '<td class="amount">'
                f"<strong>${totals['per_diem']:.2f}"
                "</strong></td></tr>"
            ),
            "        </tbody>",
            "    </table>",
            "    <h2>Estimated Total</h2>",
            "    <table>",
            "        <tbody>",
            '            <tr class="grand-total">',
            "                <td>Grand Total</td>",
            (
                '                <td class="amount">'
                f"${totals['grand_total']:.2f}</td>"
            ),
            "            </tr>",
            "        </tbody>",
            "    </table>",
            "</body>",
            "</html>",
        ]
    )

    return "\n".join(html_lines)