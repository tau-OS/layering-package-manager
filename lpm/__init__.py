import lpm.cli
from rich.traceback import install

install(show_locals=True)


def initialise():
    lpm.cli.cli()
