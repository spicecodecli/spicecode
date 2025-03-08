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
i will write a better tutorial later but for now basically just:
- clone the repo yeah no shit
- create a python virtual enviroment with venv
- install the requirements.txt with ```pip install -r requirements.txt``` (not sure about this one but probably works)
- install the package locally with ```pip install -e . ```
- then run it using ```spice analyze``` followed by the file to be analyzed
- example: ```spice analyze example.js```
