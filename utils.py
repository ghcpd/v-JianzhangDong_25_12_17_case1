"""Utility functions."""

def validate_task_title(title):
    """Validate if the task title is valid."""
    if not title or len(title) < 3:
        return False
    return True

def helper_function():
    """A helper function."""
    pass
