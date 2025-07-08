#!/usr/bin/env python3
"""
Setup script for NOTAM System
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

# Get version
def get_version():
    """Get version from __init__.py"""
    version_file = os.path.join("src", "__init__.py")
    if os.path.exists(version_file):
        with open(version_file, "r") as f:
            for line in f:
                if line.startswith("__version__"):
                    return line.split("=")[1].strip().strip('"').strip("'")
    return "2.0.0"

setup(
    name="notam-system",
    version=get_version(),
    author="Isidoro Reyes",
    author_email="tu-email@ejemplo.com",
    description="Sistema de gestión y procesamiento de NOTAMs (Notice to Airmen)",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/isidororeyes/NOTAM",
    project_urls={
        "Bug Tracker": "https://github.com/isidororeyes/NOTAM/issues",
        "Documentation": "https://github.com/isidororeyes/NOTAM/wiki",
        "Source Code": "https://github.com/isidororeyes/NOTAM",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.991",
            "pre-commit>=2.20.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
        "gui": [
            "PyQt5>=5.15.0",
        ],
        "web": [
            "flask>=2.2.0",
            "flask-restful>=0.3.9",
        ],
    },
    entry_points={
        "console_scripts": [
            "notam=src.main.app:main",
            "notam-parser=src.parsers.notam_parser:main",
            "notam-validator=src.validators.notam_validator:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": [
            "data/samples/*.txt",
            "data/templates/*.html",
            "config/*.json",
        ],
    },
    zip_safe=False,
    keywords="notam aviation airmen notice parser validator",
    platforms=["any"],
)