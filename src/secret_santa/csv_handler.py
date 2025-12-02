import csv
from typing import List, Dict

def read_employees(csv_path: str) -> List[Dict[str,str]]:
    """Read employees CSV. Expects header with Employee_Name, Employee_EmailID"""
    employees = []
    with open(csv_path, newline='', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        for r in reader:
            # Normalize keys
            name = r.get('Employee_Name') or r.get('Name') or r.get('employee_name')
            email = r.get('Employee_EmailID') or r.get('Email') or r.get('employee_emailid')
            if not name or not email:
                continue
            employees.append({'name': name.strip(), 'email': email.strip()})
    return employees

def read_previous_assignments(csv_path: str) -> Dict[str,str]:
    """Read previous assignments and return mapping giver_email -> child_email"""
    prev = {}
    with open(csv_path, newline='', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        for r in reader:
            giver = r.get('Employee_EmailID') or r.get('Employee_Email') or r.get('giver_email')
            child = r.get('Secret_Child_EmailID') or r.get('Secret_Child_Email') or r.get('child_email')
            if giver and child:
                prev[giver.strip()] = child.strip()
    return prev

def write_assignments(output_path: str, assignments: List[Dict[str,str]]):
    fieldnames = ['Employee_Name', 'Employee_EmailID', 'Secret_Child_Name', 'Secret_Child_EmailID']
    with open(output_path, 'w', newline='', encoding='utf-8') as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in assignments:
            writer.writerow({
                'Employee_Name': row['giver_name'],
                'Employee_EmailID': row['giver_email'],
                'Secret_Child_Name': row['child_name'],
                'Secret_Child_EmailID': row['child_email'],
            })
