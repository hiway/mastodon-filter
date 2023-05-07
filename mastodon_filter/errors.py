"""
Error handling utilities.
"""


def extract_error_message(error: Exception) -> str:
    """
    Extract error message from exception.
    """
    try:
        if len(str(error)) > 250:
            return error.args[0][:250] + "..."
        else:
            return error.args[0]
    except Exception:
        return str(error)
