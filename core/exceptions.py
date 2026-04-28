class OANException(Exception):
    """Base exception class for OSINT Agent Network."""
    pass

class LLMAPIError(OANException):
    """Raised when an LLM API call fails."""
    pass

class DataCollectionError(OANException):
    """Raised when data collection from a source fails."""
    pass

class ValidationError(OANException):
    """Raised when intelligence validation fails."""
    pass
