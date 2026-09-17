import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from calculations import calculate_trip_totals
from travel_model import create_travel_request
from pathlib import Path
from storage import load_travel_request, save_travel_request

from reports import (
    generate_csv_report,
    generate_html_report,
    generate_text_report,
)

from config import (
    DATE_FORMAT_DISPLAY,
    DEFAULT_WINDOW_GEOMETRY,
    MINIMUM_WINDOW_HEIGHT,
    MINIMUM_WINDOW_WIDTH,
    PROJECTS_DIRECTORY,
    REPORTS_DIRECTORY,
    WINDOW_TITLE,
)


class TravelCostEstimatorApp:

    def __init__(self, root):
        self.root = root
        self.major_booking_vars = {}
        self.other_expense_vars = {}
        self.root.title(WINDOW_TITLE)
        self.root.geometry(DEFAULT_WINDOW_GEOMETRY)
        self.root.minsize(
            MINIMUM_WINDOW_WIDTH,
            MINIMUM_WINDOW_HEIGHT,
        )

        self.travel_request = create_travel_request()

        self.current_file_path = None
        self.is_modified = False

        self.daily_rate_var = tk.StringVar(
            master=self.root,
            value="0.00",
        )
        self.travel_days_var = tk.StringVar(
            master=self.root,
            value="0",
        )
        self.full_rate_days_var = tk.StringVar(
            master=self.root,
            value="0",
        )
        self.travel_rate_days_var = tk.StringVar(
            master=self.root,
            value="0",
        )

        self.booking_total_var = tk.StringVar(
            master=self.root,
            value="$0.00",
        )
        self.other_total_var = tk.StringVar(
            master=self.root,
            value="$0.00",
        )
        self.per_diem_total_var = tk.StringVar(
            master=self.root,
            value="$0.00",
        )
        self.grand_total_var = tk.StringVar(
            master=self.root,
            value="$0.00",
        )

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
        self.create_action_bar()
        self.create_status_bar()
        self.create_main_content()

        self.root.minsize(
            MINIMUM_WINDOW_WIDTH,
            MINIMUM_WINDOW_HEIGHT,
        )

        self.configure_styles()

        self.travel_request = create_travel_request()

    def configure_styles(self):
        """Configure theme-compatible application styles."""
        self.style = ttk.Style(
            self.root,
        )

        self.style.configure(
            "Travel.TNotebook",
            tabmargins=(0, 4, 0, 0),
        )

        self.style.configure(
            "Travel.TNotebook.Tab",
            font=("Segoe UI", 10, "bold"),
            padding=(16, 8),
        )

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

    def create_action_bar(self):
        """Create project-file action controls."""
        action_frame = ttk.Frame(
            self.root,
            padding=(20, 8),
        )
        action_frame.pack(fill="x")

        ttk.Button(
            action_frame,
            text="New",
            command=self.new_project,
        ).pack(
            side="left",
            padx=(0, 8),
        )

        ttk.Button(
            action_frame,
            text="Open",
            command=self.open_project,
        ).pack(
            side="left",
            padx=(0, 8),
        )

        ttk.Button(
            action_frame,
            text="Save",
            command=self.save_project,
        ).pack(
            side="left",
            padx=(0, 8),
        )

        ttk.Button(
            action_frame,
            text="Save As",
            command=self.save_project_as,
        ).pack(
            side="left",
        )

        ttk.Separator(
            action_frame,
            orient="vertical",
        ).pack(
            side="left",
            fill="y",
            padx=12,
        )

        ttk.Button(
            action_frame,
            text="Export",
            command=self.export_report,
        ).pack(
            side="left",
        )

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
            style="Travel.TNotebook",
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
        self.create_other_expenses_tab()
        self.create_per_diem_tab()

    def create_per_diem_tab(self):
        """Create per diem inputs and the estimate summary."""
        self.per_diem_tab.columnconfigure(
            0,
            weight=1,
        )
        self.per_diem_tab.columnconfigure(
            1,
            weight=1,
        )

        input_frame = ttk.LabelFrame(
            self.per_diem_tab,
            text="Per Diem",
            padding=15,
        )
        input_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10),
        )
        input_frame.columnconfigure(
            1,
            weight=1,
        )

        ttk.Label(
            input_frame,
            text="Daily Rate",
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 10),
            pady=6,
        )

        daily_rate_entry = ttk.Entry(
            input_frame,
            textvariable=self.daily_rate_var,
            justify="right",
        )
        daily_rate_entry.grid(
            row=0,
            column=1,
            sticky="ew",
            pady=6,
        )
        daily_rate_entry.bind(
            "<KeyRelease>",
            self.mark_modified,
        )

        per_diem_rows = (
            ("Travel Days", self.travel_days_var),
            ("Full-Rate Days", self.full_rate_days_var),
            (
                "Travel-Rate Days",
                self.travel_rate_days_var,
            ),
        )

        for row_number, (
            label_text,
            value_variable,
        ) in enumerate(
            per_diem_rows,
            start=1,
        ):
            ttk.Label(
                input_frame,
                text=label_text,
            ).grid(
                row=row_number,
                column=0,
                sticky="w",
                padx=(0, 10),
                pady=6,
            )

            ttk.Label(
                input_frame,
                textvariable=value_variable,
                font=("Segoe UI", 10, "bold"),
            ).grid(
                row=row_number,
                column=1,
                sticky="e",
                pady=6,
            )

        summary_frame = ttk.LabelFrame(
            self.per_diem_tab,
            text="Estimate Summary",
            padding=15,
        )
        summary_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(10, 0),
        )
        summary_frame.columnconfigure(
            1,
            weight=1,
        )

        summary_rows = (
            (
                "Major Bookings",
                self.booking_total_var,
            ),
            (
                "Other Expenses",
                self.other_total_var,
            ),
            (
                "Per Diem",
                self.per_diem_total_var,
            ),
            (
                "Estimated Total",
                self.grand_total_var,
            ),
        )

        for row_number, (
            label_text,
            value_variable,
        ) in enumerate(summary_rows):
            is_grand_total = (
                label_text == "Estimated Total"
            )

            label_font = (
                ("Segoe UI", 11, "bold")
                if is_grand_total
                else ("Segoe UI", 10)
            )

            ttk.Label(
                summary_frame,
                text=label_text,
                font=label_font,
            ).grid(
                row=row_number,
                column=0,
                sticky="w",
                padx=(0, 20),
                pady=8,
            )

            ttk.Label(
                summary_frame,
                textvariable=value_variable,
                font=label_font,
            ).grid(
                row=row_number,
                column=1,
                sticky="e",
                pady=8,
            )

        calculate_button = ttk.Button(
            self.per_diem_tab,
            text="Calculate Estimate",
            command=self.calculate_estimate,
        )
        calculate_button.grid(
            row=1,
            column=1,
            sticky="e",
            pady=(20, 0),
        )

    def get_projects_directory(self):
        """Return the project directory and create it if needed."""
        projects_directory = (
            Path.cwd() / PROJECTS_DIRECTORY
        )
        projects_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        return projects_directory

    def get_reports_directory(self):
        """Return the report directory and create it if needed."""
        reports_directory = (
            Path.cwd() / REPORTS_DIRECTORY
        )
        reports_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        return reports_directory

    def export_report(self):
        """Calculate and export the current travel estimate."""
        try:
            self.sync_form_to_model()
            calculate_trip_totals(
                self.travel_request
            )
            self.update_estimate_display()
        except ValueError as error:
            self.status_message_var.set(
                "Unable to export report."
            )
            messagebox.showerror(
                "Unable to Export Report",
                str(error),
                parent=self.root,
            )
            return

        file_path = filedialog.asksaveasfilename(
            parent=self.root,
            title="Export Travel Cost Estimate",
            initialdir=self.get_reports_directory(),
            initialfile="travel_cost_estimate.txt",
            defaultextension=".txt",
            filetypes=(
                (
                    "Text Report",
                    "*.txt",
                ),
                (
                    "CSV Report",
                    "*.csv",
                ),
                (
                    "HTML Report",
                    "*.html",
                ),
            ),
        )

        if not file_path:
            return

        destination = Path(file_path)
        extension = destination.suffix.lower()

        report_generators = {
            ".txt": generate_text_report,
            ".csv": generate_csv_report,
            ".html": generate_html_report,
        }

        generator = report_generators.get(
            extension
        )

        if generator is None:
            messagebox.showerror(
                "Unsupported Report Format",
                (
                    "Reports must use a .txt, .csv, "
                    "or .html extension."
                ),
                parent=self.root,
            )
            return

        report_content = generator(
            self.travel_request
        )

        try:
            with destination.open(
                "w",
                encoding="utf-8",
                newline="",
            ) as report_file:
                report_file.write(
                    report_content
                )
        except OSError as error:
            self.status_message_var.set(
                "Unable to export report."
            )
            messagebox.showerror(
                "Unable to Export Report",
                str(error),
                parent=self.root,
            )
            return

        self.status_message_var.set(
            f"Report exported: {destination.name}"
        )

        messagebox.showinfo(
            "Report Exported",
            (
                "The travel cost estimate was "
                "exported successfully."
            ),
            parent=self.root,
        )

    def confirm_discard_changes(self):
        """Confirm whether unsaved changes may be discarded."""
        if not self.is_modified:
            return True

        return messagebox.askyesno(
            "Unsaved Changes",
            (
                "This project contains unsaved changes.\n\n"
                "Discard the changes and continue?"
            ),
            parent=self.root,
        )

    def populate_form_from_model(self):
        """Copy the current travel model into the UI."""
        traveler = self.travel_request["traveler"]

        self.traveler_name_var.set(
            traveler["name"]
        )
        self.destination_var.set(
            traveler["destination"]
        )
        self.departure_date_var.set(
            traveler["departure_date"]
        )
        self.return_date_var.set(
            traveler["return_date"]
        )

        for booking_key, variables in (
            self.major_booking_vars.items()
        ):
            booking = self.travel_request[
                "major_bookings"
            ][booking_key]

            variables["included"].set(
                booking["included"]
            )
            variables["description"].set(
                booking["description"]
            )
            variables["cost"].set(
                f"{booking['cost']:.2f}"
            )

        for expense_key, variables in (
            self.other_expense_vars.items()
        ):
            expense = self.travel_request[
                "other_expenses"
            ][expense_key]

            variables["included"].set(
                expense["included"]
            )
            variables["cost"].set(
                f"{expense['cost']:.2f}"
            )

        per_diem = self.travel_request["per_diem"]

        self.daily_rate_var.set(
            f"{per_diem['daily_rate']:.2f}"
        )

        self.update_estimate_display()

        if per_diem["travel_days"] == 0:
            self.travel_rate_days_var.set("0")\

    def new_project(self):
        """Create a new blank travel project."""
        if not self.confirm_discard_changes():
            return

        self.travel_request = create_travel_request()
        self.current_file_path = None
        self.is_modified = False

        self.populate_form_from_model()

        self.project_status_var.set(
            "Project: Unsaved"
        )
        self.status_message_var.set(
            "New project created."
        )

        self.name_entry.focus_set()

    def open_project(self):
        """Open an existing JSON travel project."""
        if not self.confirm_discard_changes():
            return

        file_path = filedialog.askopenfilename(
            parent=self.root,
            title="Open Travel Project",
            initialdir=self.get_projects_directory(),
            filetypes=(
                (
                    "Travel Project",
                    "*.json",
                ),
                (
                    "JSON Files",
                    "*.json",
                ),
            ),
        )

        if not file_path:
            return

        loaded_request = load_travel_request(
            file_path
        )

        if loaded_request is None:
            messagebox.showerror(
                "Unable to Open Project",
                "The selected project could not be opened.",
                parent=self.root,
            )
            return

        previous_request = self.travel_request
        self.travel_request = loaded_request

        try:
            self.populate_form_from_model()
        except (KeyError, TypeError, ValueError):
            self.travel_request = previous_request
            self.populate_form_from_model()

            messagebox.showerror(
                "Invalid Project",
                (
                    "The selected file is not a valid "
                    "Travel Cost Estimator project."
                ),
                parent=self.root,
            )
            return

        self.current_file_path = Path(
            file_path
        )
        self.is_modified = False

        self.project_status_var.set(
            f"Project: {self.current_file_path.name}"
        )
        self.status_message_var.set(
            "Project opened successfully."
        )

    def save_project(self):
        """Save the current project."""
        if self.current_file_path is None:
            return self.save_project_as()

        return self.save_project_to_path(
            self.current_file_path
        )

    def save_project_as(self):
        """Prompt for a new JSON project filename."""
        file_path = filedialog.asksaveasfilename(
            parent=self.root,
            title="Save Travel Project",
            initialdir=self.get_projects_directory(),
            defaultextension=".json",
            filetypes=(
                (
                    "Travel Project",
                    "*.json",
                ),
                (
                    "JSON Files",
                    "*.json",
                ),
            ),
        )

        if not file_path:
            return False

        return self.save_project_to_path(
            Path(file_path)
        )

    def save_project_to_path(self, file_path):
        """Synchronize and save the project to a path."""
        try:
            self.sync_form_to_model()

            departure_date = self.travel_request[
                "traveler"
            ]["departure_date"]

            return_date = self.travel_request[
                "traveler"
            ]["return_date"]

            if departure_date or return_date:
                calculate_trip_totals(
                    self.travel_request
                )
                self.update_estimate_display()

        except ValueError as error:
            self.status_message_var.set(
                "Unable to save project."
            )
            messagebox.showerror(
                "Unable to Save Project",
                str(error),
                parent=self.root,
            )
            return False

        save_succeeded = save_travel_request(
            self.travel_request,
            file_path,
        )

        if not save_succeeded:
            self.status_message_var.set(
                "Unable to save project."
            )
            messagebox.showerror(
                "Unable to Save Project",
                "The project could not be saved.",
                parent=self.root,
            )
            return False

        self.current_file_path = Path(
            file_path
        )
        self.is_modified = False

        self.project_status_var.set(
            f"Project: {self.current_file_path.name}"
        )
        self.status_message_var.set(
            "Project saved successfully."
        )

        return True

    def parse_amount(self, value, field_name):
        """Convert a currency entry into a non-negative float."""
        cleaned_value = (
            value.strip()
            .replace("$", "")
            .replace(",", "")
        )

        if cleaned_value == "":
            raise ValueError(
                f"{field_name} is required."
            )

        try:
            amount = float(cleaned_value)
        except ValueError:
            raise ValueError(
                f"{field_name} must be a valid number."
            ) from None

        if amount < 0:
            raise ValueError(
                f"{field_name} cannot be negative."
            )

        return amount

    def sync_form_to_model(self):
        """Copy all current form values into the travel model."""
        traveler = self.travel_request["traveler"]

        traveler["name"] = (
            self.traveler_name_var.get().strip()
        )
        traveler["destination"] = (
            self.destination_var.get().strip()
        )
        traveler["departure_date"] = (
            self.departure_date_var.get().strip()
        )
        traveler["return_date"] = (
            self.return_date_var.get().strip()
        )

        for booking_key, variables in (
            self.major_booking_vars.items()
        ):
            booking = self.travel_request[
                "major_bookings"
            ][booking_key]

            booking["included"] = (
                variables["included"].get()
            )
            booking["description"] = (
                variables["description"].get().strip()
            )
            booking["cost"] = self.parse_amount(
                variables["cost"].get(),
                booking["display_name"],
            )

        for expense_key, variables in (
            self.other_expense_vars.items()
        ):
            expense = self.travel_request[
                "other_expenses"
            ][expense_key]

            expense["included"] = (
                variables["included"].get()
            )
            expense["cost"] = self.parse_amount(
                variables["cost"].get(),
                expense["display_name"],
            )

        self.travel_request["per_diem"][
            "daily_rate"
        ] = self.parse_amount(
            self.daily_rate_var.get(),
            "Daily per diem rate",
        )

    def update_estimate_display(self):
        """Display calculated values from the travel model."""
        per_diem = self.travel_request["per_diem"]
        totals = self.travel_request["totals"]

        self.travel_days_var.set(
            str(per_diem["travel_days"])
        )
        self.full_rate_days_var.set(
            str(per_diem["full_rate_days"])
        )
        self.travel_rate_days_var.set(
            str(per_diem["travel_rate_days"])
        )

        self.booking_total_var.set(
            f"${totals['major_bookings']:.2f}"
        )
        self.other_total_var.set(
            f"${totals['other_expenses']:.2f}"
        )
        self.per_diem_total_var.set(
            f"${totals['per_diem']:.2f}"
        )
        self.grand_total_var.set(
            f"${totals['grand_total']:.2f}"
        )

    def calculate_estimate(self):
        """Validate the form and calculate the trip estimate."""
        try:
            self.sync_form_to_model()
            calculate_trip_totals(
                self.travel_request
            )
        except ValueError as error:
            self.status_message_var.set(
                "Unable to calculate estimate."
            )
            messagebox.showerror(
                "Unable to Calculate",
                str(error),
                parent=self.root,
            )
            return

        self.update_estimate_display()
        self.mark_modified()
        self.status_message_var.set(
            "Estimate calculated successfully."
        )

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

    def create_other_expenses_tab(self):
        """Create the additional travel-expense inputs."""
        self.other_expenses_tab.columnconfigure(
            0,
            weight=1,
        )
        self.other_expenses_tab.columnconfigure(
            2,
            weight=1,
        )

        for column in (0, 2):
            ttk.Label(
                self.other_expenses_tab,
                text="Expense",
                font=("Segoe UI", 10, "bold"),
            ).grid(
                row=0,
                column=column,
                sticky="w",
                padx=(0, 10),
                pady=(0, 10),
            )

            ttk.Label(
                self.other_expenses_tab,
                text="Cost",
                font=("Segoe UI", 10, "bold"),
            ).grid(
                row=0,
                column=column + 1,
                sticky="e",
                padx=(0, 25) if column == 0 else (0, 0),
                pady=(0, 10),
            )

        expenses = list(
            self.travel_request[
                "other_expenses"
            ].items()
        )

        left_column_count = (
            len(expenses) + 1
        ) // 2

        for index, (
            expense_key,
            expense,
        ) in enumerate(expenses):
            if index < left_column_count:
                grid_row = index + 1
                label_column = 0
                cost_column = 1
            else:
                grid_row = (
                    index - left_column_count + 1
                )
                label_column = 2
                cost_column = 3

            included_var = tk.BooleanVar(
                master=self.root,
                value=expense["included"],
            )
            cost_var = tk.StringVar(
                master=self.root,
                value=f"{expense['cost']:.2f}",
            )

            self.other_expense_vars[
                expense_key
            ] = {
                "included": included_var,
                "cost": cost_var,
            }

            include_checkbox = ttk.Checkbutton(
                self.other_expenses_tab,
                text=expense["display_name"],
                variable=included_var,
                command=self.mark_modified,
            )
            include_checkbox.grid(
                row=grid_row,
                column=label_column,
                sticky="w",
                padx=(0, 10),
                pady=6,
            )

            cost_entry = ttk.Entry(
                self.other_expenses_tab,
                textvariable=cost_var,
                width=16,
                justify="right",
            )
            cost_entry.grid(
                row=grid_row,
                column=cost_column,
                sticky="e",
                padx=(
                    (0, 25)
                    if cost_column == 1
                    else (0, 0)
                ),
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
