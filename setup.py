"""Setup configuration for Cosmos Genesis Python SDK"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8")

setup(
    name="cosmos-genesis-client",
    version="0.1.0",
    description="Official Python client for Cosmos Genesis Universe-as-a-Service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Shawn Edwards",
    author_email="info@cosmosgenesis.com",
    url="https://github.com/cosmosgenesis/cosmos-python-sdk",
    project_urls={
        "Homepage": "https://cosmosgenesis.com",
        "Documentation": "https://docs.cosmosgenesis.com",
        "Source": "https://github.com/cosmosgenesis/cosmos-python-sdk",
        "Tracker": "https://github.com/cosmosgenesis/cosmos-python-sdk/issues",
    },
    packages=find_packages(exclude=["tests", "examples"]),
    python_requires=">=3.9",
    install_requires=[
        "boto3>=1.26.0",
        "requests>=2.28.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.2.0",
            "pytest-cov>=4.0.0",
            "mypy>=1.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "jupyter>=1.0.0",
            "notebook>=6.5.0",
        ],
        "pandas": [
            "pandas>=1.5.0",
        ],
        "all": [
            "pandas>=1.5.0",
            "matplotlib>=3.6.0",
            "numpy>=1.24.0",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="astrophysics astronomy universe simulation cosmos-genesis",
    license="Apache-2.0",
    zip_safe=False,
)
