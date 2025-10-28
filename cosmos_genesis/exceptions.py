"""
Exception classes for Cosmos Genesis SDK
"""


class CosmosError(Exception):
    """Base exception for all Cosmos Genesis errors."""
    pass


class AuthenticationError(CosmosError):
    """Raised when API key is invalid or missing."""
    pass


class QueryError(CosmosError):
    """Raised when SQL query fails."""
    pass


class SchemaNotFoundError(CosmosError):
    """Raised when requested schema doesn't exist."""
    pass


class TimeoutError(CosmosError):
    """Raised when query exceeds timeout."""
    pass
