#!/usr/bin/env python3
"""
HANDY REAPER - Advanced OSINT Intelligence System
Setup configuration for installation and distribution
"""

from setuptools import setup, find_packages
import os
import re

# Read the version from the main package
with open('handy_reaper/__init__.py', 'r') as f:
    version = re.search(r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read())
    if version:
        VERSION = version.group(1)
    else:
        VERSION = '1.0.0'

# Read long description from README
with open('README.md', 'r', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

# Read requirements
with open('requirements.txt', 'r') as f:
    REQUIREMENTS = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="handy-reaper",
    version=VERSION,
    author="Cyberzilla",
    author_email="contact@cyberzilla.io",
    description="Advanced OSINT Intelligence System for digital reconnaissance",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/cyberzilla/handy-reaper",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=REQUIREMENTS,
    entry_points={
        "console_scripts": [
            "handy-reaper=handy_reaper.cli:main",
            "osint-scan=handy_reaper.cli:main",
        ],
    },
    include_package_data=True,
    keywords="osint, reconnaissance, security, intelligence, social-media, scanning",
    project_urls={
        "Documentation": "https://github.com/cyberzilla/handy-reaper/wiki",
        "Source": "https://github.com/cyberzilla/handy-reaper",
        "Tracker": "https://github.com/cyberzilla/handy-reaper/issues",
    },
)
