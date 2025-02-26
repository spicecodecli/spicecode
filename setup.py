from setuptools import setup, find_packages

setup(
    name="spicecode",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer[all]",
        "rich",
        # ... list any other dependencies here
    ],
    entry_points={
        "console_scripts": [
            "spice=cli.main:app",
        ],
    },
)
