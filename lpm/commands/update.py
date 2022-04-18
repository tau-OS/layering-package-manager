from rich.console import Console
from lpm import dnf
from lpm.handlers.format_transaction import format_transaction_summary

console = Console()
error_console = Console(stderr=True, style="bold red")
base = dnf.base

def command_update(package_name):
    if package_name:
        query = base.sack.query()
        results = query.installed()
        results = results.filter(name=package_name)

        if not results:
            error_console.print(f"Package [italic]{package_name}[/italic] is not installed")
            exit()

        base.upgrade(package_name)
    else:
        base.upgrade_all()

    try:
        base.resolve()
    except dnf.exceptions.DepsolveError as error:
        error_console.print("An error occured while handling the transaction:")
        print(error)
        exit()

    format_transaction_summary()