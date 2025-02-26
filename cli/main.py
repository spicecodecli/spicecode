

import typer

app = typer.Typer()


@app.command()
def hello(name: str):
    print(f"Hello {name}")


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye{name}")
    else:
        print(f"get the fuck out  {name}")


if __name__ == "__main__":
    app()