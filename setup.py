"""setuptools configuration."""
from setuptools import find_packages, setup  # type: ignore

setup(
    name="enerator",
    version="0.2",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={"console_scripts": ["enerator=enerator.commands:main"]},
    install_requires=["cmarkgfm", "pygments", "uvicorn", "watchgod"],
    zip_safe=False,
)
