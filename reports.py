def generate_text_report(travel_request):
    """
    Generate a formatted text report from a travel request.

    Args:
        travel_request: The completed travel request dictionary.

    Returns:
        A formatted string containing the travel cost report.
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
    report_lines.append(f"Traveler: {traveler['name']}")
    report_lines.append(f"Destination: {traveler['destination']}")
    report_lines.append(f"Departure Date: {traveler['departure_date']}")
    report_lines.append(f"Return Date: {traveler['return_date']}")
    report_lines.append("")

    report_lines.append("MAJOR BOOKINGS")
    report_lines.append("-" * 50)

    for booking in major_bookings.values():
        if booking["included"]:
            report_lines.append(
                f"{booking['display_name']}: ${booking['cost']:.2f}"
            )

    report_lines.append(
        f"Major Bookings Total: ${totals['major_bookings']:.2f}"
    )
    report_lines.append("")

    report_lines.append("OTHER EXPENSES")
    report_lines.append("-" * 50)

    for expense in other_expenses.values():
        if expense["included"]:
            report_lines.append(
                f"{expense['display_name']}: ${expense['cost']:.2f}"
            )

    report_lines.append(
        f"Other Expenses Total: ${totals['other_expenses']:.2f}"
    )
    report_lines.append("")

    report_lines.append("PER DIEM")
    report_lines.append("-" * 50)
    report_lines.append(
        f"Daily Rate: ${per_diem['daily_rate']:.2f}"
    )
    report_lines.append(
        f"Travel Days: {per_diem['travel_days']}"
    )
    report_lines.append(
        f"Full-Rate Days: {per_diem['full_rate_days']}"
    )
    report_lines.append(
        f"Travel-Rate Days: {per_diem['travel_rate_days']}"
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

### TEMPORARY TEST BLOCK BELOW ###

if __name__ == "__main__":
    from travel_model import create_travel_request
    from calculations import calculate_trip_totals

    trip = create_travel_request()

    trip["traveler"]["name"] = "Jonah Pickens"
    trip["traveler"]["destination"] = "Honolulu, Hawaii"
    trip["traveler"]["departure_date"] = "07/10/2026"
    trip["traveler"]["return_date"] = "07/15/2026"

    trip["major_bookings"]["airfare"]["included"] = True
    trip["major_bookings"]["airfare"]["cost"] = 650.00

    trip["major_bookings"]["hotel"]["included"] = True
    trip["major_bookings"]["hotel"]["cost"] = 1200.00

    trip["other_expenses"]["airport_parking"]["included"] = True
    trip["other_expenses"]["airport_parking"]["cost"] = 90.00

    trip["per_diem"]["daily_rate"] = 100.00

    calculate_trip_totals(trip)

    report = generate_text_report(trip)

    print(report)