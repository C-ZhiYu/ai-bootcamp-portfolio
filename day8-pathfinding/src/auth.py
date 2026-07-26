"""
auth.py

Simple authentication for map editing.
"""

EDITOR_PASSWORD = "admin123"


def check_password(password):
    """
    Returns True if password is correct.
    """
    return password == EDITOR_PASSWORD