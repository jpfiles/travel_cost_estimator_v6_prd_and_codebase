def create_travel_request():
    return {

        "metadata": {
            "version": "6.0",
            "created": "",
            "last_modified": ""
        },

        "traveler": {
            "name": "",
            "destination": "",
            "departure_date": "",
            "return_date": ""
        },

        "major_bookings": {

            "airfare": {
                "display_name": "Airfare",
                "included": False,
                "description": "",
                "cost": 0.00
            },

            "hotel": {
                "display_name": "Hotel",
                "included": False,
                "description": "",
                "cost": 0.00
            },

            "rental_car": {
                "display_name": "Rental Car",
                "included": False,
                "description": "",
                "cost": 0.00
            }
        },

        "other_expenses": {

            "pov_mileage": {
                "display_name": "POV Mileage",
                "included": False,
                "cost": 0.00
            },

            "rental_car_fuel": {
                "display_name": "Rental Car Fuel",
                "included": False,
                "cost": 0.00
            },

            "baggage_fees": {
                "display_name": "Baggage Fees",
                "included": False,
                "cost": 0.00
            },

            "hotel_taxes": {
                "display_name": "Hotel Taxes",
                "included": False,
                "cost": 0.00
            },

            "resort_fees": {
                "display_name": "Resort Fees",
                "included": False,
                "cost": 0.00
            },

            "tolls": {
                "display_name": "Tolls",
                "included": False,
                "cost": 0.00
            },

            "advanced_travel_fees": {
                "display_name": "ADTRAV Fees",
                "included": False,
                "cost": 0.00
            },

            "airport_parking": {
                "display_name": "Airport Parking",
                "included": False,
                "cost": 0.00
            },

            "hotel_parking": {
                "display_name": "Hotel Parking",
                "included": False,
                "cost": 0.00
            },

            "uber_taxi": {
                "display_name": "Uber/Taxi Services",
                "included": False,
                "cost": 0.00
            },

            "miscellaneous": {
                "display_name": "Miscellaneous",
                "included": False,
                "cost": 0.00
            },
        },

        "per_diem": {
            "meals_rate": 0.00,
            "incidentals_rate": 0.00,
            "daily_rate": 0.00,
            "travel_days": 0,
            "full_rate_days": 0,
            "travel_rate_days": 0,
            "meals_total": 0.00,
            "incidentals_total": 0.00,
            "total": 0.00
        },

        "totals": {
            "major_bookings": 0.00,
            "other_expenses": 0.00,
            "per_diem": 0.00,
            "grand_total": 0.00
        }
    }