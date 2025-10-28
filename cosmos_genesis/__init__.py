"""
Cosmos Genesis Python SDK

Official Python client for querying Universe-as-a-Service data.
"""

from .client import CosmosClient, AsyncCosmosClient
from .query import QueryBuilder
from .exceptions import (
    CosmosError,
    AuthenticationError,
    QueryError,
    SchemaNotFoundError,
)

__version__ = "0.1.0"
__all__ = [
    "CosmosClient",
    "AsyncCosmosClient",
    "QueryBuilder",
    "CosmosError",
    "AuthenticationError",
    "QueryError",
    "SchemaNotFoundError",
]
