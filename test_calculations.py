import unittest

from calculations import (
    calculate_grand_total,
    calculate_major_booking_total,
    calculate_other_expense_total,
    calculate_per_diem,
    calculate_trip_totals,
)
from travel_model import create_travel_request


class TestTravelCalculations(unittest.TestCase):

    def setUp(self):
        """Create a fresh travel request before every test."""
        self.trip = create_travel_request()

    def set_trip_dates(
        self,
        departure_date="07/10/2026",
        return_date="07/15/2026",
    ):
        """Add valid travel dates to the test trip."""
        self.trip["traveler"]["departure_date"] = departure_date
        self.trip["traveler"]["return_date"] = return_date

    def test_major_booking_total_includes_selected_bookings(self):
        self.trip["major_bookings"]["airfare"]["included"] = True
        self.trip["major_bookings"]["airfare"]["cost"] = 650.00

        self.trip["major_bookings"]["hotel"]["included"] = True
        self.trip["major_bookings"]["hotel"]["cost"] = 1200.00

        total = calculate_major_booking_total(
            self.trip["major_bookings"]
        )

        self.assertEqual(total, 1850.00)

    def test_major_booking_total_ignores_excluded_bookings(self):
        self.trip["major_bookings"]["airfare"]["included"] = True
        self.trip["major_bookings"]["airfare"]["cost"] = 650.00

        self.trip["major_bookings"]["hotel"]["included"] = False
        self.trip["major_bookings"]["hotel"]["cost"] = 1200.00

        total = calculate_major_booking_total(
            self.trip["major_bookings"]
        )

        self.assertEqual(total, 650.00)

    def test_other_expense_total_includes_selected_expenses(self):
        self.trip["other_expenses"]["airport_parking"]["included"] = True
        self.trip["other_expenses"]["airport_parking"]["cost"] = 90.00

        self.trip["other_expenses"]["baggage_fees"]["included"] = True
        self.trip["other_expenses"]["baggage_fees"]["cost"] = 70.00

        total = calculate_other_expense_total(
            self.trip["other_expenses"]
        )

        self.assertEqual(total, 160.00)

    def test_other_expense_total_ignores_excluded_expenses(self):
        self.trip["other_expenses"]["airport_parking"]["included"] = True
        self.trip["other_expenses"]["airport_parking"]["cost"] = 90.00

        self.trip["other_expenses"]["baggage_fees"]["included"] = False
        self.trip["other_expenses"]["baggage_fees"]["cost"] = 70.00

        total = calculate_other_expense_total(
            self.trip["other_expenses"]
        )

        self.assertEqual(total, 90.00)

    def test_grand_total_combines_all_subtotals(self):
        total = calculate_grand_total(
            booking_total=1850.00,
            other_total=90.00,
            per_diem_total=550.00,
        )

        self.assertEqual(total, 2490.00)

    def test_two_day_trip_uses_two_travel_rate_days(self):
        self.set_trip_dates(
            departure_date="07/10/2026",
            return_date="07/11/2026",
        )
        self.trip["per_diem"]["daily_rate"] = 100.00

        total = calculate_per_diem(self.trip)

        self.assertEqual(self.trip["per_diem"]["travel_days"], 2)
        self.assertEqual(self.trip["per_diem"]["full_rate_days"], 0)
        self.assertEqual(self.trip["per_diem"]["travel_rate_days"], 2)
        self.assertEqual(total, 150.00)

    def test_six_day_trip_calculates_per_diem(self):
        self.set_trip_dates()
        self.trip["per_diem"]["daily_rate"] = 100.00

        total = calculate_per_diem(self.trip)

        self.assertEqual(self.trip["per_diem"]["travel_days"], 6)
        self.assertEqual(self.trip["per_diem"]["full_rate_days"], 4)
        self.assertEqual(self.trip["per_diem"]["travel_rate_days"], 2)
        self.assertEqual(total, 550.00)
        self.assertEqual(self.trip["per_diem"]["total"], 550.00)

    def test_trip_totals_are_stored_in_travel_request(self):
        self.set_trip_dates()
        self.trip["per_diem"]["daily_rate"] = 100.00

        self.trip["major_bookings"]["airfare"]["included"] = True
        self.trip["major_bookings"]["airfare"]["cost"] = 650.00

        self.trip["major_bookings"]["hotel"]["included"] = True
        self.trip["major_bookings"]["hotel"]["cost"] = 1200.00

        self.trip["other_expenses"]["airport_parking"]["included"] = True
        self.trip["other_expenses"]["airport_parking"]["cost"] = 90.00

        returned_total = calculate_trip_totals(self.trip)

        self.assertEqual(
            self.trip["totals"]["major_bookings"],
            1850.00,
        )
        self.assertEqual(
            self.trip["totals"]["other_expenses"],
            90.00,
        )
        self.assertEqual(
            self.trip["totals"]["per_diem"],
            550.00,
        )
        self.assertEqual(
            self.trip["totals"]["grand_total"],
            2490.00,
        )
        self.assertEqual(returned_total, 2490.00)

    def test_same_day_trip_is_rejected(self):
        self.set_trip_dates(
            departure_date="07/10/2026",
            return_date="07/10/2026",
        )
        self.trip["per_diem"]["daily_rate"] = 100.00

        with self.assertRaisesRegex(
            ValueError,
            "at least two days",
        ):
            calculate_per_diem(self.trip)

    def test_return_date_before_departure_date_is_rejected(self):
        self.set_trip_dates(
            departure_date="07/15/2026",
            return_date="07/10/2026",
        )
        self.trip["per_diem"]["daily_rate"] = 100.00

        with self.assertRaisesRegex(
            ValueError,
            "Return date must be after departure date",
        ):
            calculate_per_diem(self.trip)

    def test_invalid_date_format_is_rejected(self):
        self.set_trip_dates(
            departure_date="2026-07-10",
            return_date="2026-07-15",
        )
        self.trip["per_diem"]["daily_rate"] = 100.00

        with self.assertRaisesRegex(
            ValueError,
            "MM/DD/YYYY",
        ):
            calculate_per_diem(self.trip)

    def test_missing_dates_are_rejected(self):
        self.trip["per_diem"]["daily_rate"] = 100.00

        with self.assertRaisesRegex(
            ValueError,
            "Departure and return dates are required",
        ):
            calculate_per_diem(self.trip)

    def test_negative_per_diem_rate_is_rejected(self):
        self.set_trip_dates()
        self.trip["per_diem"]["daily_rate"] = -100.00

        with self.assertRaisesRegex(
            ValueError,
            "Per diem rate cannot be negative",
        ):
            calculate_per_diem(self.trip)

    def test_negative_included_booking_cost_is_rejected(self):
        self.trip["major_bookings"]["airfare"]["included"] = True
        self.trip["major_bookings"]["airfare"]["cost"] = -650.00

        with self.assertRaisesRegex(
            ValueError,
            "Booking cost cannot be negative",
        ):
            calculate_major_booking_total(
                self.trip["major_bookings"]
            )

    def test_negative_included_expense_cost_is_rejected(self):
        self.trip["other_expenses"]["airport_parking"]["included"] = True
        self.trip["other_expenses"]["airport_parking"]["cost"] = -90.00

        with self.assertRaisesRegex(
            ValueError,
            "Expense cost cannot be negative",
        ):
            calculate_other_expense_total(
                self.trip["other_expenses"]
            )

    def test_currency_totals_are_rounded_to_two_decimal_places(self):
        total = calculate_grand_total(
            booking_total=0.10,
            other_total=0.20,
            per_diem_total=0.00,
        )

        self.assertEqual(total, 0.30)


if __name__ == "__main__":
    unittest.main()