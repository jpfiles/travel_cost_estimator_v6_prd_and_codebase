from travel_model import create_travel_request
from datetime import datetime

def calculate_major_booking_total(major_bookings):
    """
    Calculate the total cost of all major bookings.

    Returns:
        Float representing the total booking cost.
    """

    booking_total = 0.00

    for booking in major_bookings.values():
        
        if booking["included"]:
            booking_total += booking["cost"]
            
    return booking_total

###############################################################################################################

def calculate_other_expense_total(other_expenses):
    """
    Calculate the total of all additional travel expenses.
    """

    other_total = 0.00

    for expense in other_expenses.values():

        if expense["included"]:
            other_total += expense["cost"]

    return other_total

###############################################################################################################

def calculate_grand_total(
    booking_total,
    other_total,
    per_diem_total
):
    """
    Calculate the estimated total trip cost.
    """

    grand_total = (
        booking_total
        + other_total
        + per_diem_total
    )

    return grand_total

###############################################################################################################

def calculate_per_diem(travel_request):
    """
    Calculate the number of travel days and the total per diem.

    The first and last travel days receive 75% of the daily rate.
    Every day between them receives 100% of the daily rate.

    The calculated values are stored in the travel request dictionary.
    """

    # Retrieve the dates stored in the traveler section.
    departure_date_string = travel_request["traveler"]["departure_date"]
    return_date_string = travel_request["traveler"]["return_date"]

    # Convert the date strings into datetime objects.
    departure_date = datetime.strptime(
        departure_date_string,
        "%m/%d/%Y"
    )

    return_date = datetime.strptime(
        return_date_string,
        "%m/%d/%Y"
    )

    # Calculate the number of days between the dates.
    # Add 1 so both the departure and return dates are counted.
    travel_days = (return_date - departure_date).days + 1

    # The application supports trips lasting at least two days.
    if travel_days < 2:
        raise ValueError("Travel must last at least two days.")

    # Retrieve the daily per diem rate from the model.
    daily_rate = travel_request["per_diem"]["daily_rate"]

    # The first and last days are travel-rate days.
    travel_rate_days = 2

    # Every day between the first and last is a full-rate day.
    full_rate_days = travel_days - travel_rate_days

    # Calculate the two per diem subtotals.
    full_rate_total = full_rate_days * daily_rate
    travel_rate_total = travel_rate_days * daily_rate * 0.75

    # Add both subtotals together.
    per_diem_total = full_rate_total + travel_rate_total

    # Store the calculated values back in the travel request.
    travel_request["per_diem"]["travel_days"] = travel_days
    travel_request["per_diem"]["full_rate_days"] = full_rate_days
    travel_request["per_diem"]["travel_rate_days"] = travel_rate_days
    travel_request["per_diem"]["total"] = per_diem_total

    return per_diem_total

###############################################################################################################

def calculate_trip_totals(travel_request):
    """
    Calculate all travel costs and store the results in the model.
    """

    booking_total = calculate_major_booking_total(
        travel_request["major_bookings"]
    )

    other_total = calculate_other_expense_total(
        travel_request["other_expenses"]
    )

    per_diem_total = calculate_per_diem(travel_request)

    grand_total = calculate_grand_total(
        booking_total,
        other_total,
        per_diem_total
    )

    travel_request["totals"]["major_bookings"] = booking_total
    travel_request["totals"]["other_expenses"] = other_total
    travel_request["totals"]["per_diem"] = per_diem_total
    travel_request["totals"]["grand_total"] = grand_total

    return grand_total

### TEMPORARY TEST BLOCK BELOW ###

if __name__ == "__main__":
    trip = create_travel_request()

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

    print(f"Major bookings: ${trip['totals']['major_bookings']:.2f}")
    print(f"Other expenses: ${trip['totals']['other_expenses']:.2f}")
    print(f"Per diem: ${trip['totals']['per_diem']:.2f}")
    print(f"Grand total: ${trip['totals']['grand_total']:.2f}")
