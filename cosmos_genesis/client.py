"""
Main client for Cosmos Genesis API
"""

import os
import time
from typing import Dict, List, Any, Optional
import boto3
import requests

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

from .exceptions import AuthenticationError, QueryError, SchemaNotFoundError


class CosmosClient:
    """
    Client for querying Cosmos Genesis universe data.

    Uses AWS Athena for SQL queries against Iceberg tables.
    Requires either API key or AWS credentials.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        region: str = "us-east-1",
        timeout: int = 300,
        database: str = "cosmological_production",
    ):
        """
        Initialize Cosmos Genesis client.

        Args:
            api_key: Cosmos Genesis API key (or set COSMOS_API_KEY env var)
            region: AWS region (default: us-east-1)
            timeout: Query timeout in seconds (default: 300)
            database: Glue database name (default: cosmological_production)
        """
        self.api_key = api_key or os.environ.get("COSMOS_API_KEY")
        if not self.api_key:
            raise AuthenticationError(
                "API key required. Pass api_key parameter or set COSMOS_API_KEY environment variable."
            )

        self.region = region
        self.timeout = timeout
        self.database = database

        # Initialize AWS Athena client
        self.athena = boto3.client("athena", region_name=region)
        self.s3 = boto3.client("s3", region_name=region)

        # Results bucket (should be provided by API key validation)
        self.results_bucket = f"cosmos-query-results-{region}"

    def list_galaxies(self) -> List[Dict[str, Any]]:
        """
        List all available galaxies.

        Returns:
            List of galaxy metadata dictionaries
        """
        query = f"""
        SELECT DISTINCT
            galaxy_id,
            COUNT(*) as system_count
        FROM {self.database}.starsystem
        GROUP BY galaxy_id
        ORDER BY galaxy_id
        """

        results = self._execute_query(query)
        return [
            {
                "galaxy_id": row[0],
                "system_count": int(row[1]),
            }
            for row in results
        ]

    def query_galaxy(
        self,
        galaxy_id: str,
        query: str,
        universe_time: int = 0,
    ) -> List[Dict[str, Any]]:
        """
        Execute SQL query against galaxy data.

        Args:
            galaxy_id: Galaxy identifier (e.g., "spiral-sm-2arm-001")
            query: SQL query string
            universe_time: Universe time in Myr (default: 0)

        Returns:
            List of result rows as dictionaries

        Example:
            >>> client.query_galaxy(
            ...     "spiral-sm-2arm-001",
            ...     "SELECT * FROM star WHERE stellar_mass_msun > 10 LIMIT 100"
            ... )
        """
        # Inject galaxy_id filter if not present
        if "WHERE" in query.upper():
            query = query.replace("WHERE", f"WHERE galaxy_id = '{galaxy_id}' AND", 1)
        else:
            # Add WHERE clause before LIMIT/ORDER BY if present
            for keyword in ["LIMIT", "ORDER BY", "GROUP BY"]:
                if keyword in query.upper():
                    query = query.replace(
                        keyword, f"WHERE galaxy_id = '{galaxy_id}' {keyword}", 1
                    )
                    break
            else:
                # No LIMIT/ORDER BY, append WHERE at end
                query = f"{query} WHERE galaxy_id = '{galaxy_id}'"

        # Add universe_time filter
        if universe_time > 0:
            query = query.replace(
                f"galaxy_id = '{galaxy_id}'",
                f"galaxy_id = '{galaxy_id}' AND universe_time = {universe_time}",
            )

        results = self._execute_query(query)

        # Convert to list of dicts (column names from query)
        return self._rows_to_dicts(results, query)

    def query_to_dataframe(
        self,
        galaxy_id: str,
        query: str,
        universe_time: int = 0,
    ) -> "pd.DataFrame":
        """
        Execute query and return results as pandas DataFrame.

        Args:
            galaxy_id: Galaxy identifier
            query: SQL query string
            universe_time: Universe time in Myr (default: 0)

        Returns:
            pandas DataFrame with query results

        Raises:
            ImportError: If pandas is not installed
        """
        if not HAS_PANDAS:
            raise ImportError(
                "pandas is required for query_to_dataframe(). Install with: pip install pandas"
            )

        results = self.query_galaxy(galaxy_id, query, universe_time)
        return pd.DataFrame(results)

    def get_schema(self, schema_name: str) -> Dict[str, Any]:
        """
        Get Avro schema definition.

        Args:
            schema_name: Schema name (e.g., "Star", "Planet")

        Returns:
            Schema definition dictionary

        Raises:
            SchemaNotFoundError: If schema doesn't exist
        """
        # TODO: Fetch from cosmos-schemas GitHub repo
        raise NotImplementedError("Schema fetching not yet implemented")

    def _execute_query(self, query: str) -> List[tuple]:
        """
        Execute Athena query and return raw results.

        Args:
            query: SQL query string

        Returns:
            List of result tuples

        Raises:
            QueryError: If query fails
        """
        try:
            # Start query execution
            response = self.athena.start_query_execution(
                QueryString=query,
                QueryExecutionContext={"Database": self.database},
                ResultConfiguration={
                    "OutputLocation": f"s3://{self.results_bucket}/queries/"
                },
            )

            query_id = response["QueryExecutionId"]

            # Wait for query to complete
            start_time = time.time()
            while True:
                status = self.athena.get_query_execution(QueryExecutionId=query_id)
                state = status["QueryExecution"]["Status"]["State"]

                if state == "SUCCEEDED":
                    break
                elif state in ["FAILED", "CANCELLED"]:
                    reason = status["QueryExecution"]["Status"].get(
                        "StateChangeReason", "Unknown error"
                    )
                    raise QueryError(f"Query failed: {reason}")

                if time.time() - start_time > self.timeout:
                    raise QueryError(f"Query timeout after {self.timeout}s")

                time.sleep(1)

            # Fetch results
            results = []
            paginator = self.athena.get_paginator("get_query_results")
            for page in paginator.paginate(QueryExecutionId=query_id):
                for row in page["ResultSet"]["Rows"][1:]:  # Skip header
                    results.append(tuple(col.get("VarCharValue") for col in row["Data"]))

            return results

        except Exception as e:
            if isinstance(e, (QueryError, AuthenticationError)):
                raise
            raise QueryError(f"Query execution failed: {str(e)}")

    def _rows_to_dicts(self, rows: List[tuple], query: str) -> List[Dict[str, Any]]:
        """
        Convert result tuples to dictionaries.

        Args:
            rows: List of result tuples
            query: Original query (to extract column names)

        Returns:
            List of dictionaries
        """
        # Simple column name extraction (could be improved)
        # For now, use generic col1, col2, etc.
        if not rows:
            return []

        num_cols = len(rows[0])
        col_names = [f"col{i}" for i in range(num_cols)]

        return [dict(zip(col_names, row)) for row in rows]


class AsyncCosmosClient:
    """
    Async version of CosmosClient (placeholder for future implementation).
    """

    def __init__(self, *args, **kwargs):
        raise NotImplementedError("Async client not yet implemented")
