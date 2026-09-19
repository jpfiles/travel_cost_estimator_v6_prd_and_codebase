"""
Shared configuration values for the Travel Cost Estimator.
"""

APP_NAME = "Travel Cost Calculator"
APP_VERSION = "0.97_beta"
WINDOW_TITLE = f"{APP_NAME} v{APP_VERSION}"

DEFAULT_WINDOW_GEOMETRY = "1200x760"
MINIMUM_WINDOW_WIDTH = 1000
MINIMUM_WINDOW_HEIGHT = 650

DATE_FORMAT = "%m/%d/%Y"
DATE_FORMAT_DISPLAY = "MM/DD/YYYY"

PROJECTS_DIRECTORY = "projects"
REPORTS_DIRECTORY = "reports"

SUPPORTED_PROJECT_EXTENSION = ".json"
SUPPORTED_REPORT_EXTENSIONS = (
    ".txt",
    ".csv",
    ".html",
)