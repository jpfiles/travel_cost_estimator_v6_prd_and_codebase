"""
Application entry point for the Travel Cost Estimator.
"""

import tkinter as tk

from ui import TravelCostEstimatorApp


def main():
    """Create and run the Travel Cost Estimator application."""
    root = tk.Tk()

    app = TravelCostEstimatorApp(root)

    root.mainloop()

    return app


if __name__ == "__main__":
    main()