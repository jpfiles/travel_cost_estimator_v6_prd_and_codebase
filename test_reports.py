import copy
import unittest

import csv
import reports

from io import StringIO
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

        self.trip["per_diem"]["meals_rate"] = 75.00
        self.trip["per_diem"]["incidentals_rate"] = 25.00

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
            "Meals Rate: $75.00",
            report,
        )
        self.assertIn(
            "Incidentals Rate: $25.00",
            report,
        )
        self.assertIn(
            "Combined M&IE Rate: $100.00",
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
            "Travel-Rate Days (75%): 2",
            report,
        )
        self.assertIn(
            "Meals Subtotal: $412.50",
            report,
        )
        self.assertIn(
            "Incidentals Subtotal: $137.50",
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

class TestCsvAndHtmlReportGeneration(unittest.TestCase):

    def setUp(self):
        """Create and calculate a representative travel request."""
        self.trip = create_travel_request()

        self.trip["traveler"]["name"] = "Jonah Pickens"
        self.trip["traveler"]["destination"] = "Honolulu, Hawaii"
        self.trip["traveler"]["departure_date"] = "07/10/2026"
        self.trip["traveler"]["return_date"] = "07/15/2026"

        self.trip["major_bookings"]["airfare"]["included"] = True
        self.trip["major_bookings"]["airfare"]["description"] = (
            "Round-trip airfare"
        )
        self.trip["major_bookings"]["airfare"]["cost"] = 650.00

        self.trip["major_bookings"]["hotel"]["included"] = True
        self.trip["major_bookings"]["hotel"]["description"] = (
            "Five-night hotel stay"
        )
        self.trip["major_bookings"]["hotel"]["cost"] = 1200.00

        self.trip["major_bookings"]["rental_car"]["included"] = False
        self.trip["major_bookings"]["rental_car"]["description"] = (
            "Excluded rental car"
        )
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

        self.trip["per_diem"]["meals_rate"] = 75.00
        self.trip["per_diem"]["incidentals_rate"] = 25.00

        calculate_trip_totals(self.trip)

    def parse_csv_report(self):
        """Generate and parse the CSV report into rows."""
        csv_report = reports.generate_csv_report(
            self.trip
        )

        return list(
            csv.reader(
                StringIO(csv_report)
            )
        )

    def test_csv_report_returns_string(self):
        csv_report = reports.generate_csv_report(
            self.trip
        )

        self.assertIsInstance(csv_report, str)
        self.assertGreater(len(csv_report), 0)

    def test_csv_report_has_expected_header(self):
        rows = self.parse_csv_report()

        self.assertEqual(
            rows[0],
            [
                "Section",
                "Item",
                "Description",
                "Amount",
            ],
        )

    def test_csv_report_contains_traveler_information(self):
        rows = self.parse_csv_report()

        self.assertIn(
            [
                "Traveler Information",
                "Traveler",
                "Jonah Pickens",
                "",
            ],
            rows,
        )

        self.assertIn(
            [
                "Traveler Information",
                "Destination",
                "Honolulu, Hawaii",
                "",
            ],
            rows,
        )

        self.assertIn(
            [
                "Traveler Information",
                "Departure Date",
                "07/10/2026",
                "",
            ],
            rows,
        )

        self.assertIn(
            [
                "Traveler Information",
                "Return Date",
                "07/15/2026",
                "",
            ],
            rows,
        )

    def test_csv_report_contains_included_bookings(self):
        rows = self.parse_csv_report()

        self.assertIn(
            [
                "Major Bookings",
                "Airfare",
                "Round-trip airfare",
                "650.00",
            ],
            rows,
        )

        self.assertIn(
            [
                "Major Bookings",
                "Hotel",
                "Five-night hotel stay",
                "1200.00",
            ],
            rows,
        )

    def test_csv_report_excludes_unselected_items(self):
        rows = self.parse_csv_report()

        item_names = [
            row[1]
            for row in rows
            if len(row) >= 2
        ]

        self.assertNotIn(
            "Rental Car",
            item_names,
        )
        self.assertNotIn(
            "Baggage Fees",
            item_names,
        )

    def test_csv_report_contains_expenses_and_totals(self):
        rows = self.parse_csv_report()

        self.assertIn(
            [
                "Other Expenses",
                "Airport Parking",
                "",
                "90.00",
            ],
            rows,
        )

        self.assertIn(
            [
                "Totals",
                "Major Bookings Total",
                "",
                "1850.00",
            ],
            rows,
        )

        self.assertIn(
            [
                "Totals",
                "Other Expenses Total",
                "",
                "90.00",
            ],
            rows,
        )

        self.assertIn(
            [
                "Totals",
                "Per Diem Total",
                "",
                "550.00",
            ],
            rows,
        )

        self.assertIn(
            [
                "Totals",
                "Grand Total",
                "",
                "2490.00",
            ],
            rows,
        )

    def test_csv_report_contains_per_diem_components(self):
        rows = self.parse_csv_report()

        expected_rows = [
            [
                "Per Diem",
                "Meals Rate",
                "",
                "75.00",
            ],
            [
                "Per Diem",
                "Incidentals Rate",
                "",
                "25.00",
            ],
            [
                "Per Diem",
                "Combined M&IE Rate",
                "",
                "100.00",
            ],
            [
                "Per Diem",
                "Meals Subtotal",
                "",
                "412.50",
            ],
            [
                "Per Diem",
                "Incidentals Subtotal",
                "",
                "137.50",
            ],
                        [
                "Per Diem",
                "Travel-Rate Days (75%)",
                "",
                "2",
            ],
        ]

        for expected_row in expected_rows:
            self.assertIn(
                expected_row,
                rows,
            )

    def test_csv_report_preserves_comma_inside_destination(self):
        rows = self.parse_csv_report()

        destination_rows = [
            row
            for row in rows
            if len(row) >= 2
            and row[1] == "Destination"
        ]

        self.assertEqual(
            len(destination_rows),
            1,
        )
        self.assertEqual(
            destination_rows[0][2],
            "Honolulu, Hawaii",
        )
        self.assertEqual(
            len(destination_rows[0]),
            4,
        )

    def test_html_report_returns_complete_document(self):
        html_report = reports.generate_html_report(
            self.trip
        )

        self.assertIsInstance(html_report, str)
        self.assertIn(
            "<!DOCTYPE html>",
            html_report,
        )
        self.assertIn(
            '<html lang="en">',
            html_report,
        )
        self.assertIn(
            "</html>",
            html_report,
        )

    def test_html_report_contains_traveler_information(self):
        html_report = reports.generate_html_report(
            self.trip
        )

        self.assertIn(
            "Jonah Pickens",
            html_report,
        )
        self.assertIn(
            "Honolulu, Hawaii",
            html_report,
        )
        self.assertIn(
            "07/10/2026",
            html_report,
        )
        self.assertIn(
            "07/15/2026",
            html_report,
        )

    def test_html_report_contains_included_costs(self):
        html_report = reports.generate_html_report(
            self.trip
        )

        self.assertIn(
            "Airfare",
            html_report,
        )
        self.assertIn(
            "$650.00",
            html_report,
        )
        self.assertIn(
            "Hotel",
            html_report,
        )
        self.assertIn(
            "$1200.00",
            html_report,
        )
        self.assertIn(
            "Airport Parking",
            html_report,
        )
        self.assertIn(
            "$90.00",
            html_report,
        )

    def test_html_report_excludes_unselected_items(self):
        html_report = reports.generate_html_report(
            self.trip
        )

        self.assertNotIn(
            "Excluded rental car",
            html_report,
        )
        self.assertNotIn(
            "Baggage Fees",
            html_report,
        )
        self.assertNotIn(
            "$800.00",
            html_report,
        )
        self.assertNotIn(
            "$70.00",
            html_report,
        )

    def test_html_report_contains_totals(self):
        html_report = reports.generate_html_report(
            self.trip
        )

        self.assertIn(
            "Major Bookings Total",
            html_report,
        )
        self.assertIn(
            "$1850.00",
            html_report,
        )
        self.assertIn(
            "Other Expenses Total",
            html_report,
        )
        self.assertIn(
            "Per Diem Total",
            html_report,
        )
        self.assertIn(
            "$550.00",
            html_report,
        )
        self.assertIn(
            "Grand Total",
            html_report,
        )
        self.assertIn(
            "$2490.00",
            html_report,
        )

    def test_html_report_contains_per_diem_components(self):
        html_report = reports.generate_html_report(
            self.trip
        )

        expected_content = (
            "Meals Rate",
            "$75.00",
            "Incidentals Rate",
            "$25.00",
            "Combined M&amp;IE Rate",
            "$100.00",
            "Meals Subtotal",
            "$412.50",
            "Incidentals Subtotal",
            "$137.50",
            "Travel-Rate Days (75%)",
        )

        for expected_value in expected_content:
            self.assertIn(
                expected_value,
                html_report,
            )

    def test_html_report_escapes_special_characters(self):
        self.trip["traveler"]["name"] = (
            "Jonah <Admin> & Co."
        )

        html_report = reports.generate_html_report(
            self.trip
        )

        self.assertIn(
            "Jonah &lt;Admin&gt; &amp; Co.",
            html_report,
        )
        self.assertNotIn(
            "Jonah <Admin> & Co.",
            html_report,
        )


if __name__ == "__main__":
    unittest.main()