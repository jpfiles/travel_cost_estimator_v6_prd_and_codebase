# Travel Cost Estimator v0.96 Beta

Travel Cost Estimator is a Python desktop application for estimating official travel costs, calculating per diem, saving travel projects, and exporting cost reports.

This repository contains the Version 6 codebase for the v0.96 beta application.

## Features

- Traveler and destination information
- Departure and return dates
- Automatic travel-day calculation
- Manual daily per diem rate
- 75 percent per diem for the first and last travel days
- Major booking expenses:
  - Airfare
  - Hotel
  - Rental car
- Additional travel expenses:
  - POV mileage
  - Rental car fuel
  - Baggage fees
  - Hotel taxes
  - Resort fees
  - Tolls
  - ADTRAV fees
  - Airport parking
  - Hotel parking
  - Uber and taxi services
  - Miscellaneous expenses
- Major-booking subtotal
- Other-expense subtotal
- Per-diem subtotal
- Estimated grand total
- JSON project save and reopen
- TXT report export
- CSV report export
- HTML report export
- Unsaved-change warnings
- System-compatible Tkinter interface

## Requirements

- Python 3.10 or newer
- Tkinter
- Windows 10 or Windows 11

The application uses only the Python standard library. No third-party runtime packages are required.

## Running the Application

Open PowerShell in the project directory and run:

```powershell
python main.py