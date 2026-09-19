from datetime import datetime
from math import isfinite


DATE_FORMAT = "%m/%d/%Y"


def validate_non_negative_number(value, field_name):
    """
    Validate that a monetary value is a finite, non-negative number.

    Args:
        value: The value being validated.
        field_name: User-friendly field name for error messages.

    Returns:
        The value converted to a float.

    Raises:
        ValueError: If the value is not a valid non-negative number.
    """

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field_name} must be a number.")

    if not isfinite(value):
        raise ValueError(f"{field_name} must be a finite number.")

    if value < 0:
        raise ValueError(f"{field_name} cannot be negative.")

    return float(value)


def calculate_major_booking_total(major_bookings):
    """
    Calculate the total cost of all included major bookings.

    Args:
        major_bookings: Dictionary containing the major bookings.

    Returns:
        The rounded total booking cost.

    Raises:
        ValueError: If an included booking contains an invalid cost.
    """

    booking_total = 0.00

    for booking in major_bookings.values():
        if booking["included"]:
            cost = validate_non_negative_number(
                booking["cost"],
                "Booking cost",
            )
            booking_total += cost

    return round(booking_total, 2)


def calculate_other_expense_total(other_expenses):
    """
    Calculate the total cost of all included additional expenses.

    Args:
        other_expenses: Dictionary containing additional expenses.

    Returns:
        The rounded total of all included additional expenses.

    Raises:
        ValueError: If an included expense contains an invalid cost.
    """

    other_total = 0.00

    for expense in other_expenses.values():
        if expense["included"]:
            cost = validate_non_negative_number(
                expense["cost"],
                "Expense cost",
            )
            other_total += cost

    return round(other_total, 2)


def calculate_grand_total(
    booking_total,
    other_total,
    per_diem_total,
):
    """
    Calculate the estimated total trip cost.

    Args:
        booking_total: Total cost of major bookings.
        other_total: Total cost of other travel expenses.
        per_diem_total: Total per diem cost.

    Returns:
        The rounded estimated trip cost.
    """

    booking_total = validate_non_negative_number(
        booking_total,
        "Booking total",
    )
    other_total = validate_non_negative_number(
        other_total,
        "Other expense total",
    )
    per_diem_total = validate_non_negative_number(
        per_diem_total,
        "Per diem total",
    )

    grand_total = (
        booking_total
        + other_total
        + per_diem_total
    )

    return round(grand_total, 2)


def parse_travel_date(date_string):
    """
    Convert a travel-date string into a datetime object.

    Args:
        date_string: Date formatted as MM/DD/YYYY.

    Returns:
        A datetime object.

    Raises:
        ValueError: If the date is missing or incorrectly formatted.
    """

    try:
        return datetime.strptime(
            date_string,
            DATE_FORMAT,
        )
    except (TypeError, ValueError):
        raise ValueError(
            "Dates must use MM/DD/YYYY format."
        ) from None


def calculate_per_diem(travel_request):
    """
    Calculate trip length and per diem component totals.

    Meals and incidentals are calculated separately. The first
    and last travel days receive 75 percent of each component's
    daily rate. Every intervening day receives the full rate.

    Older projects containing only a combined daily_rate remain
    supported by treating that amount as meals with zero
    incidentals.

    Args:
        travel_request: Travel-request dictionary containing dates
            and per diem rates.

    Returns:
        The rounded combined per diem total.

    Raises:
        ValueError: If dates or rates are invalid.
    """

    departure_date_string = travel_request[
        "traveler"
    ]["departure_date"]

    return_date_string = travel_request[
        "traveler"
    ]["return_date"]

    if not departure_date_string or not return_date_string:
        raise ValueError(
            "Departure and return dates are required."
        )

    departure_date = parse_travel_date(
        departure_date_string
    )
    return_date = parse_travel_date(
        return_date_string
    )

    if return_date < departure_date:
        raise ValueError(
            "Return date must be after departure date."
        )

    travel_days = (
        return_date - departure_date
    ).days + 1

    if travel_days < 2:
        raise ValueError(
            "Travel must last at least two days."
        )

    per_diem = travel_request["per_diem"]

    meals_rate_value = per_diem.get(
        "meals_rate",
        0.00,
    )
    incidentals_rate_value = per_diem.get(
        "incidentals_rate",
        0.00,
    )
    legacy_daily_rate = per_diem.get(
        "daily_rate",
        0.00,
    )

    uses_legacy_combined_rate = (
        meals_rate_value == 0
        and incidentals_rate_value == 0
        and legacy_daily_rate != 0
    )

    if uses_legacy_combined_rate:
        meals_rate = validate_non_negative_number(
            legacy_daily_rate,
            "Per diem rate",
        )
        incidentals_rate = 0.00
    else:
        meals_rate = validate_non_negative_number(
            meals_rate_value,
            "Meals rate",
        )
        incidentals_rate = validate_non_negative_number(
            incidentals_rate_value,
            "Incidentals rate",
        )

    daily_rate = round(
        meals_rate + incidentals_rate,
        2,
    )

    travel_rate_days = 2
    full_rate_days = (
        travel_days - travel_rate_days
    )

    meals_full_rate_total = (
        full_rate_days * meals_rate
    )
    meals_travel_rate_total = (
        travel_rate_days
        * meals_rate
        * 0.75
    )
    meals_total = round(
        meals_full_rate_total
        + meals_travel_rate_total,
        2,
    )

    incidentals_full_rate_total = (
        full_rate_days * incidentals_rate
    )
    incidentals_travel_rate_total = (
        travel_rate_days
        * incidentals_rate
        * 0.75
    )
    incidentals_total = round(
        incidentals_full_rate_total
        + incidentals_travel_rate_total,
        2,
    )

    per_diem_total = round(
        meals_total + incidentals_total,
        2,
    )

    per_diem["meals_rate"] = meals_rate
    per_diem["incidentals_rate"] = (
        incidentals_rate
    )
    per_diem["daily_rate"] = daily_rate
    per_diem["travel_days"] = travel_days
    per_diem["full_rate_days"] = full_rate_days
    per_diem["travel_rate_days"] = (
        travel_rate_days
    )
    per_diem["meals_total"] = meals_total
    per_diem["incidentals_total"] = (
        incidentals_total
    )
    per_diem["total"] = per_diem_total

    return per_diem_total


def calculate_trip_totals(travel_request):
    """
    Calculate and store all travel-cost totals.

    Args:
        travel_request: Complete travel-request dictionary.

    Returns:
        The rounded grand total.
    """

    booking_total = calculate_major_booking_total(
        travel_request["major_bookings"]
    )

    other_total = calculate_other_expense_total(
        travel_request["other_expenses"]
    )

    per_diem_total = calculate_per_diem(
        travel_request
    )

    grand_total = calculate_grand_total(
        booking_total,
        other_total,
        per_diem_total,
    )

    travel_request["totals"]["major_bookings"] = (
        booking_total
    )
    travel_request["totals"]["other_expenses"] = (
        other_total
    )
    travel_request["totals"]["per_diem"] = (
        per_diem_total
    )
    travel_request["totals"]["grand_total"] = (
        grand_total
    )

    return grand_total