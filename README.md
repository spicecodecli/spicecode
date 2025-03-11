# 🌶️ SpiceCode CLI - Making your code spicier 🔥🥵


### Installing via PIP
- Make sure you have Python installed on your system
- Open the terminal
- Install SpiceCode via PIP with:
```
pip install spicecode
```

### Using SpiceCode
- After installing via PIP, you can run these three commands: *(replace file with the filename)*

```
spice hello
```

```
spice translate
```

```
spice analyze FILE
```

- EXAMPLE: 
```
spice analyze code.js
```


---

### Supported Programming Langagues for Analysis:
[![My Skills](https://skillicons.dev/icons?i=python,js,ruby,go&perline=10)](https://skillicons.dev)

- Python **(.py)**
- JavaScript **(.js)**
- Ruby **(.rb)**
- Go **(.go)**
- Many more **coming soon!**
  

#### All lexers and parsers are built by us. We don't use external libraries/packages to parse your code.



---

You can **visit our page on the pypi registry**: https://pypi.org/project/spicecode/

---


### For Development
- Clone the repo to your machine
- Go to the cloned spicecode folder
- Create a python virtual environment (venv):
```
python -m venv venv
```

- Activate your virtual environment:
- **Windows**
```
./venv/Scripts/activate
```
- **Linux**
```
source ./venv/bin/activate
```

- Install all packages from requirements.txt:
```
pip install -r requirements.txt
```

- Install (build) the spicecode package locally:
```
pip install -e .
```

- Have fun!
```
spice version
```
```
spice hello
```
```
spice translate
```
```
spice analyze
```