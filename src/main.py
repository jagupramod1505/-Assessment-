import sys
from secret_santa.csv_handler import read_employees, read_previous_assignments, write_assignments
from secret_santa.assigner import SecretSantaAssigner, AssignmentError

# FIXED PATHS (your requirement)
EMPLOYEE_CSV = r"C:\secret_santa\data\current.csv"
PREVIOUS_CSV = r"C:\secret_santa\data\previous.csv"
OUTPUT_CSV   = r"C:\secret_santa\data\result.csv"

def main():
    # Read current year employees
    employees = read_employees(EMPLOYEE_CSV)
    if not employees:
        print("No employees found in current.csv", file=sys.stderr)
        sys.exit(2)

    # Read last year's assignments (optional file)
    prev = {}
    try:
        prev = read_previous_assignments(PREVIOUS_CSV)
    except Exception:
        prev = {}

    try:
        # Perform Secret Santa assignment
        assigner = SecretSantaAssigner(employees, prev)
        assignments = assigner.assign()

        # Save result
        write_assignments(OUTPUT_CSV, assignments)

        print(f"Success! Generated {len(assignments)} Secret Santa pairs.")
        print(f"Output saved to: {OUTPUT_CSV}")

    except AssignmentError as e:
        print("Assignment failed:", e, file=sys.stderr)
        sys.exit(3)
    except Exception as e:
        print("Error:", e, file=sys.stderr)
        sys.exit(4)

if __name__ == "__main__":
    main()
