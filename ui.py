import tkinter as tk
from tkinter import ttk

from config import (
    DATE_FORMAT_DISPLAY,
    DEFAULT_WINDOW_GEOMETRY,
    MINIMUM_WINDOW_HEIGHT,
    MINIMUM_WINDOW_WIDTH,
    WINDOW_TITLE,
)
from travel_model import create_travel_request


class TravelCostEstimatorApp:

    def __init__(self, root):
        self.root = root
        self.major_booking_vars = {}
        self.root.title(WINDOW_TITLE)
        self.root.geometry(DEFAULT_WINDOW_GEOMETRY)
        self.root.minsize(
            MINIMUM_WINDOW_WIDTH,
            MINIMUM_WINDOW_HEIGHT,
        )

        self.travel_request = create_travel_request()

        self.current_file_path = None
        self.is_modified = False

        self.project_status_var = tk.StringVar(
            master=self.root,
            value="Project: Unsaved",
        )

        self.status_message_var = tk.StringVar(
            master=self.root,
            value="Ready.",
        )

        self.traveler_name_var = tk.StringVar(
            master=self.root,
        )
        self.destination_var = tk.StringVar(
            master=self.root,
        )
        self.departure_date_var = tk.StringVar(
            master=self.root,
        )
        self.return_date_var = tk.StringVar(
            master=self.root,
        )

        self.create_header()
        self.create_status_bar()
        self.create_main_content()

    def create_header(self):
        """Create the application title and project status."""
        header_frame = ttk.Frame(
            self.root,
            padding=(20, 15, 20, 10),
        )
        header_frame.pack(fill="x")
        header_frame.columnconfigure(
            0,
            weight=1,
        )

        title_label = ttk.Label(
            header_frame,
            text="Travel Cost Estimator",
            font=("Segoe UI", 20, "bold"),
        )
        title_label.grid(
            row=0,
            column=0,
            sticky="w",
        )

        subtitle_label = ttk.Label(
            header_frame,
            text=(
                "Estimate official travel costs "
                "and generate reports"
            ),
            font=("Segoe UI", 10),
        )
        subtitle_label.grid(
            row=1,
            column=0,
            sticky="w",
            pady=(2, 0),
        )

        project_status_label = ttk.Label(
            header_frame,
            textvariable=self.project_status_var,
            font=("Segoe UI", 10, "bold"),
        )
        project_status_label.grid(
            row=0,
            column=1,
            rowspan=2,
            sticky="e",
            padx=(20, 0),
        )

        separator = ttk.Separator(
            self.root,
            orient="horizontal",
        )
        separator.pack(fill="x")

    def create_main_content(self):
        """Create the expandable application workspace."""
        self.main_frame = ttk.Frame(
            self.root,
            padding=(20, 15, 20, 15),
        )
        self.main_frame.pack(
            fill="both",
            expand=True,
        )

        self.create_traveler_section()                
        self.create_input_notebook()

    def create_traveler_section(self):
        """Create the traveler and trip-date input fields."""
        traveler_frame = ttk.LabelFrame(
            self.main_frame,
            text="Traveler Information",
            padding=15,
        )
        traveler_frame.pack(
            fill="x",
        )

        traveler_frame.columnconfigure(
            1,
            weight=1,
        )
        traveler_frame.columnconfigure(
            3,
            weight=1,
        )

        name_label = ttk.Label(
            traveler_frame,
            text="Traveler Name",
        )
        name_label.grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 8),
            pady=(0, 12),
        )

        self.name_entry = ttk.Entry(
            traveler_frame,
            textvariable=self.traveler_name_var,
        )
        self.name_entry.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(0, 24),
            pady=(0, 12),
        )

        destination_label = ttk.Label(
            traveler_frame,
            text="Destination",
        )
        destination_label.grid(
            row=0,
            column=2,
            sticky="w",
            padx=(0, 8),
            pady=(0, 12),
        )

        self.destination_entry = ttk.Entry(
            traveler_frame,
            textvariable=self.destination_var,
        )
        self.destination_entry.grid(
            row=0,
            column=3,
            sticky="ew",
            pady=(0, 12),
        )

        departure_label = ttk.Label(
            traveler_frame,
            text="Departure Date",
        )
        departure_label.grid(
            row=1,
            column=0,
            sticky="w",
            padx=(0, 8),
        )

        self.departure_entry = ttk.Entry(
            traveler_frame,
            textvariable=self.departure_date_var,
        )
        self.departure_entry.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(0, 24),
        )

        return_label = ttk.Label(
            traveler_frame,
            text="Return Date",
        )
        return_label.grid(
            row=1,
            column=2,
            sticky="w",
            padx=(0, 8),
        )

        self.return_entry = ttk.Entry(
            traveler_frame,
            textvariable=self.return_date_var,
        )
        self.return_entry.grid(
            row=1,
            column=3,
            sticky="ew",
        )

        date_help_label = ttk.Label(
            traveler_frame,
            text=f"Date format: {DATE_FORMAT_DISPLAY}",
        )
        date_help_label.grid(
            row=2,
            column=1,
            columnspan=3,
            sticky="w",
            pady=(8, 0),
        )

        for entry in (
            self.name_entry,
            self.destination_entry,
            self.departure_entry,
            self.return_entry,
        ):
            entry.bind(
                "<KeyRelease>",
                self.mark_modified,
            )

        self.name_entry.focus_set()

    def create_input_notebook(self):
        """Create the tabbed travel-cost input workspace."""
        self.input_notebook = ttk.Notebook(
            self.main_frame,
        )
        self.input_notebook.pack(
            fill="both",
            expand=True,
            pady=(15, 0),
        )

        self.major_bookings_tab = ttk.Frame(
            self.input_notebook,
            padding=15,
        )
        self.other_expenses_tab = ttk.Frame(
            self.input_notebook,
            padding=15,
        )
        self.per_diem_tab = ttk.Frame(
            self.input_notebook,
            padding=15,
        )

        self.input_notebook.add(
            self.major_bookings_tab,
            text="Major Bookings",
        )
        self.input_notebook.add(
            self.other_expenses_tab,
            text="Other Expenses",
        )
        self.input_notebook.add(
            self.per_diem_tab,
            text="Per Diem",
        )

        self.create_major_bookings_tab()

    def create_major_bookings_tab(self):
        """Create the major-booking input table."""
        self.major_bookings_tab.columnconfigure(
            1,
            weight=1,
        )

        ttk.Label(
            self.major_bookings_tab,
            text="Include",
            font=("Segoe UI", 10, "bold"),
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 15),
            pady=(0, 10),
        )

        ttk.Label(
            self.major_bookings_tab,
            text="Booking and Description",
            font=("Segoe UI", 10, "bold"),
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=(0, 15),
            pady=(0, 10),
        )

        ttk.Label(
            self.major_bookings_tab,
            text="Cost",
            font=("Segoe UI", 10, "bold"),
        ).grid(
            row=0,
            column=2,
            sticky="e",
            pady=(0, 10),
        )

        for row_number, (
            booking_key,
            booking,
        ) in enumerate(
            self.travel_request[
                "major_bookings"
            ].items(),
            start=1,
        ):
            included_var = tk.BooleanVar(
                master=self.root,
                value=booking["included"],
            )
            description_var = tk.StringVar(
                master=self.root,
                value=booking["description"],
            )
            cost_var = tk.StringVar(
                master=self.root,
                value=f"{booking['cost']:.2f}",
            )

            self.major_booking_vars[
                booking_key
            ] = {
                "included": included_var,
                "description": description_var,
                "cost": cost_var,
            }

            include_checkbox = ttk.Checkbutton(
                self.major_bookings_tab,
                text=booking["display_name"],
                variable=included_var,
                command=self.mark_modified,
            )
            include_checkbox.grid(
                row=row_number,
                column=0,
                sticky="w",
                padx=(0, 15),
                pady=6,
            )

            description_entry = ttk.Entry(
                self.major_bookings_tab,
                textvariable=description_var,
            )
            description_entry.grid(
                row=row_number,
                column=1,
                sticky="ew",
                padx=(0, 15),
                pady=6,
            )
            description_entry.bind(
                "<KeyRelease>",
                self.mark_modified,
            )

            cost_entry = ttk.Entry(
                self.major_bookings_tab,
                textvariable=cost_var,
                width=16,
                justify="right",
            )
            cost_entry.grid(
                row=row_number,
                column=2,
                sticky="e",
                pady=6,
            )
            cost_entry.bind(
                "<KeyRelease>",
                self.mark_modified,
            )        

    def mark_modified(self, event=None):
        """Mark the current project as having unsaved changes."""
        self.is_modified = True

        if self.current_file_path is None:
            self.project_status_var.set(
                "Project: Unsaved *"
            )
        else:
            self.project_status_var.set(
                f"Project: {self.current_file_path.name} *"
            )

        self.status_message_var.set(
            "Unsaved changes."
        )

    def create_status_bar(self):
        """Create the status bar at the bottom of the window."""
        status_container = ttk.Frame(
            self.root,
        )
        status_container.pack(
            side="bottom",
            fill="x",
        )

        separator = ttk.Separator(
            status_container,
            orient="horizontal",
        )
        separator.pack(fill="x")

        status_frame = ttk.Frame(
            status_container,
            padding=(20, 8),
        )
        status_frame.pack(fill="x")

        status_label = ttk.Label(
            status_frame,
            textvariable=self.status_message_var,
        )
        status_label.pack(side="left")
