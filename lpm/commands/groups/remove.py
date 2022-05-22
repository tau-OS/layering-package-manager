from rich.console import Console
from lpm import dnf
from lpm.handlers.format_transaction import format_transaction_summary

console = Console()
error_console = Console(stderr=True, style="bold red")
base = dnf.base

def command_group_remove(group_name):
    query = base.comps.group_by_pattern(group_name, False)

    if not query:
        error_console.print(f"Group [italic]{group_name}[/italic] not found")
        exit()

    try:
        base.group_remove(query.id)
    except dnf.exceptions.CompsError:
        error_console.print(f"Group [italic]{group_name}[/italic] not installed")
        exit()

    try:
        base.resolve()
    except dnf.exceptions.DepsolveError as error:
        error_console.print("An error occured while handling the transaction:")
        print(error)
        exit()

    format_transaction_summary()