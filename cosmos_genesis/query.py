"""
SQL query builder for type-safe queries
"""

from typing import List, Optional


class QueryBuilder:
    """
    Type-safe SQL query builder.

    Example:
        >>> query = (
        ...     QueryBuilder()
        ...     .select("system_id", "stellar_mass_msun")
        ...     .from_table("star")
        ...     .where("spectral_type = 'O'")
        ...     .limit(100)
        ... )
        >>> print(query.build())
        SELECT system_id, stellar_mass_msun FROM star WHERE spectral_type = 'O' LIMIT 100
    """

    def __init__(self):
        self._select_fields: List[str] = []
        self._from_table: Optional[str] = None
        self._where_conditions: List[str] = []
        self._order_by: Optional[str] = None
        self._limit: Optional[int] = None
        self._offset: Optional[int] = None

    def select(self, *fields: str) -> "QueryBuilder":
        """
        Specify SELECT fields.

        Args:
            *fields: Field names to select

        Returns:
            Self for chaining
        """
        self._select_fields.extend(fields)
        return self

    def from_table(self, table: str) -> "QueryBuilder":
        """
        Specify FROM table.

        Args:
            table: Table name (e.g., "star", "planet")

        Returns:
            Self for chaining
        """
        self._from_table = table
        return self

    def where(self, condition: str) -> "QueryBuilder":
        """
        Add WHERE condition.

        Args:
            condition: SQL condition (e.g., "stellar_mass_msun > 10")

        Returns:
            Self for chaining
        """
        self._where_conditions.append(condition)
        return self

    def order_by(self, field: str, direction: str = "ASC") -> "QueryBuilder":
        """
        Add ORDER BY clause.

        Args:
            field: Field to sort by
            direction: Sort direction ("ASC" or "DESC")

        Returns:
            Self for chaining
        """
        self._order_by = f"{field} {direction}"
        return self

    def limit(self, count: int) -> "QueryBuilder":
        """
        Set LIMIT.

        Args:
            count: Maximum number of rows to return

        Returns:
            Self for chaining
        """
        self._limit = count
        return self

    def offset(self, count: int) -> "QueryBuilder":
        """
        Set OFFSET.

        Args:
            count: Number of rows to skip

        Returns:
            Self for chaining
        """
        self._offset = count
        return self

    def build(self) -> str:
        """
        Build SQL query string.

        Returns:
            Complete SQL query

        Raises:
            ValueError: If required fields are missing
        """
        if not self._select_fields:
            raise ValueError("SELECT fields required")
        if not self._from_table:
            raise ValueError("FROM table required")

        # SELECT
        query_parts = [f"SELECT {', '.join(self._select_fields)}"]

        # FROM
        query_parts.append(f"FROM {self._from_table}")

        # WHERE
        if self._where_conditions:
            query_parts.append(f"WHERE {' AND '.join(self._where_conditions)}")

        # ORDER BY
        if self._order_by:
            query_parts.append(f"ORDER BY {self._order_by}")

        # LIMIT
        if self._limit is not None:
            query_parts.append(f"LIMIT {self._limit}")

        # OFFSET
        if self._offset is not None:
            query_parts.append(f"OFFSET {self._offset}")

        return " ".join(query_parts)

    def __str__(self) -> str:
        """String representation (builds query)."""
        return self.build()
