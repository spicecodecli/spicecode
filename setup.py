from setuptools import setup, find_packages

# Read requirements.txt using utf-16 encoding to handle the BOM correctly
with open("requirements.txt", encoding="utf-16") as f:
    install_requires = f.read().splitlines()

# Read the README.md for PyPI long description
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="spicecode",
    version="2.1.5",  # Version 2.0.0 = all features from N2
    packages=find_packages(exclude=["spicecode-venv", "spicecode.egg-info"]),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'spice = cli.main:main',  # Entry point for CLI
        ],
    },
    description="SpiceCode: The next generation of code analysis.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="SpiceCodeCLI",
    author_email="spicecodecli@gmail.com",
    url="https://github.com/spicecodecli/spicecode",
    license="Apache-2.0",  # Specify the license
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Optional but good practice
)
