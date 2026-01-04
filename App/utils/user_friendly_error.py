# utils/error_handler.py
import re
import logging
from typing import Optional, Dict, Any
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from pydantic import ValidationError
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class UserFriendlyError(Exception):
    """Custom exception for user-friendly error messages"""
    def __init__(self, message: str, status_code: int = 400, details: Optional[Dict] = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

def extract_duplicate_value(error_msg: str) -> Optional[str]:
    """
    Extract duplicate value from various database error message formats
    """
    patterns = [
        r"value is \(([^)]*)\)",                    # SQL Server style
        r"duplicate key value \(([^)]*)\)",         # PostgreSQL style
        r"Duplicate entry '([^']*)'",               # MySQL style
        r"'([^']*)' already exists",                # Generic exists
        r"= '([^']*)' already exists",              # Column value style
        r"with unique.*value.*\(([^)]*)\)",         # Unique constraint with value
    ]
    
    for pattern in patterns:
        match = re.search(pattern, error_msg, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return None

def extract_constraint_name(error_msg: str) -> Optional[str]:
    """
    Extract constraint/field name from error message
    """
    patterns = [
        r"with unique (?:index|constraint) ['\"]([^'\"]+)['\"]",  # SQL Server
        r"Key \(([^)]+)\)=",                                      # PostgreSQL
        r"for key '([^']+)'",                                     # MySQL
        r"constraint ['\"]([^'\"]+)['\"]",                        # Generic constraint
    ]
    
    for pattern in patterns:
        match = re.search(pattern, error_msg, re.IGNORECASE)
        if match:
            return match.group(1)
    
    # Try to guess field from common patterns
    if "email" in error_msg.lower():
        return "email"
    elif "username" in error_msg.lower():
        return "username"
    elif "phone" in error_msg.lower():
        return "phone"
    
    return None

def get_user_friendly_message(exception: Exception) -> str:
    """
    Convert any exception to a user-friendly message
    
    Usage:
        try:
            # your code
        except Exception as e:
            user_message = get_user_friendly_message(e)
            raise HTTPException(status_code=400, detail=user_message)
    """
    
    # If it's already a user-friendly exception
    if isinstance(exception, UserFriendlyError):
        return exception.message
    
    # If it's already an HTTPException with user-friendly message
    if isinstance(exception, HTTPException):
        return exception.detail
    
    # Handle SQLAlchemy IntegrityError (duplicate keys, constraints)
    if isinstance(exception, IntegrityError):
        error_msg = str(exception.orig) if exception.orig else str(exception)
        
        if "duplicate" in error_msg.lower() or "unique constraint" in error_msg.lower():
            duplicate_value = extract_duplicate_value(error_msg)
            constraint_name = extract_constraint_name(error_msg)
            
            # Common field detection
            if "email" in error_msg.lower() or "ix_user_email" in constraint_name.lower() if constraint_name else False:
                return f"The email address '{duplicate_value}' is already registered. Please use a different email."
            
            elif "username" in error_msg.lower() or "ix_user_username" in constraint_name.lower() if constraint_name else False:
                return f"The username '{duplicate_value}' is already taken. Please choose a different one."
            
            elif "phone" in error_msg.lower():
                return f"The phone number '{duplicate_value}' is already registered."
            
            elif duplicate_value:
                return f"The value '{duplicate_value}' already exists and must be unique."
            else:
                return "This information already exists in our system. Please check your input and try again."
        
        elif "foreign key constraint" in error_msg.lower():
            return "The referenced record does not exist. Please check the related information."
        
        elif "not null constraint" in error_msg.lower():
            field = extract_constraint_name(error_msg)
            return f"The '{field}' field is required. Please provide a value."
        
        else:
            return "A database constraint was violated. Please check your input data."
    
    # Handle SQLAlchemy general errors
    if isinstance(exception, SQLAlchemyError):
        return "A database error occurred. Please try again later."
    
    # Handle Pydantic validation errors
    if isinstance(exception, ValidationError):
        errors = exception.errors()
        if errors:
            # Get the first error
            first_error = errors[0]
            field = first_error.get("loc", ["field"])[-1]
            msg = first_error.get("msg", "Invalid value")
            
            if "required" in msg.lower():
                return f"The '{field}' field is required."
            elif "string" in msg.lower() and "type" in msg.lower():
                return f"'{field}' must be text."
            elif "integer" in msg.lower():
                return f"'{field}' must be a number."
            elif "email" in msg.lower():
                return f"Please provide a valid email address for '{field}'."
            else:
                return f"Invalid value for '{field}': {msg}"
        return "The provided data is invalid. Please check your input."
    
    # Handle common Python exceptions
    if isinstance(exception, ValueError):
        return str(exception) or "An invalid value was provided."
    
    if isinstance(exception, TypeError):
        return "An unexpected error occurred with the data types."
    
    if isinstance(exception, KeyError):
        return f"Missing required information: {exception}"
    
    if isinstance(exception, AttributeError):
        return "An error occurred while processing your request."
    
    if isinstance(exception, PermissionError):
        return "You don't have permission to perform this action."
    
    if isinstance(exception, FileNotFoundError):
        return "The requested file or resource was not found."
    
    if isinstance(exception, TimeoutError):
        return "The request timed out. Please try again."
    
    if isinstance(exception, ConnectionError):
        return "Unable to connect to the service. Please check your network connection."
    
    # Generic fallback
    error_msg = str(exception)
    if error_msg:
        # Clean up technical error messages
        cleaned_msg = re.sub(r"\(.*?\)", "", error_msg)  # Remove parentheses content
        cleaned_msg = re.sub(r"'[^']*'", "", cleaned_msg)  # Remove quoted strings
        cleaned_msg = cleaned_msg.strip()
        
        if cleaned_msg and len(cleaned_msg) < 100:  # Not too long
            return cleaned_msg
    
    return "An unexpected error occurred. Please try again."

def get_error_response(exception: Exception, include_debug: bool = False) -> Dict[str, Any]:
    """
    Get complete error response for API
    
    Args:
        exception: The exception that occurred
        include_debug: Whether to include debug information (for development)
    
    Returns:
        Dict with error response
    """
    user_message = get_user_friendly_message(exception)
    
    # Determine appropriate status code
    if isinstance(exception, IntegrityError):
        if "duplicate" in str(exception).lower():
            status_code = 409  # Conflict
        else:
            status_code = 400  # Bad Request
    elif isinstance(exception, HTTPException):
        status_code = exception.status_code
    elif isinstance(exception, UserFriendlyError):
        status_code = exception.status_code
    elif isinstance(exception, ValidationError):
        status_code = 422  # Unprocessable Entity
    elif isinstance(exception, (PermissionError,)):
        status_code = 403  # Forbidden
    elif isinstance(exception, (FileNotFoundError, KeyError)):
        status_code = 404  # Not Found
    else:
        status_code = 500  # Internal Server Error
    
    response = {
        "success": False,
        "error": user_message,
        "status_code": status_code
    }
    
    # Add debug information if requested
    if include_debug:
        response.update({
            "debug": {
                "exception_type": type(exception).__name__,
                "exception_message": str(exception),
                "exception_details": repr(exception)
            }
        })
    
    # Add specific details for certain error types
    if isinstance(exception, IntegrityError) and "duplicate" in str(exception).lower():
        duplicate_value = extract_duplicate_value(str(exception))
        constraint_name = extract_constraint_name(str(exception))
        
        if duplicate_value:
            response["duplicate_value"] = duplicate_value
        if constraint_name:
            response["conflicting_field"] = constraint_name
    
    return response

def handle_exception(exception: Exception, raise_http: bool = True, include_debug: bool = False):
    """
    Handle exception and either return response or raise HTTPException
    
    Args:
        exception: The exception to handle
        raise_http: If True, raises HTTPException; if False, returns dict response
        include_debug: Include debug information
    
    Returns:
        Dict response if raise_http=False, else raises HTTPException
    """
    response = get_error_response(exception, include_debug=include_debug)
    
    if raise_http:
        raise HTTPException(
            status_code=response["status_code"],
            detail=response["error"]
        )
    
    return response