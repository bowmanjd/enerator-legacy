"""setuptools configuration."""
from setuptools import find_packages, setup  # type: ignore

setup(
    name="enerator",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={"console_scripts": ["enerator=enerator.commands:main"]},
    install_requires=["cmarkgfm", "lxml", "pygments"],
    zip_safe=False,
)
