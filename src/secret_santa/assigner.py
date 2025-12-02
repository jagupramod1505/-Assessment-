import random
from typing import List, Dict, Optional, Tuple

class AssignmentError(Exception):
    pass

class SecretSantaAssigner:
    """Assign secret children to employees.

    Usage:
        assigner = SecretSantaAssigner(employees, previous_map)
        assignments = assigner.assign()
    """
    def __init__(self, employees: List[Dict[str,str]], previous: Optional[Dict[str,str]] = None):
        # employees: list of {'name','email'}
        if not employees or len(employees) < 2:
            raise ValueError('Need at least 2 employees to play Secret Santa.')
        self.employees = employees
        self.previous = previous or {}
        # maps for quick lookup
        self.email_to_name = {e['email']: e['name'] for e in employees}

    def assign(self, max_random_attempts: int = 5000) -> List[Dict[str,str]]:
        """Return list of assignment dicts with keys: giver_name, giver_email, child_name, child_email"""
        givers = [e['email'] for e in self.employees]
        receivers = [e['email'] for e in self.employees]

        # Quick randomized attempt: try shuffling receivers to get a valid derangement obeying previous.
        for attempt in range(max_random_attempts):
            random.shuffle(receivers)
            ok = True
            for g, r in zip(givers, receivers):
                if g == r:
                    ok = False
                    break
                prev_child = self.previous.get(g)
                if prev_child and prev_child == r:
                    ok = False
                    break
            if ok:
                return self._format_assignments(givers, receivers)

        # If random attempts fail, try deterministic backtracking search
        assignments = self._backtracking_search(givers, receivers)
        if assignments is None:
            raise AssignmentError('No valid Secret Santa assignment found with constraints.')
        return self._format_assignments(givers, assignments)

    def _format_assignments(self, givers: List[str], receivers: List[str]) -> List[Dict[str,str]]:
        out = []
        for g, r in zip(givers, receivers):
            out.append({
                'giver_name': self.email_to_name[g],
                'giver_email': g,
                'child_name': self.email_to_name[r],
                'child_email': r,
            })
        return out

    def _backtracking_search(self, givers: List[str], receivers: List[str]) -> Optional[List[str]]:
        """Backtracking search to find a valid permutation of receivers matching givers."""
        used = set()
        result = [None] * len(givers)

        # Precompute forbidden sets per giver (self + previous child if any)
        forbidden = {}
        for i, g in enumerate(givers):
            forb = {g}
            prev = self.previous.get(g)
            if prev:
                forb.add(prev)
            forbidden[g] = forb

        # Order givers by least options heuristic
        order = list(range(len(givers)))
        order.sort(key=lambda i: len(forbidden[givers[i]]))

        def backtrack(idx):
            if idx == len(order):
                return True
            i = order[idx]
            g = givers[i]
            for r in receivers:
                if r in used:
                    continue
                if r in forbidden[g]:
                    continue
                used.add(r)
                result[i] = r
                if backtrack(idx + 1):
                    return True
                used.remove(r)
                result[i] = None
            return False

        if backtrack(0):
            return result
        return None
