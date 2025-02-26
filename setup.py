from setuptools import setup, find_packages

# Read requirements.txt using utf-16 encoding to handle the BOM correctly
with open("requirements.txt", encoding="utf-16") as f:
    install_requires = f.read().splitlines()

setup(
    name="spicecode",
    version="0.2.1",
    packages=find_packages(exclude=["spicecode-venv", "spicecode.egg-info"]),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'spice = cli.main:main',  # This tells Python to run the main function in cli.main
        ],
    },

)
