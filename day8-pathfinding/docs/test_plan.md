# Test Plan

## Objective

The objective of this test plan is to verify that the pathfinding web application functions correctly and handles both normal and invalid user inputs.

---

## Test Environment

- Operating System: Windows 11
- Python Version: 3.12
- Framework: Flask
- Testing Framework: Pytest

---

## Test Cases

| Test ID | Description | Expected Result | Status |
|----------|-------------|-----------------|--------|
| TP-001 | Correct password | Login succeeds | Pass |
| TP-002 | Incorrect password | Login denied | Pass |
| TP-003 | Valid shortest path | Path and distance returned | Pass |
| TP-004 | Start equals end | Distance is 0 | Pass |
| TP-005 | Invalid start node | ValueError raised | Pass |
| TP-006 | Invalid end node | ValueError raised | Pass |
| TP-007 | Invalid start and end nodes | ValueError raised | Pass |

---

## Test Execution

Run all tests using:

```bash
python -m pytest
```

Expected Result:

```
7 passed
```

---

## Conclusion

All implemented unit tests passed successfully. The application correctly computes shortest paths, validates inputs, and authenticates editor access.