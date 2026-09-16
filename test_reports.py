import copy
import unittest

from calculations import calculate_trip_totals
from reports import generate_text_report
from travel_model import create_travel_request


class TestTextReportGeneration(unittest.TestCase):

    def setUp(self):
        """Create and calculate a representative travel request."""
        self.trip = create_travel_request()

        self.trip["traveler"]["name"] = "Jonah Pickens"
        self.trip["traveler"]["destination"] = "Honolulu, Hawaii"
        self.trip["traveler"]["departure_date"] = "07/10/2026"
        self.trip["traveler"]["return_date"] = "07/15/2026"

        self.trip["major_bookings"]["airfare"]["included"] = True
        self.trip["major_bookings"]["airfare"]["cost"] = 650.00

        self.trip["major_bookings"]["hotel"]["included"] = True
        self.trip["major_bookings"]["hotel"]["cost"] = 1200.00

        self.trip["major_bookings"]["rental_car"]["included"] = False
        self.trip["major_bookings"]["rental_car"]["cost"] = 800.00

        self.trip[
            "other_expenses"
        ]["airport_parking"]["included"] = True

        self.trip[
            "other_expenses"
        ]["airport_parking"]["cost"] = 90.00

        self.trip[
            "other_expenses"
        ]["baggage_fees"]["included"] = False

        self.trip[
            "other_expenses"
        ]["baggage_fees"]["cost"] = 70.00

        self.trip["per_diem"]["daily_rate"] = 100.00

        calculate_trip_totals(self.trip)

    def test_generate_text_report_returns_string(self):
        report = generate_text_report(self.trip)

        self.assertIsInstance(report, str)
        self.assertGreater(len(report), 0)

    def test_report_contains_title(self):
        report = generate_text_report(self.trip)

        self.assertIn(
            "TRAVEL COST ESTIMATE",
            report,
        )

    def test_report_contains_traveler_information(self):
        report = generate_text_report(self.trip)

        self.assertIn(
            "Traveler: Jonah Pickens",
            report,
        )
        self.assertIn(
            "Destination: Honolulu, Hawaii",
            report,
        )
        self.assertIn(
            "Departure Date: 07/10/2026",
            report,
        )
        self.assertIn(
            "Return Date: 07/15/2026",
            report,
        )

    def test_report_contains_included_major_bookings(self):
        report = generate_text_report(self.trip)

        self.assertIn(
            "Airfare: $650.00",
            report,
        )
        self.assertIn(
            "Hotel: $1200.00",
            report,
        )

    def test_report_excludes_unselected_major_bookings(self):
        report = generate_text_report(self.trip)

        self.assertNotIn(
            "Rental Car:",
            report,
        )
        self.assertNotIn(
            "$800.00",
            report,
        )

    def test_report_contains_included_other_expenses(self):
        report = generate_text_report(self.trip)

        self.assertIn(
            "Airport Parking: $90.00",
            report,
        )

    def test_report_excludes_unselected_other_expenses(self):
        report = generate_text_report(self.trip)

        self.assertNotIn(
            "Baggage Fees:",
            report,
        )
        self.assertNotIn(
            "$70.00",
            report,
        )

    def test_report_contains_per_diem_details(self):
        report = generate_text_report(self.trip)

        self.assertIn(
            "Daily Rate: $100.00",
            report,
        )
        self.assertIn(
            "Travel Days: 6",
            report,
        )
        self.assertIn(
            "Full-Rate Days: 4",
            report,
        )
        self.assertIn(
            "Travel-Rate Days: 2",
            report,
        )
        self.assertIn(
            "Per Diem Total: $550.00",
            report,
        )

    def test_report_contains_all_totals(self):
        report = generate_text_report(self.trip)

        self.assertIn(
            "Major Bookings Total: $1850.00",
            report,
        )
        self.assertIn(
            "Other Expenses Total: $90.00",
            report,
        )
        self.assertIn(
            "Per Diem Total: $550.00",
            report,
        )
        self.assertIn(
            "TOTAL ESTIMATED COST",
            report,
        )
        self.assertIn(
            "$2490.00",
            report,
        )

    def test_report_handles_no_selected_expenses(self):
        empty_trip = create_travel_request()

        empty_trip["traveler"]["name"] = "Test Traveler"
        empty_trip["traveler"]["destination"] = "Test Destination"
        empty_trip["traveler"]["departure_date"] = "08/01/2026"
        empty_trip["traveler"]["return_date"] = "08/02/2026"
        empty_trip["per_diem"]["daily_rate"] = 0.00

        calculate_trip_totals(empty_trip)

        report = generate_text_report(empty_trip)

        self.assertIn(
            "Major Bookings Total: $0.00",
            report,
        )
        self.assertIn(
            "Other Expenses Total: $0.00",
            report,
        )
        self.assertIn(
            "Per Diem Total: $0.00",
            report,
        )
        self.assertIn(
            "TOTAL ESTIMATED COST",
            report,
        )
        self.assertIn(
            "$0.00",
            report,
        )

    def test_report_does_not_modify_travel_request(self):
        original_trip = copy.deepcopy(self.trip)

        generate_text_report(self.trip)

        self.assertEqual(
            self.trip,
            original_trip,
        )


if __name__ == "__main__":
    unittest.main()