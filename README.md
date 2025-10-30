# Cosmos Genesis Python SDK

**Official Python client for querying Universe-as-a-Service data**

**COMING SOON!**

[![PyPI version](https://img.shields.io/pypi/v/cosmos-genesis-client.svg)](https://pypi.org/project/cosmos-genesis-client/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green)](LICENSE)

## Quick Start

### Installation

```bash
pip install cosmos-genesis-client
```

### Basic Usage

```python
from cosmos_genesis import CosmosClient

# Initialize client with API key
client = CosmosClient(api_key="your_api_key_here")

# Query star data
stars = client.query_galaxy(
    galaxy_id="spiral-sm-2arm-001",
    query="SELECT * FROM star WHERE stellar_mass_msun > 10 LIMIT 100"
)

# Analyze results
for star in stars:
    print(f"{star['system_id']}: {star['stellar_mass_msun']} M☉")
```

## Features

- **Simple API** - Query trillion-object datasets with standard SQL
- **Reproducible** - Deterministic seeding ensures identical results
- **Type-safe** - Full type hints for IDE autocomplete
- **Async support** - Built-in async/await for concurrent queries
- **Pandas integration** - Direct conversion to DataFrames
- **Schema validation** - Automatic validation against 89 open-source schemas

## Authentication

### Getting API Keys

1. Sign up at [cosmosgenesis.com](https://cosmosgenesis.com/#beta-signup)
2. Receive API key via email
3. Set environment variable:

```bash
export COSMOS_API_KEY="your_api_key_here"
```

Or pass directly to client:

```python
client = CosmosClient(api_key="your_api_key_here")
```

## Examples

### Query Builder

```python
from cosmos_genesis import CosmosClient, QueryBuilder

client = CosmosClient()

# Use query builder for type-safe queries
query = (
    QueryBuilder()
    .select("system_id", "stellar_mass_msun", "age_myr")
    .from_table("star")
    .where("spectral_type = 'O'")
    .where("stellar_mass_msun > 20")
    .limit(100)
)

results = client.execute(query, galaxy_id="spiral-sm-2arm-001")
```

### Pandas Integration

```python
import pandas as pd

# Get results as DataFrame
df = client.query_to_dataframe(
    galaxy_id="spiral-sm-2arm-001",
    query="SELECT * FROM star WHERE stellar_mass_msun > 10"
)

# Analyze with pandas
print(df.describe())
print(df.groupby('spectral_type')['stellar_mass_msun'].mean())
```

### Async Queries

```python
import asyncio
from cosmos_genesis import AsyncCosmosClient

async def analyze_multiple_galaxies():
    client = AsyncCosmosClient()

    queries = [
        client.query_galaxy("galaxy-001", "SELECT COUNT(*) FROM star"),
        client.query_galaxy("galaxy-002", "SELECT COUNT(*) FROM star"),
        client.query_galaxy("galaxy-003", "SELECT COUNT(*) FROM star"),
    ]

    results = await asyncio.gather(*queries)
    return results

# Run async queries
results = asyncio.run(analyze_multiple_galaxies())
```

## Example Notebooks

The `examples/notebooks/` directory contains Jupyter notebooks demonstrating:

1. **[01_quickstart.ipynb](examples/notebooks/01_quickstart.ipynb)** - Basic queries and setup
2. **[02_imf_analysis.ipynb](examples/notebooks/02_imf_analysis.ipynb)** - Validate Kroupa IMF
3. **[03_stellar_evolution.ipynb](examples/notebooks/03_stellar_evolution.ipynb)** - Track stars over time
4. **[04_exoplanet_stats.ipynb](examples/notebooks/04_exoplanet_stats.ipynb)** - Population synthesis

Run notebooks locally:

```bash
git clone https://github.com/cosmosgenesis/cosmos-python-sdk.git
cd cosmos-python-sdk
pip install -e ".[dev]"
jupyter lab examples/notebooks/
```

## API Reference

### CosmosClient

```python
class CosmosClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        region: str = "us-east-1",
        timeout: int = 300
    ):
        """Initialize Cosmos Genesis API client."""

    def query_galaxy(
        self,
        galaxy_id: str,
        query: str,
        universe_time: int = 0
    ) -> List[Dict[str, Any]]:
        """Execute SQL query against galaxy data."""

    def list_galaxies(self) -> List[Dict[str, Any]]:
        """List all available galaxies."""

    def get_schema(self, schema_name: str) -> Dict[str, Any]:
        """Get Avro schema definition."""

    def query_to_dataframe(
        self,
        galaxy_id: str,
        query: str
    ) -> pd.DataFrame:
        """Execute query and return pandas DataFrame."""
```

### QueryBuilder

```python
class QueryBuilder:
    def select(*fields: str) -> QueryBuilder:
        """Specify SELECT fields."""

    def from_table(table: str) -> QueryBuilder:
        """Specify FROM table."""

    def where(condition: str) -> QueryBuilder:
        """Add WHERE condition."""

    def limit(count: int) -> QueryBuilder:
        """Set LIMIT."""

    def build() -> str:
        """Build SQL query string."""
```

## Schema Reference

All 89 schemas are documented at:

**[cosmos-schemas GitHub Repository](https://github.com/cosmosgenesis/cosmos-schemas)**

Common tables:
- `star` - Main sequence stars with spectral types
- `planet` - Exoplanets with orbital parameters
- `moon` - Natural satellites
- `asteroid` - Individual asteroids
- `asteroidbelt` - Asteroid belt regions
- `blackhole` - Black holes and accretion disks
- `nebula` - Emission/reflection nebulae

## Development

### Setup

```bash
git clone https://github.com/cosmosgenesis/cosmos-python-sdk.git
cd cosmos-python-sdk
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest tests/
pytest --cov=cosmos_genesis tests/
```

### Type Checking

```bash
mypy cosmos_genesis/
```

## Support

- **Documentation**: [docs.cosmosgenesis.com](https://docs.cosmosgenesis.com)
- **Issues**: [GitHub Issues](https://github.com/cosmosgenesis/cosmos-python-sdk/issues)
- **Email**: info@cosmosgenesis.com
- **Research**: founder@cosmosgenesis.com

## Citation

```bibtex
@software{cosmosgenesis_sdk2025,
  author = {Edwards, Shawn},
  title = {Cosmos Genesis Python SDK},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/cosmosgenesis/cosmos-python-sdk}
}
```

## License

Apache License 2.0 - See [LICENSE](LICENSE)

---

**Cosmos Genesis™** - *We build the universe. You build the worlds.™*
