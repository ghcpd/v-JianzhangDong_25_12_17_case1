"""Utilities module for helper functions and validation.
Provides utility functions used across the application.
"""

def validate_task_title(title):
    """Validate task title format and length.
    
    Args:
        title: The task title string to validate.
    
    Returns:
        bool: True if title is valid (non-empty and at least 3 characters), False otherwise.
    """
    if not title or len(title) < 3:
        return False
    return True

def helper_function():
    """Generic helper function for utility operations.
    
    Returns:
        None
    """
    pass
