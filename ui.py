import tkinter as tk
from tkinter import ttk

from travel_model import create_travel_request


class TravelCostEstimatorApp:

    def __init__(self, root):
        self.root = root

        self.root.title("Travel Cost Estimator")
        self.root.geometry("1200x760")
        self.root.minsize(1000, 650)

        self.travel_request = create_travel_request()

        self.current_file_path = None
        self.is_modified = False

        self.project_status_var = tk.StringVar(
            value="Project: Unsaved"
        )

        self.status_message_var = tk.StringVar(
            value="Ready."
        )

        self.create_header()

    def create_header(self):
        """
        Create the title, project status, and subtitle.
        """

        header_frame = ttk.Frame(
            self.root,
            padding=(20, 15, 20, 10)
        )

        header_frame.pack(fill="x")

        header_frame.columnconfigure(0, weight=1)   

def main():

    root = tk.Tk()

    app = TravelCostEstimatorApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()