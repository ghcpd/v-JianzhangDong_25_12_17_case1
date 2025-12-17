"""Internal test module for verifying docstrings."""

import sys

def verify_docstrings():
    """Verify that all required docstrings are present.
    
    Returns:
        bool: True if all docstrings are present, False otherwise.
    """
    import inspect
    import api
    import app
    import config
    import utils
    import tasks

    errors = []

    # Check api.py
    if not api.__doc__:
        errors.append('api.py: Missing module docstring')
    if not api.internal_helper.__doc__:
        errors.append('api.py: internal_helper() missing docstring')

    # Check app.py
    if not app.__doc__:
        errors.append('app.py: Missing module docstring')

    # Check config.py
    if not config.__doc__:
        errors.append('config.py: Missing module docstring')

    # Check utils.py
    if not utils.__doc__:
        errors.append('utils.py: Missing module docstring')
    if not utils.validate_task_title.__doc__:
        errors.append('utils.py: validate_task_title() missing docstring')
    if not utils.helper_function.__doc__:
        errors.append('utils.py: helper_function() missing docstring')

    # Check tasks.py
    if not tasks.__doc__:
        errors.append('tasks.py: Missing module docstring')
    if not tasks.Task.__doc__:
        errors.append('tasks.py: Task class missing docstring')
    if not tasks.TaskManager.__doc__:
        errors.append('tasks.py: TaskManager class missing docstring')

    if errors:
        for error in errors:
            print(f'ERROR: {error}')
        return False
    else:
        print('All docstrings verified successfully')
        return True

if __name__ == '__main__':
    success = verify_docstrings()
    sys.exit(0 if success else 1)
