import sys
import traceback
import inspect
from typing import Any, Dict, List, Optional


def _frame_to_dict(frame: inspect.FrameInfo) -> Dict[str, Any]:
    return {
        "file": frame.filename,
        "function": frame.function,
        "line": frame.lineno,
        "code": frame.code_context[0].strip() if frame.code_context else None,
    }


def _get_last_error_location(exc_tb: Optional[Any]) -> Optional[Dict[str, Any]]:
    """Extract the last file and line number where the error occurred from traceback."""
    if not exc_tb:
        return None
    
    try:
        # Walk to the last frame in the traceback (where the exception actually occurred)
        last_tb = exc_tb
        while last_tb.tb_next:
            last_tb = last_tb.tb_next
        
        # Get the frame info for the last traceback entry
        frame = last_tb.tb_frame
        return {
            "file": frame.f_code.co_filename,
            "line": last_tb.tb_lineno,
            "function": frame.f_code.co_name,
        }
    except Exception:
        return None


def build_debug_info(
    request: Optional[Any] = None,
    exc: Optional[BaseException] = None,
    exc_info: Optional[tuple] = None,
    error_messages: Optional[List[Dict[str, Any]]] = None,
    request_body: Optional[Any] = None,
    middleware: Optional[str] = None,
    include_locals: bool = False,
) -> Dict[str, Any]:
    """Build a structured debug information dict for inclusion in error responses.

    - request: starlette Request (optional). We will not await on it here; pass request_body separately if needed.
    - exc: the exception instance (optional).
    - exc_info: result of sys.exc_info() if available (optional).
    - error_messages: validation error details (optional).
    - request_body: parsed request body (optional). Caller should await request.json() where needed.
    - middleware: name of middleware where error occurred (optional).
    - include_locals: when True attempt to include local variables from current frame (may be noisy).

    Returns a JSON-serializable dict.
    """
    # Determine exception info
    if exc_info:
        exc_type, exc_value, exc_tb = exc_info
    else:
        exc_type, exc_value, exc_tb = sys.exc_info()

    tb_str = None
    if exc_type:
        tb_str = traceback.format_exception(exc_type, exc_value, exc_tb)

    # Get the last error location from traceback
    last_error_location = _get_last_error_location(exc_tb)

    # Build call hierarchy from the current stack (skip the first frame which will be inside this util)
    call_hierarchy = []
    try:
        for frame in inspect.stack()[1:]:
            # Avoid showing frames inside site-packages to keep output focused on app code
            if frame.filename and "site-packages" in frame.filename:
                continue
            call_hierarchy.append(_frame_to_dict(frame))
    except Exception:
        call_hierarchy = []

    locals_snapshot = None
    if include_locals:
        try:
            locals_snapshot = {
                k: repr(v) for k, v in inspect.currentframe().f_locals.items() if not k.startswith("__")
            }
        except Exception:
            locals_snapshot = None

    debug: Dict[str, Any] = {
        "error_type": type(exc).__name__ if exc is not None else (exc_type.__name__ if exc_type else None),
        "endpoint": f"{getattr(request, 'method', None)} {getattr(request, 'url', None)}" if request is not None else None,
        "exception_message": str(exc) if exc is not None else (str(exc_value) if exc_value else None),
        "traceback": tb_str,
        "call_hierarchy": call_hierarchy,
        "request_headers": dict(request.headers) if request is not None and getattr(request, 'headers', None) is not None else None,
        "request_body": request_body,
        "validation_errors": error_messages,
        "middleware": middleware,
        "locals": locals_snapshot,
        "last_error_location": last_error_location,  # Added this field
    }

    # Remove None values for compactness
    return {k: v for k, v in debug.items() if v is not None}