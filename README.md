# Secret Santa - DigitalXC Coding Challenge

## Overview
This project implements a Secret Santa assignment system that:
- Reads an employee CSV (name + email)
- Optionally reads last year's assignments to avoid repeats
- Produces a new CSV mapping each employee to a unique secret child
- Follows constraints (no self assignment, no repeat from previous year)

## Project structure
- `src/secret_santa/assigner.py` — core OOP implementation
- `src/secret_santa/csv_handler.py` — CSV parsing & writing helpers
- `src/secret_santa/__init__.py`
- `src/main.py` — CLI entry point
- `tests/test_assigner.py` — pytest test suite
- `requirements.txt` — minimal dependencies
- `.gitignore`

## How to run
1. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate    # on Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Run the CLI (example):
   ```bash
   python -m src.main --input /path/to/employee_list.csv --output /path/to/output.csv --previous /path/to/prev.csv
   ```

## Notes
- The assignment algorithm first attempts a randomized derangement with retries.
- If a valid assignment is non-trivial (many constraints), a backtracking search is used.
- Tests cover typical and edge cases.
