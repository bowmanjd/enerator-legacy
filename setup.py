"""setuptools configuration."""
from setuptools import setup, find_packages

setup(
    name="enerator",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={"console_scripts": ["enerator=enerator:run"]},
    install_requires=["cmarkgfm", "lxml", "pygments"],
)
