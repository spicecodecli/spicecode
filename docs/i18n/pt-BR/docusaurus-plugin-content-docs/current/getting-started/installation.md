---
sidebar_position: 1
---

# Installation Guide

Embarking on your journey with SpiceCode requires preparing your development environment, much like a Fremen meticulously readies their gear before venturing into the vast deserts of Arrakis. This guide provides detailed instructions to ensure SpiceCode is correctly installed and ready for use on your system. The installation process is designed to be straightforward, leveraging standard Python package management tools.

## Prerequisites

Before you can install SpiceCode, there are a couple of essential prerequisites that must be met. Firstly, you need a working installation of Python on your system. SpiceCode is built upon Python, making it a fundamental requirement, akin to the necessity of water for life in the desert. Ensure that Python is not only installed but also correctly configured in your system's PATH environment variable, allowing you to execute Python commands from your terminal. Secondly, you will need access to a command-line terminal or prompt. This interface serves as your primary means of interacting with SpiceCode, your personal thopter for navigating the complexities of your codebase. Most operating systems (Windows, macOS, Linux) provide a built-in terminal application.

## Standard Installation using PIP

The most common and recommended method for installing SpiceCode is by using PIP, the standard package installer for Python. This method fetches the latest stable release directly from the Python Package Index (PyPI) and handles the installation process automatically. Open your terminal and execute the following command:

```bash
pip install spicecode
```

Executing this command instructs PIP to download the SpiceCode package and its dependencies, installing them into your Python environment. Upon successful completion, the `spice` command should become available in your terminal session, ready to be invoked like a Fremen drawing their crysknife – swift and precise.

## Installation from Source Code

For developers who prefer to build the tool directly from its source code, perhaps for development purposes or to access the very latest, unreleased changes, installation from the source repository is also possible. This process mirrors the Fremen tradition of crafting their own tools and equipment from available resources.

First, you need to obtain a local copy of the source code. Clone the official SpiceCode repository from GitHub using Git:

```bash
git clone https://github.com/spicecodecli/spicecode.git
```

Once the repository is cloned, navigate into the newly created `spicecode` directory using your terminal:

```bash
cd spicecode
```

It is highly recommended to create and activate a Python virtual environment within this directory. Virtual environments provide isolation, preventing conflicts between project dependencies and your global Python installation. Create a virtual environment named `venv` (or any name you prefer):

```bash
python -m venv venv
```

Activate the virtual environment. The activation command differs slightly depending on your operating system:

On **Windows** (using Command Prompt or PowerShell):
```bash
.\venv\Scripts\activate
```

On **Linux or macOS** (using bash or zsh):
```bash
source ./venv/bin/activate
```

With the virtual environment active (you should see its name, like `(venv)`, prepended to your terminal prompt), install the necessary dependencies listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

Finally, install SpiceCode in "editable" mode. This mode links the installed package directly to your source code directory, meaning any changes you make to the code are immediately reflected when you run the `spice` command, without needing to reinstall.

```bash
pip install -e .
```

Following these steps ensures that you have a development-ready installation of SpiceCode, built directly from the source, empowering you to explore and potentially contribute to its evolution.

## Verifying the Installation

Regardless of the installation method chosen, it is crucial to verify that SpiceCode has been installed correctly and is accessible from your terminal. Execute the version command:

```bash
spice version
```

If the installation was successful, this command will output the currently installed version number of SpiceCode. Seeing this confirmation signifies that the spice is indeed flowing through your system, and you are prepared to begin analyzing your code with the power and precision of a seasoned desert navigator.
