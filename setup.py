#!/usr/bin/env python3
"""
Media Bridge Viewer - A standalone Adobe Bridge-style media viewer
for comparing and selecting multiple media files at once.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="media-bridge-viewer",
    version="0.1.0",
    author="David Ashby",
    author_email="da@vidashby.com",
    description="Adobe Bridge-style viewer for comparing multiple media files with remote SSH support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cfomodz/media-bridge-viewer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Pillow>=8.0.0",
        "opencv-python>=4.5.0",
        "numpy>=1.21.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black",
            "flake8",
        ],
    },
    entry_points={
        "console_scripts": [
            "media-bridge=media_bridge_viewer.cli:main",
            "media-bridge-cli=media_bridge_viewer.cli_viewer:main",
            "media-bridge-remote=media_bridge_viewer.remote:main",
        ],
    },
)