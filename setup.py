"""Setup script for the self-driving car project."""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="self-driving-car-ml",
    version="1.0.0",
    author="ThatOneGuyIDK",
    description="A self-driving car simulation using machine learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ThatOneGuyIDK/First-Predictive-AI-model-",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pygame>=2.5.0",
        "numpy>=1.24.0",
        "torch>=2.0.0",
        "matplotlib>=3.7.0",
    ],
)
