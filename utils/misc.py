"""
Miscellaneous utility functions
"""


def conditional_print(is_quiet: bool, *args, **kwargs):
    """
    Print if not quiet
    """
    if not is_quiet:
        print(*args, **kwargs)
