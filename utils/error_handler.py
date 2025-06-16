import requests

def handle_errors(error):
    """User-friendly error messages with learning capability"""
    error_type = type(error).__name__
    
    # Handle specific errors
    if isinstance(error, requests.exceptions.ConnectionError):
        return "🔌 Connection lost. Please check your internet and try again."
    
    elif isinstance(error, requests.exceptions.Timeout):
        return "⏳ Request timed out. The server is busy - try a simpler question."
    
    elif "rate limit" in str(error).lower():
        return "🚦 Too many requests. Please wait a moment and try again."
    
    elif "authentication" in str(error).lower():
        return "🔑 API authentication issue. This has been reported to our team."
    
    # Fallback to general error
    return f"⚠️ Climate insight unavailable. Error: {error_type}. We're working to fix this!"

def should_fallback(error):
    """Determine if we should use fallback response"""
    error_str = str(error).lower()
    
    # Conditions where fallback is appropriate
    fallback_conditions = [
        "connection",
        "timeout",
        "rate limit",
        "server error",
        "502",
        "503",
        "504"
    ]
    
    return any(cond in error_str for cond in fallback_conditions)
