# 🌶️ SpiceCode CLI - Making your code spicier 🔥🥵

## Installing via PIP

- Make sure you have Python installed on your system
- Open the terminal
- Install SpiceCode via PIP with:

```bash
pip install spicecode
```

### Using SpiceCode

- After installing via PIP, you can run these three commands: *(replace file with the filename)*

```bash
spice hello
```

```bash
spice translate
```

```bash
spice analyze FILE
```

- EXAMPLE:

```bash
spice analyze code.js
```

---

### Supported Programming Languages for Analysis

[![My Skills](https://skillicons.dev/icons?i=python,js,ruby,go&perline=10)](https://skillicons.dev)

- Python **(.py)**
- JavaScript **(.js)**
- Ruby **(.rb)**
- Go **(.go)**
  
#### All lexers and parsers are built by us. We don't use external libraries/packages to parse your code

---

You can **visit our page on the pypi registry**: [https://pypi.org/project/spicecode/](https://pypi.org/project/spicecode/)

---

### For Development

- Clone the repo to your machine
- Go to the cloned spicecode folder
- Create a python virtual environment (venv):

```bash
python -m venv venv
```

- Activate your virtual environment:

- **Windows**

```bash
./venv/Scripts/activate
```

- **Linux**

```bash
source ./venv/bin/activate
```

- Install all packages from requirements.txt:

```bash
pip install -r requirements.txt
```

- Install (build) the spicecode package locally:

```bash
pip install -e .
```

- Have fun!

```bash
spice version
```

```bash
spice hello
```

```bash
spice translate
```

```bash
spice analyze
```
