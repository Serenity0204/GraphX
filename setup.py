from setuptools import setup, find_packages

setup(
    name="linnngraphx",
    version="0.3",
    packages=find_packages(),
    package_dir={"linnngraphx": "graphx"},
    install_requires=[],
    description="GraphX is a Python-based in-memory graph storage engine designed to facilitate the representation of complex relational queries, enabling users to store data while effectively capturing relationships between individual data points.",
)
