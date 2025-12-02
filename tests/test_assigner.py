import pytest
from src.secret_santa.assigner import SecretSantaAssigner, AssignmentError

def make_employees(n):
    return [{'name': f'Person{i}', 'email': f'p{i}@example.com'} for i in range(n)]

# ------------------------------
# Basic functionality
# ------------------------------
def test_basic_assignment():
    emps = make_employees(5)
    assigner = SecretSantaAssigner(emps)
    assignments = assigner.assign()
    assert len(assignments) == 5
    emails = {a['giver_email'] for a in assignments}
    childs = {a['child_email'] for a in assignments}
    assert emails == childs  # bijection
    for a in assignments:
        assert a['giver_email'] != a['child_email']  # no self-assignment
        # check keys exist
        assert 'giver_name' in a and 'child_name' in a

# ------------------------------
# Previous assignments constraint
# ------------------------------
def test_previous_prevents_repeat():
    emps = make_employees(4)
    prev = { 'p0@example.com': 'p1@example.com' }
    assigner = SecretSantaAssigner(emps, prev)
    assignments = assigner.assign()
    for a in assignments:
        if a['giver_email'] == 'p0@example.com':
            assert a['child_email'] != 'p1@example.com'

def test_multiple_previous_constraints():
    emps = make_employees(4)
    prev = {
        'p0@example.com': 'p1@example.com',
        'p2@example.com': 'p3@example.com'
    }
    assigner = SecretSantaAssigner(emps, prev)
    assignments = assigner.assign()
    for a in assignments:
        if a['giver_email'] in prev:
            assert a['child_email'] != prev[a['giver_email']]

# ------------------------------
# Impossible assignments
# ------------------------------
def test_impossible_assignment_raises():
    emps = [{'name':'A','email':'a@e'},{'name':'B','email':'b@e'}]
    prev = {'a@e':'b@e', 'b@e':'a@e'}
    assigner = SecretSantaAssigner(emps, prev)
    with pytest.raises(AssignmentError):
        assigner.assign()

# ------------------------------
# Minimum employee validation
# ------------------------------
def test_too_few_employees_raises():
    with pytest.raises(ValueError):
        SecretSantaAssigner([])
    with pytest.raises(ValueError):
        SecretSantaAssigner([{'name':'A','email':'a@e'}])

# ------------------------------
# Force backtracking scenario
# ------------------------------
def test_backtracking_used():
    # 4 employees where first random shuffle likely fails
    emps = make_employees(4)
    prev = {
        'p0@example.com': 'p1@example.com',
        'p1@example.com': 'p0@example.com',
        # Others free
    }
    assigner = SecretSantaAssigner(emps, prev)
    # Reduce random attempts to force deterministic search
    assignments = assigner.assign(max_random_attempts=1)
    emails = {a['giver_email'] for a in assignments}
    childs = {a['child_email'] for a in assignments}
    assert emails == childs
    for a in assignments:
        assert a['giver_email'] != a['child_email']
        if a['giver_email'] in prev:
            assert a['child_email'] != prev[a['giver_email']]

# ------------------------------
# Large-scale assignment stability
# ------------------------------
def test_large_number_of_employees():
    emps = make_employees(20)
    assigner = SecretSantaAssigner(emps)
    assignments = assigner.assign()
    emails = {a['giver_email'] for a in assignments}
    childs = {a['child_email'] for a in assignments}
    assert emails == childs
    for a in assignments:
        assert a['giver_email'] != a['child_email']

# ------------------------------
# Edge case: previous constraints allow only one valid permutation
# ------------------------------
def test_single_valid_permutation():
    emps = make_employees(3)
    prev = {
        'p0@example.com': 'p1@example.com',
        'p1@example.com': 'p2@example.com',
        'p2@example.com': 'p0@example.com'
    }
    assigner = SecretSantaAssigner(emps, prev)
    assignments = assigner.assign()
    for a in assignments:
        assert a['giver_email'] != a['child_email']
        assert a['child_email'] != prev.get(a['giver_email'], None)
