import tkinter as tk
from tkinter import ttk

from config import (
    DEFAULT_WINDOW_GEOMETRY,
    MINIMUM_WINDOW_HEIGHT,
    MINIMUM_WINDOW_WIDTH,
    WINDOW_TITLE,
)
from travel_model import create_travel_request


class TravelCostEstimatorApp:

    def __init__(self, root):
        self.root = root

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

        self.create_header()
        self.create_status_bar()

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
